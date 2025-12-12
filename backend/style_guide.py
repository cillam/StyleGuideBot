import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from datetime import datetime
from pydantic import BaseModel, ConfigDict, ValidationInfo, field_validator
from numpy import array
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv
import os
from anthropic import Anthropic


COLLECTION_NAME = "style_guide_mos"
EMBEDDINGS_MODEL = "text-embedding-3-small"
ENV_LOC = "../backend/.env"
GENERATION_MODEL = "claude-haiku-4-5"


logger = logging.getLogger(__name__)
collection = None
assistant = None


@asynccontextmanager
async def lifespan_mechanism(app: FastAPI):
    logging.info("Starting up  API")

    # Load environment variables
    load_dotenv(ENV_LOC)

    # Create embedding function
    embedding_function = OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name=EMBEDDINGS_MODEL
    )

    # Load the existing collection with the same embedding function
    global collection
    client = chromadb.PersistentClient(path="../data/chroma_db")
    collection = client.get_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )

    # Load text generation model
    global assistant
    assistant = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    yield

    logging.info("Shutting down API")


# Create instance of subapplication
sub_application_style_guide = FastAPI(lifespan=lifespan_mechanism)


# Define input model for single prediction
class StyleGuideQuery(BaseModel):
    pass


# Define output model
class Output(BaseModel):
    reply: str


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

