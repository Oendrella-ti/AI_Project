from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import numpy as np
# Load embedding model
embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# Pinecone Init
pc = Pinecone(api_key="YOUR_PINECONE_API_KEY")
index = pc.Index("my-chat-index")
#pinecone.init(api_key="YOUR_PINECONE_API_KEY", environment="us-east-1")
index_name = "my-chat-index"
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create index if it doesn't exist
#if index_name not in pinecone.list_indexes():
if index_name not in pc.list_indexes().names()
    pc.create_index(name=index_name, dimension=384, metric="cosine")

index = pc.Index(index_name)

#def store_query(query, metadata):
 #   vector = embed_model.encode([query])[0]
  #  index.upsert([(metadata['id'], vector.tolist(), metadata)])
def store_query(query, namespace="default"):
    embedding = model.encode(query).tolist()
    index.upsert(vectors=[{"id": query, "values": embedding}], namespace=namespace)    
