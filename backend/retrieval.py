from pathlib import Path
import json
from typing import List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = Path(__file__).resolve().parent.parent
CHUNKS_PATH = BASE_DIR / "docs" / "processed" / "chunks.jsonl"


class ChunkRetriever:
    def __init__(self):
        self.chunks: List[Dict] = []
        self.texts: List[str] = []
        self.vectorizer = TfidfVectorizer() 
        self.tfidf_matrix = None
        self._load_chunks()
        self._build_index()

    def _load_chunks(self):
        with CHUNKS_PATH.open("r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                self.chunks.append(obj)
                self.texts.append(obj["text"])

    def _build_index(self):
        # Crea la matriz TF-IDF de todos los fragmentos
        self.tfidf_matrix = self.vectorizer.fit_transform(self.texts)

    def retrieve(self, query: str, top_k: int = 5) -> List[Dict]:
        # Calcula similitud coseno entre la consulta y todos los fragmentos
        query_vec = self.vectorizer.transform([query])
        sims = cosine_similarity(query_vec, self.tfidf_matrix)[0]
        # Ordena índices de mayor a menor similitud
        top_indices = sims.argsort()[::-1][:top_k]
        results = []
        for idx in top_indices:
            chunk = self.chunks[idx].copy()
            chunk["score"] = float(sims[idx])
            results.append(chunk)
        return results


# Prueba rápida desde línea de comandos
if __name__ == "__main__":
    retriever = ChunkRetriever()
    pregunta = "¿Cuáles son los requisitos de acceso al curso de especialización?"
    resultados = retriever.retrieve(pregunta, top_k=3)
    for i, r in enumerate(resultados, start=1):
        print(f"\n--- Fragmento {i} (score={r['score']:.3f}, doc_id={r['doc_id']}) ---\n")
        print(r["text"][:500], "...")
