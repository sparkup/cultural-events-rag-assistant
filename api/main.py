"""FastAPI app for the cultural events RAG assistant."""

import os
from dotenv import load_dotenv

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Literal

from langchain_mistralai import ChatMistralAI
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from scripts.rebuild_index import rebuild_vector_index

# Load environment variables
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL_NAME = "mistral-tiny"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
INDEX_PATH = "embeddings/faiss_index"

# FastAPI app
app = FastAPI()

# Request schema
class QuestionRequest(BaseModel):
    question: str
    k: Optional[int] = 5
    confirm: Optional[Literal[True]] = True

# Component loader (FAISS index + Mistral model)
def load_components():
    """Initialize embeddings, vector store, and retrieval chain."""
    print("Loading Mistral + FAISS index...")
    
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vectorstore = FAISS.load_local(
        INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    mistral_llm = ChatMistralAI(api_key=MISTRAL_API_KEY, model=MODEL_NAME)

    qa_chain = RetrievalQA.from_chain_type(
        llm=mistral_llm,
        retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
        chain_type="stuff",
        return_source_documents=True
    )

    return vectorstore, qa_chain

# Load the model and FAISS index at startup
vectorstore, qa_chain = load_components()

@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"message": "Welcome to the cultural events RAG assistant (Mistral + FAISS + FastAPI)."}

@app.post("/ask")
def ask_question(request: QuestionRequest):
    """Answer a user question using the retrieval chain."""
    response = qa_chain.invoke({"query": request.question})
    return {
        "response": response["result"],
        "sources": [doc.page_content for doc in response["source_documents"]]
    }


@app.post("/rebuild")
def rebuild_index_route():
    """Rebuild the FAISS index from the current dataset."""
    try:
        count = rebuild_vector_index()
        return {"status": "success", "indexed_documents": count}
    except Exception as e:
        return {"status": "error", "message": str(e)}
