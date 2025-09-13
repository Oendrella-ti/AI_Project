from flask import Flask, request, jsonify, render_template
import os
import openai
from pinecone import Pinecone, ServerlessSpec

# ✅ Load API keys securely from environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")
pinecone_api_key = os.environ.get("PINECONE_API_KEY")

# ✅ Initialize Flask app
app = Flask(__name__)

# ✅ Initialize Pinecone client
pc = Pinecone(api_key=pinecone_api_key)

# ✅ Create or connect to index
index_name = "my-chat-index"

if index_name not in pc.list_indexes():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )

index = pc.Index(index_name)

# ✅ Flask routes
@app.route("/")
def home():
    return "Chatbot running with Pinecone!"

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")

    # Create embedding
    embedding = openai.Embedding.create(
        input=user_input,
        model="text-embedding-ada-002"
    )["data"][0]["embedding"]

    # Query Pinecone
    results = index.query(vector=embedding, top_k=3, include_metadata=True)
    context = "\n".join([match["metadata"]["text"] for match in results["matches"]])

    # Prompt GPT
    prompt = f"Context:\n{context}\n\nUser: {user_input}\nAI:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"response": response["choices"][0]["message"]["content"]})

@app.route("/ui")
def chat_ui():
    return render_template("index.html")
