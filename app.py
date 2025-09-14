from flask import Flask, request, jsonify, render_template
import chromadb
from chromadb.utils import embedding_functions

app = Flask(__name__)

# Set up ChromaDB
client = chromadb.Client()
collection = client.get_or_create_collection("chat")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get("question")

    # Dummy response or vector DB query here
    response = f"Echo: {user_question}"

    return jsonify({"answer": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
