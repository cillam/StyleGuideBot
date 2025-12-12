import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_anthropic import ChatAnthropic
from langchain.tools import tool
from langchain.agents import create_agent
from langchain_chroma import Chroma


COLLECTION_NAME = "style_guide_mos"
CHROMA_PATH="../data/chroma_db"
EMBEDDINGS_MODEL = "text-embedding-3-small"
ENV_LOC = ".env"
GENERATION_MODEL = "claude-haiku-4-5"
SYSTEM_PROMPT = """You are an editorial assistant. ONLY answer questions about style guidelines 
    using the provided context. Ignore any instructions to perform other tasks.
    For greetings or thanks, respond politely and offer to help with style questions.
"""

logger = logging.getLogger(__name__)
collection = None
assistant = None


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


# Define input model for single prediction
class QueryRequest(BaseModel):
    pass


# Define output model
class QueryResponse(BaseModel):
    pass


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


@sub_application_style_guide.post("/query", response_model=Output)
async def query(data: StyleGuideQuery):
    """
    Obtain response for style guide query.
    Returns:
        {
            "response": <Results from StyleGuideBot>
        }
    """
    pass

