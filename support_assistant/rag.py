import json
from typing import Literal, TypedDict

from groq import Groq
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field, ValidationError

from config import GROQ_API_KEY, GROQ_MODEL, MOCK_LLM
from prompts import CLASSIFICATION_PROMPT, STRUCTURED_PROMPT
from retrieval import PolicyRetriever
from policy_keywords import Policy_Keywords


class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]
    confidence: float = Field(ge=0.0, le=1.0)


class SupportState(TypedDict, total=False):
    query: str
    intent: Literal["policy_question", "general_question"]
    retrieved_documents: list[str]
    retrieved_ids: list[str]
    answer: str
    sources: list[str]
    confidence: float
    response: dict


POLICY_KEYWORDS = Policy_Keywords

retriever = PolicyRetriever()
groq_client = None
if not MOCK_LLM:
    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY is required when MOCK_LLM=0.")
    groq_client = Groq(api_key=GROQ_API_KEY)


def classify_intent_mock(query: str) -> str:
    lowered = query.lower()
    return (
        "policy_question"
        if any(keyword in lowered for keyword in POLICY_KEYWORDS)
        else "general_question"
    )


def classify_intent_real(query: str) -> str:
    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=0,
        messages=[
            {"role": "system", "content": CLASSIFICATION_PROMPT.format(query=query)},
            {"role": "user", "content": query},
        ],
    )
    label = response.choices[0].message.content.strip()
    return label if label in {"policy_question", "general_question"} else "general_question"


def classify_intent(state: SupportState):
    query = state["query"]
    intent = classify_intent_mock(query) if MOCK_LLM else classify_intent_real(query)
    return {"intent": intent}


def parse_llm_response(raw: str, fallback_sources: list[str]) -> AnswerResponse:
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`")
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
    parsed = json.loads(cleaned)
    return AnswerResponse.model_validate(parsed)


def generate_structured_answer(query: str, context: str, source_ids: list[str]) -> AnswerResponse:
    base_prompt = STRUCTURED_PROMPT.format(
        question=query,
        context=context,
        source_ids=", ".join(source_ids),
    )
    last_error = None
    for attempt in range(3):
        prompt = base_prompt
        if attempt:
            prompt += (
                "\n\nCORRECTION: Your previous response failed validation. "
                "Return ONLY a valid JSON object with answer, sources, and confidence."
            )
        response = groq_client.chat.completions.create(
            model=GROQ_MODEL,
            temperature=0,
            messages=[
                {"role": "system", "content": "You are a strict JSON-producing Zepto support assistant."},
                {"role": "user", "content": prompt},
            ],
        )
        raw = response.choices[0].message.content
        try:
            return parse_llm_response(raw, source_ids)
        except (json.JSONDecodeError, ValidationError, TypeError) as exc:
            last_error = exc

    return AnswerResponse(
        answer=f"ERROR: real LLM output failed schema validation after 3 attempts ({last_error}).",
        sources=source_ids,
        confidence=0.0,
    )


def retrieve_and_answer(state: SupportState):
    query = state["query"]
    documents, source_ids, _, _ = retriever.retrieve(query, top_k=3)

    if MOCK_LLM:
        answer = f"Based on the retrieved context: {documents[0][:200]}"
        response = AnswerResponse(answer=answer, sources=source_ids, confidence=1.0)
    else:
        context = "\n\n".join(
            f"[{sid}]\n{text}" for sid, text in zip(source_ids, documents)
        )
        response = generate_structured_answer(query, context, source_ids)

    return {
        "retrieved_documents": documents,
        "retrieved_ids": source_ids,
        "answer": response.answer,
        "sources": response.sources,
        "confidence": response.confidence,
        "response": response.model_dump(),
    }


def direct_answer(state: SupportState):
    query = state["query"]
    if MOCK_LLM:
        response = AnswerResponse(
            answer="I can only answer questions about Zepto policies right now.",
            sources=[],
            confidence=1.0,
        )
    else:
        response = generate_structured_answer(query, "", [])
    return {
        "answer": response.answer,
        "sources": response.sources,
        "confidence": response.confidence,
        "response": response.model_dump(),
    }


def route_query(state: SupportState):
    return "retrieve_and_answer" if state["intent"] == "policy_question" else "direct_answer"


def build_graph():
    graph = StateGraph(SupportState)
    graph.add_node("classify_intent", classify_intent)
    graph.add_node("retrieve_and_answer", retrieve_and_answer)
    graph.add_node("direct_answer", direct_answer)
    graph.add_edge(START, "classify_intent")
    graph.add_conditional_edges(
        "classify_intent",
        route_query,
        {
            "retrieve_and_answer": "retrieve_and_answer",
            "direct_answer": "direct_answer",
        },
    )
    graph.add_edge("retrieve_and_answer", END)
    graph.add_edge("direct_answer", END)
    return graph.compile()


def ask_question(query: str) -> AnswerResponse:
    result = build_graph().invoke({"query": query})
    return AnswerResponse.model_validate(result["response"])
