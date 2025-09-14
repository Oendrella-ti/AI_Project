from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

# Initialize the embedding model and ChromaDB client
model = SentenceTransformer('all-MiniLM-L6-v2')

# Configure ChromaDB with local persistence
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_store"  # Folder where data is saved
))

# Create or load a collection
collection_name = "chatbot"
collection = client.get_or_create_collection(name=collection_name)


def add_documents(documents: list, ids: list):
    """
    Add documents to the ChromaDB collection with embeddings.

    Args:
        documents (list): List of string documents.
        ids (list): Unique IDs for each document.
    """
    embeddings = model.encode(documents).tolist()
    collection.add(documents=documents, embeddings=embeddings, ids=ids)
    print(f"✅ Added {len(documents)} documents to collection '{collection_name}'")


def query_document(query: str, top_k: int = 1):
    """
    Query ChromaDB for the most similar document to the input query.

    Args:
        query (str): The user input or question.
        top_k (int): Number of top results to return.

    Returns:
        str: Most relevant document (or a default response).
    """
    embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=embedding, n_results=top_k)

    if results['documents'] and results['documents'][0]:
        return results['documents'][0][0]  # Return the top document
    else:
        return "Sorry, I couldn't find anything relevant."


def list_all_documents():
    """
    List all stored documents (for debugging or display).
    """
    return collection.get()


def delete_all_documents():
    """
    Delete all documents from the collection (for resetting).
    """
    client.delete_collection(collection_name)
    print(f"🗑️ Deleted collection '{collection_name}'")


# Optional: Call this to persist to disk manually
def persist_db():
    client.persist()
