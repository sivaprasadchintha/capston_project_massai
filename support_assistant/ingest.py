import os

import chromadb
from sentence_transformers import SentenceTransformer

from config import CHROMA_DIR, COLLECTION_NAME, DOCS_DIR, EMBEDDING_MODEL_NAME


def load_documents():
    files = sorted(
        os.path.join(DOCS_DIR, name)
        for name in os.listdir(DOCS_DIR)
        if name.startswith("doc_") and name.endswith(".txt")
    )
    if len(files) != 8:
        raise RuntimeError(f"Expected exactly 8 corpus documents, found {len(files)}.")

    chunks = []
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read().strip()

        if not text:
            raise RuntimeError(f"Empty document: {os.path.basename(file_path)}")

        document_id = os.path.splitext(os.path.basename(file_path))[0]
        chunks.append(
            {
                "chunk_id": f"{document_id}_chunk_01",
                "document_id": document_id,
                "source": os.path.basename(file_path),
                "text": text,
            }
        )

    return chunks


def build_vector_store():
    chunks = load_documents()
    print(f"Loaded {len(chunks)} documents as {len(chunks)} chunks.")

    model = SentenceTransformer(EMBEDDING_MODEL_NAME)
    embeddings = model.encode(
        [chunk["text"] for chunk in chunks],
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    os.makedirs(CHROMA_DIR, exist_ok=True)
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    collection.add(
        ids=[chunk["chunk_id"] for chunk in chunks],
        documents=[chunk["text"] for chunk in chunks],
        embeddings=embeddings.tolist(),
        metadatas=[
            {
                "document_id": chunk["document_id"],
                "source": chunk["source"],
            }
            for chunk in chunks
        ],
    )

    print(f"Stored {collection.count()} chunks in '{COLLECTION_NAME}'.")
    return collection


if __name__ == "__main__":
    build_vector_store()
