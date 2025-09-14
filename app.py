import sys
sys.path.insert(0, "/mnt/data/AI_Project/libs")
from flask import Flask, request, jsonify, render_template
import chromadb
from chromadb.utils import embedding_functions

# Initialize Flask app
app = Flask(__name__)
# Initialize ChromaDB with SentenceTransformer embedding function
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
client = chromadb.Client()
collection = client.get_or_create_collection(name="chat",embedding_function=sentence_transformer_ef)
# Set up ChromaDB
#client = chromadb.Client()
#collection = client.get_or_create_collection("chat")
# Optional: Add sample documents if collection is empty
if len(collection.get()["ids"]) == 0:
    collection.add(
        documents=[
            "ChromaDB is an open-source embedding database for AI applications.",
            "Flask is a lightweight web framework written in Python.",
            "LangChain enables building applications with LLMs using modular components.",
            "Terraform automates infrastructure deployment and provisioning.",
            "Lion is the king of Jungle.",
            "DevOps is a cultural philosophy, a set of practices, and tools that integrate software development (Dev) and IT operations (Ops) to deliver high-quality applications and services faster and more reliably.",
            "C.P. Radhakrishnan will be sworn in as the 15th Vice President of India today. President Droupadi Murmu will administer the oath of office to Mr Radhakrishnan at Rashtrapati Bhavan."
        ],
        ids=["1", "2", "3", "4", "5", "6", "7"]
    )

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get("question")

    # Dummy response or vector DB query here
    response = f"Echo: {user_question}"
    results = collection.query(
        query_texts=[user_question],
        n_results=1
    )
    if results["documents"] and results["documents"][0]:
        response = results["documents"][0][0]
    else:
        response = "Sorry, I couldn't find a relevant answer."
    return jsonify({"answer": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
import sys
sys.path.insert(0, "/mnt/data/AI_Project/libs")
from flask import Flask, request, jsonify, render_template
import chromadb
from chromadb.utils import embedding_functions

# Initialize Flask app
app = Flask(__name__)
# Initialize ChromaDB with SentenceTransformer embedding function
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)
client = chromadb.Client()
collection = client.get_or_create_collection(name="chat",embedding_function=sentence_transformer_ef)
# Set up ChromaDB
#client = chromadb.Client()
#collection = client.get_or_create_collection("chat")
# Optional: Add sample documents if collection is empty
if len(collection.get()["ids"]) == 0:
    collection.add(
        documents=[
            "ChromaDB is an open-source embedding database for AI applications.",
            "Flask is a lightweight web framework written in Python.",
            "LangChain enables building applications with LLMs using modular components.",
            "Terraform automates infrastructure deployment and provisioning."
            "Lion is the king of Jungle"
            "DevOps is a cultural philosophy, a set of practices, and tools that integrate software development (Dev) and IT operations (Ops) to deliver high-quality applications and services faster and more reliably."
            "C.P. Radhakrishnan will be sworn in as the 15th Vice President of India today. President Droupadi Murmu will administer the oath of office to Mr Radhakrishnan at Rashtrapati Bhavan"
        ],
        ids=["1", "2", "3", "4", "5", "6", "7"]
    )

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/ask', methods=['POST'])
def ask():
    user_question = request.json.get("question")

    # Dummy response or vector DB query here
    response = f"Echo: {user_question}"
    results = collection.query(
        query_texts=[user_question],
        n_results=1
    )
    if results["documents"] and results["documents"][0]:
        response = results["documents"][0][0]
    else:
        response = "Sorry, I couldn't find a relevant answer."
    return jsonify({"answer": response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

