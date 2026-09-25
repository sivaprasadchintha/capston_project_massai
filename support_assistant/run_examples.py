import json

from rag import ask_question


examples = [
    "What is the delivery fee for orders below INR 149?",
    "What is the capital of India?",
]

for query in examples:
    response = ask_question(query)
    print(json.dumps({"query": query, **response.model_dump()}, ensure_ascii=False))
