from flask import Flask, request, jsonify, render_template
import openai
import pinecone

app = Flask(__name__)

# Init API Keys
openai.api_key = "Open_API_KEY"
pinecone.init(api_key="Pine_Cone_API_Key", environment="gcp-starter")
index = pinecone.Index("my-chat-index")

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
