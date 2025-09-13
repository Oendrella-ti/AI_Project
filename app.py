from flask import Flask, request, jsonify, render_template
import os
from openai import OpenAI
from pinecone import Pinecone, ServerlessSpec

# ✅ Load API keys securely from environment variables
openai_api_key = os.environ.get("OPENAI_API_KEY")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")

# ✅ Initialize clients
client = OpenAI(api_key=openai_api_key)
pc = Pinecone(api_key=pinecone_api_key)

# ✅ Flask app setup
app = Flask(__name__)

# ✅ Create or connect to Pinecone index
index_name = "my-chat-index"
region = "aped-4627-b74a"  # Replace with your actual Pinecone region

# Ensure index exists
if index_name not in [i['name'] for i in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region=region)
    )

# Connect to the index
index = pc.Index(index_name)

# ✅ Flask routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    # Create embedding using OpenAI v1 SDK
    embedding_response = client.embeddings.create(
        input=user_input,
        model="text-embedding-ada-002"
    )
