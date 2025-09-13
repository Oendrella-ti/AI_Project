import openai
import pinecone

openai.api_key = "YOUR_OPENAI_KEY"
pinecone.init(api_key="YOUR_PINECONE_KEY", environment="us-east-1")

index = pinecone.Index("chatbot-index")

docs = [
    {"id": "1", "text": "DeepSeek is a state-of-the-art language model."},
    {"id": "2", "text": "Pinecone is used for storing embeddings."}
]

def get_embedding(text):
    res = openai.Embedding.create(input=[text], model="text-embedding-ada-002")
    return res["data"][0]["embedding"]

vectors = [{
    "id": doc["id"],
    "values": get_embedding(doc["text"]),
    "metadata": {"text": doc["text"]}
} for doc in docs]

index.upsert(vectors=vectors)
print("Data uploaded.")
