import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv
import os

COLLECTION_NAME = "style_guide_mos"
MODEL = "text-embedding-3-small"
ENV_LOC = "../backend/.env"

# Load environment variables
load_dotenv(ENV_LOC)

# Create embedding function
embedding_function = OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name=MODEL
)

# Load the existing collection with the same embedding function
client = chromadb.PersistentClient(path="../data/chroma_db")
collection = client.get_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)

# Test queries
test_queries = [
    "Should I use the Oxford comma?",
    "How do I format quotations?",
    "When should I capitalize words?"
]

print("Testing Vector Store Retrieval")
print("=" * 80)

for query in test_queries:
    print(f"\nQuery: {query}")
    print("-" * 80)
    
    # Now you can use query_texts - Chroma will embed automatically!
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    
    # Display results
    for i, (doc, metadata, distance) in enumerate(zip(
        results['documents'][0],
        results['metadatas'][0],
        results['distances'][0]
    ), 1):
        print(f"\nResult {i}:")
        print(f"  Title: {metadata['title']}")
        print(f"  Parent: {metadata.get('parent', 'None')}")
        print(f"  Shortcuts: {metadata.get('shortcuts', 'None')}")
        print(f"  Distance: {distance:.4f}")
        print(f"  Content preview: {doc[:150]}...")