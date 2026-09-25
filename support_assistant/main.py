from fastapi import FastAPI
from pydantic import BaseModel, Field

from rag import AnswerResponse, ask_question

app = FastAPI(
    title="Zepto Support Assistant",
    description="Offline-first LangGraph RAG service for Zepto policies",
    version="1.0.0",
)


class AskRequest(BaseModel):
    query: str = Field(..., min_length=1)


@app.get("/")
def root():
    return {"service": "Zepto Support Assistant", "status": "running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AnswerResponse)
def ask(request: AskRequest):
    return ask_question(request.query)
