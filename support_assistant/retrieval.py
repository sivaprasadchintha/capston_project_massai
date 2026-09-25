import chromadb
from sentence_transformers import SentenceTransformer

from config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL_NAME


class PolicyRetriever:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.collection = self.client.get_collection(COLLECTION_NAME)

    def retrieve(self, query: str, top_k: int = 3):
        query_embedding = self.model.encode(
            [query], normalize_embeddings=True
        )[0]
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"],
        )
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        ids = [metadata["document_id"] + "_chunk_01" for metadata in metadatas]
        return documents, ids, metadatas, distances
