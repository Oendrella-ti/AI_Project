from flask import Flask, request, jsonify, render_template
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings

app = Flask(__name__, static_url_path='/static')

# Setup ChromaDB
client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_store"))
collection = client.get_or_create_collection(name="chatbot")

# Embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    embedding = model.encode([user_input]).tolist()

    results = collection.query(query_embeddings=embedding, n_results=1)
    matched = results['documents'][0][0] if results['documents'] else "Sorry, I don't understand."

    return jsonify({'response': matched})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
