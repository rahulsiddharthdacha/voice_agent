# vectorstore/build_store.py

import json
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def build():
    with open("data/processed/wise_articles.json") as f:
        articles = json.load(f)

    texts = []
    metadatas = []

    for a in articles:
        texts.append(
            f"Question: {a['question']}\n\nAnswer: {a['answer']}"
        )
        metadatas.append({
            "source": a["source"],
            "question": a["question"]
        })

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    db = FAISS.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas
    )

    db.save_local("vectorstore/wise_faq")
    print("Vector store built successfully")

if __name__ == "__main__":
    build()
