from openai import OpenAI
from dotenv import load_dotenv
import os
import json
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

MODEL = "text-embedding-3-small"
ENV_LOC = ".env"
COLLECTION_NAME = "style_guide_mos"


def save_chroma(mos_dict):
    # Get embeddings from OpenAI
    embedding_function = OpenAIEmbeddingFunction(
        api_key=os.getenv("OPENAI_API_KEY"),
        model_name=MODEL
    )
    # Create persistent chromadb
    client = chromadb.PersistentClient(path="./data/chroma_db")
    # Create collection
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_function
    )
    collection.add(
        ids=mos_dict["ids"],
        documents=mos_dict["content"],
        metadatas=mos_dict["metadata"]
    )
    return "Data saved"

# Stringify shortcut list
def prepare_metadata(metadata_dict):
    metadata_copy = metadata_dict.copy()
    # Convert shortcuts list to comma-separated string
    metadata_copy["shortcuts"] = ", ".join(metadata_copy["shortcuts"])
    return metadata_copy


if __name__ == "__main__":
    # Load environment variables
    load_dotenv(ENV_LOC)
    try:
        # Load data
        with open('./data/chunked_mos.json', 'r') as file:
            style_guide = json.load(file)
        chunks_data = style_guide["chunks"]  # Get full chunk objects
        # Save desired metadata
        mos_dictionary = {
            "ids": ["chunk_" + str(num) for num in range(len(chunks_data))],
            "content": [item["content"] for item in chunks_data],
            "metadata": [prepare_metadata(item["metadata"]) for item in chunks_data]
        }
        print(save_chroma(mos_dictionary))

    except Exception as e:
        print(f"\n❌ Failed to save data: {e}")
        exit(1)

        