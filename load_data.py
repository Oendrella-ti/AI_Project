from vector_store import add_documents, persist_db

docs = [
    "Python is a programming language.",
    "A neural network is inspired by the human brain.",
    "Flask is a lightweight web framework for Python."
]
ids = ["1", "2", "3"]

add_documents(docs, ids)
persist_db()
