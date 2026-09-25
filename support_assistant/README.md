# Zepto Support Assistant

A small, complete, offline-first GenAI/RAG service for Zepto policy questions. The required grading path uses deterministic `MOCK_LLM=1` behavior, so no LLM API key or LLM-provider network call is needed. The optional `MOCK_LLM=0` path uses Groq for intent classification and answer generation.

## Assignment requirements covered

- 8 exact Zepto policy documents in `docs/`
- Local `sentence-transformers/all-MiniLM-L6-v2` embeddings
- Persistent ChromaDB collection `zepto_policies`
- Cosine-similarity top-3 retrieval
- Structured prompt with Role, Context, Task, Format, Length, negative constraint, and few-shot example
- LangGraph `StateGraph` with `TypedDict` state
- Required nodes: `classify_intent`, `retrieve_and_answer`, `direct_answer`
- Conditional routing after classification
- Exact mock keyword heuristic required by the assignment
- Deterministic mock answer and Pydantic validation
- Optional Groq path with up to 3 total validation attempts
- FastAPI `POST /ask`
- Dockerfile exposing port 7860

## 1. Architecture

> **Implementation note:** This project uses Python's built-in `os` module for file and directory paths.

```text
INGESTION
8 docs/*.txt
    |
    v
ingest.py
one document -> one chunk
    |
    v
EMBEDDING
SentenceTransformer
all-MiniLM-L6-v2
    |
    v
STORAGE
ChromaDB / zepto_policies
cosine space

QUERY
user query
    |
    v
LangGraph
classify_intent
    |
    +---------------------------+
    |                           |
policy_question          general_question
    |                           |
    v                           v
retrieve_and_answer       direct_answer
    |
    v
query embedding -> ChromaDB -> top 3 chunks
    |
    +---------------------------+
    |                           |
MOCK_LLM=1                 MOCK_LLM=0
    |                           |
fixed deterministic       Groq generation
answer                    using structured prompt
    |                           |
    +-------------+-------------+
                  v
        Pydantic AnswerResponse
        answer / sources / confidence
                  |
                  v
              FastAPI /ask
```

### Ingestion
`ingest.py` reads the eight files and uses one whole document as one chunk, which is explicitly allowed by the assignment because the documents are short. Each chunk gets an ID such as `doc_01_chunk_01`.

### Embedding
`ingest.py` embeds every chunk with `sentence-transformers/all-MiniLM-L6-v2`. At query time `retrieval.py` embeds the incoming query with the same model.

### Retrieval
`retrieval.py` sends the query embedding to the persistent ChromaDB collection `zepto_policies`. The collection is configured for cosine distance and returns the top three most similar chunks. No keyword reranking is used, so the retrieval order is the actual ChromaDB cosine-similarity result required by the assignment.

### Generation and routing
`rag.py` builds a LangGraph `StateGraph`. `classify_intent` routes to `retrieve_and_answer` or `direct_answer` through a conditional edge. Retrieval always runs for policy questions in both modes. Only LLM-dependent generation/classification branches on `MOCK_LLM`.

## 2. MOCK_LLM behavior (graded baseline)

`MOCK_LLM` defaults to enabled unless explicitly set to `0`.

When `MOCK_LLM=1` or is unset:

- `classify_intent` uses exactly these policy keywords: `delivery`, `return`, `refund`, `membership`, `tracking`, `cancel`, `gift card`, `support hours`.
- No Groq/OpenAI/other LLM call is made.
- Policy queries perform real Sentence Transformer embedding and ChromaDB top-3 retrieval.
- `retrieve_and_answer` returns `Based on the retrieved context: ` followed by the first approximately 200 characters of the top retrieved chunk.
- `direct_answer` returns the fixed string `I can only answer questions about Zepto policies right now.`
- `sources` contains the retrieved chunk IDs for policy questions and is empty for general questions.
- `confidence` is deterministically `1.0`.

This is the path intended for grading.

## 3. Optional Groq mode

Create `.env` and set:

```env
MOCK_LLM=0
GROQ_API_KEY=your_key_here
GROQ_MODEL=openai/gpt-oss-20b
```

Groq is only the optional LLM backend. It does **not** replace the required `all-MiniLM-L6-v2` embedding model. Retrieval remains:

```text
query -> all-MiniLM-L6-v2 -> ChromaDB cosine search -> top 3
```

With `MOCK_LLM=0`, the optional path uses Groq for classification and generation. Real generation is prompted with the structured prompt in `prompts.py`. Invalid JSON/schema output is retried up to two additional times (three attempts total); after the final failure, a clearly marked `ERROR:` response with confidence `0.0` is returned.

## 4. Installation

Windows PowerShell:

```powershell
pip install -r requirements.txt
```


Create `.env`:

```env
MOCK_LLM=1
```

## 5. Build the vector database

Run from the `support_assistant` directory:

```powershell
python ingest.py
```

The first embedding-model load may download/cache the Sentence Transformer model. After ingestion, `chroma_db/` contains the persistent local vector database.

Expected final message:

```text
Stored 8 chunks in 'zepto_policies'.
```

## 6. Verify the required baseline

```powershell
python verify.py
```

The verifier checks that all eight corpus files exist, the ChromaDB collection is queryable, policy queries return sources, and general queries return an empty source list.

## 7. Run example calls

```powershell
python run_examples.py
```

Two required examples are included:

1. Policy question: `What is the delivery fee for orders below INR 149?`
2. General question: `What is the financial capital of India?`

Because embeddings are computed locally, exact top-3 source ordering should be recorded from the output of your own run. A representative mock response has this form:

```json
{"query":"What is the delivery fee for orders below INR 149?","answer":"Based on the retrieved context: ...","sources":["doc_01_chunk_01","...","..."],"confidence":1.0}
{"query":"What is the capital of India?","answer":"I can only answer questions about Zepto policies right now.","sources":[],"confidence":1.0}
```

For the final submitted README, replace the ellipsis/source placeholders in the first line with the raw output produced by `python run_examples.py` on the submission machine. This avoids documenting a potentially machine/version-specific nearest-neighbor ordering as a fact.

## 8. Run FastAPI

```powershell
python -m uvicorn main:app --reload
```

Open Swagger:

```text
http://127.0.0.1:8000/docs
```

Or call:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/ask" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"query":"What is the delivery fee for orders below INR 149?"}'
```

General question:

```powershell
Invoke-RestMethod `
  -Uri "http://127.0.0.1:8000/ask" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"query":"What is the financial capital of India?"}'
```

The response schema is:

```json
{
  "answer": "string",
  "sources": ["chunk_id"],
  "confidence": 1.0
}
```

## 9. Docker

The required Docker baseline uses port 7860:

```powershell
docker build -t support_assistant .

docker run --rm -p 7860:7860 support_assistant
```

Then open:

```text
http://127.0.0.1:7860/docs
or
http://localhost:7860/docs
```

The image starts FastAPI with:

```text
uvicorn main:app --host 0.0.0.0 --port 7860
```

The Docker baseline starts with `MOCK_LLM=1`. For an offline/local container test, run `python ingest.py` first and copy the generated `chroma_db/` directory into the build context, or extend the image build to download/cache the embedding model and run ingestion during image construction. The assignment only requires a locally buildable/runnable Dockerfile; no cloud deployment is required.

## 10. File responsibilities

| File | Responsibility |
|---|---|
| `docs/*.txt` | Exact Zepto corpus |
| `config.py` | Paths and environment configuration |
| `ingest.py` | Load, chunk, embed, and index corpus |
| `retrieval.py` | Query embedding + ChromaDB cosine top-3 retrieval |
| `prompts.py` | Required structured prompt and classification prompt |
| `policy_keywords.py` |  Classification of policy keywords |
| `rag.py` | Pydantic schema + LangGraph nodes/router + mock/Groq logic |
| `main.py` | FastAPI application and `/ask` endpoint |
| `verify.py` | Baseline verification checks |
| `run_examples.py` | Two rubric demonstration calls |
| `Dockerfile` | Local container execution |

## 11. Grading checklist

- [x] 8 exact corpus documents
- [x] Local all-MiniLM-L6-v2 embeddings
- [x] ChromaDB persistent collection
- [x] Cosine top-3 retrieval
- [x] Role/context/task/format/length prompt
- [x] Explicit negative constraint
- [x] Few-shot example
- [x] TypedDict LangGraph state
- [x] Three required graph nodes
- [x] Conditional edge
- [x] Exact required mock keyword heuristic
- [x] Mock retrieval + canned answer
- [x] Mock direct answer
- [x] Pydantic response schema
- [x] Real-LLM retry logic
- [x] FastAPI POST `/ask`
- [x] Dockerfile
- [x] Architecture description

Optional Groq and Hugging Face deployment are not required for full marks.
