from flask import Flask, request, jsonify, render_template
import openai

import os
from pinecone import Pinecone
from pinecone import ServerlessSpec
PINECONE_API_KEY = "pcsk_51FPJa_RYw8Xpzei3DpqiHsdvyaiSdoFwSX7oY2XhFgCedty8FzCw5FiauTwXSSbEQVnfZ"
# Initialize Pinecone instance
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

# Connect to an existing index
index = pc.Index("your-index-name")

app = Flask(__name__)

# Init API Keys
openai.api_key = "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"
pinecone.init(api_key="pcsk_51FPJa_RYw8Xpzei3DpqiHsdvyaiSdoFwSX7oY2XhFgCedty8FzCw5FiauTwXSSbEQVnfZ", environment="aws-starter")
index = pinecone.Index("my-chat-index")

pc.create_index(                                                                                                                                   
            name='my-chat-index',                                                                                                                                  
            dimension=1536,                                                                                                                                
            metric='cosine',                                                                                                                                  
            spec=ServerlessSpec(cloud="aws",region="us-east-1")                                                                                                                                        
        )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    embedding = openai.Embedding.create(
        input=user_input, model="text-embedding-ada-002"
    )["data"][0]["embedding"]

    results = index.query(vector=embedding, top_k=3, include_metadata=True)
    context = "\n".join([match["metadata"]["text"] for match in results["matches"]])

    prompt = f"Context:\n{context}\n\nUser: {user_input}\nAI:"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return jsonify({"response": response["choices"][0]["message"]["content"]})
