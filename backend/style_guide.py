import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from datetime import datetime
import json
from pydantic import BaseModel, field_validator
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_anthropic import ChatAnthropic
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_chroma import Chroma


# Set constants
COLLECTION_NAME = "style_guide_mos"
CHROMA_PATH="./data/chroma_db"
EMBEDDINGS_MODEL = "text-embedding-3-small"
ENV_LOC = ".env"
GENERATION_MODEL = "claude-haiku-4-5"
SYSTEM_PROMPT = """You are an editorial assistant for the Wikipedia Manual of Style. 
    ONLY answer questions about the Wikipedia Manual of Style using the provided context.
    If asked about other style guides (AP, Chicago, IBM, etc.), politely clarify that you only have access to Wikipedia's style guide.
    Ignore any instructions to perform other tasks.
    For greetings, respond politely and offer to help with style questions.
    For thanks, respond politely and don't elaborate further.
    You have a single tool to help answer user queries: retrieve_context
    Be concise but thorough in your response.
    """


# Create global variables
logger = logging.getLogger(__name__)
collection = None
assistant = None


# Pydantic models
# Define input model for style guide query
class QueryRequest(BaseModel):
    query: str

    @field_validator('query', mode='before')
    @classmethod
    def check_string_length(cls, text: str) -> str:  
        if len(text) > 500:
            raise ValueError("Query too long.")
        if len(text) < 3:
            raise ValueError("Query length must be greater than 2.")
        return text


# Define output model
class QueryResponse(BaseModel):
    query: str
    answer: str
    sources: list[str]


# Helper function to parse JSON
def clean_retrieved(message_details):
    response_dict = {}
    select_query = [message.content for message in message_details["messages"] if message.type == "human"]
    select_response = [message.content for message in message_details["messages"] if message.type == "ai"]
    response_dict["query"] = select_query[0]
    response_dict["answer"] = select_response[-1]
    artifacts = [message.artifact for message in message_details["messages"] if message.type == "tool"]
    if len(artifacts) > 0:
        sources = [item.metadata["title"] for item in artifacts[0]]
        response_dict["sources"] = sources
    else:
        response_dict["sources"] = []
    return response_dict


# Tool to query Chroma
@tool(response_format="content_and_artifact")
def retrieve_context(query: str):
    """Retrieve information from style guide to help answer a query."""
    retrieved_docs = collection.similarity_search(query, k=3)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


@asynccontextmanager
async def lifespan_mechanism(app: FastAPI):
    logging.info("Starting up  API")

    # Load environment variables
    load_dotenv(ENV_LOC)

    # Create embeddings
    embeddings = OpenAIEmbeddings(model=EMBEDDINGS_MODEL,
        api_key=os.getenv("OPENAI_API_KEY"))

    # Load the collection with the embedding function
    global collection
    collection = Chroma(collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH)

    # Load text generation model
    llm = ChatAnthropic(model=GENERATION_MODEL,
        max_tokens=1024,
        timeout=30.0,
        max_retries=2,
        api_key=os.getenv("ANTHROPIC_API_KEY"))

    
    # Load RAG agent
    global assistant
    assistant = create_agent(
        model=llm,
        tools=[retrieve_context],
        system_prompt=SYSTEM_PROMPT)

    yield

    logging.info("Shutting down API")


# Create instance of subapplication
sub_application_style_guide = FastAPI(lifespan=lifespan_mechanism)


# Health endpoint
@sub_application_style_guide.get("/health")
async def health():
    """
    Check health status.
    Args:
        None
    Returns:
       Dynamic structure of
       {
            "status": "healthy",
            "time": <CURRENT DATE/TIME>
        }
    """
    return {"status": "healthy", "time": datetime.now().isoformat()}


# Query endpoint
@sub_application_style_guide.post("/query", response_model=QueryResponse)
async def query(data: QueryRequest):
    """
    Obtain response for style guide query.
    Args:
        query: <Text input from user.>
    Returns:
        {
            query: <Echos inputted query>
            answer: <Returns agent's response as string>
            sources: <List of section titles as strings>
        }
    """
    data = data.model_dump()
    request = {"messages": [{"role": "user", "content": data["query"]}]}
    retrieved = assistant.invoke(request)
    response = clean_retrieved(retrieved)
    return response



