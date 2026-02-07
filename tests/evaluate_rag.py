"""Lightweight evaluation of RAG answers using keyword checks."""

import json
from pathlib import Path
import requests

API_URL = "http://localhost:7860/ask"
TEST_QUESTIONS = [
    {
        "question": "What events are taking place in Montargis in July 2025?",
        "expected_keywords": ["Montargis", "July", "2025"]
    },
    {
        "question": "Are there workshops for children scheduled this summer?",
        "expected_keywords": ["workshop", "child", "summer"]
    },
    {
        "question": "When does the play 'Embrassons-nous Vaudeville' take place?",
        "expected_keywords": ["Vaudeville", "July"]
    }
]

def ask_question(question: str) -> str:
    """Call the /ask endpoint and return the answer text."""
    response = requests.post(API_URL, json={"question": question})
    response.raise_for_status()
    return response.json()["response"]

def evaluate():
    """Run keyword-based checks against a small question set."""
    print("=== RAG system evaluation ===")
    for q in TEST_QUESTIONS:
        print(f"\nQuestion: {q['question']}")
        try:
            answer = ask_question(q["question"])
            print(f"Answer: {answer}")
            missing_keywords = [kw for kw in q["expected_keywords"] if kw.lower() not in answer.lower()]
            if missing_keywords:
                print(f"Missing keywords in the answer: {missing_keywords}")
            else:
                print("Answer appears relevant.")
        except Exception as e:
            print(f"API call failed: {e}")

if __name__ == "__main__":
    evaluate()
