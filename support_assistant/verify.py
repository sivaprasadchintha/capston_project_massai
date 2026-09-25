import os

from config import COLLECTION_NAME, CHROMA_DIR, DOCS_DIR, MOCK_LLM
from rag import ask_question


def main():
    docs = sorted(
        name
        for name in os.listdir(DOCS_DIR)
        if name.startswith("doc_") and name.endswith(".txt")
    )
    assert len(docs) == 8, f"Expected 8 docs, found {len(docs)}"
    assert os.path.isdir(CHROMA_DIR), "chroma_db does not exist. Run: python ingest.py"

    policy = ask_question("What is the delivery fee for orders below INR 149?")
    assert policy.sources, "Policy query must return sources."
    if MOCK_LLM:
        assert policy.answer.startswith("Based on the retrieved context:")

    general = ask_question("What is the capital of India?")
    assert general.sources == [], "General query must have empty sources."
    if MOCK_LLM:
        assert general.answer == "I can only answer questions about Zepto policies right now."

    print("PASS: 8 documents present")
    print(f"PASS: collection '{COLLECTION_NAME}' is queryable")
    print("PASS: policy route returns sources")
    print("PASS: general route returns empty sources")
    print("PASS: MOCK_LLM baseline checks completed")


if __name__ == "__main__":
    main()
