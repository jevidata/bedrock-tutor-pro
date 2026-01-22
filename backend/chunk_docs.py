from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED_DIR = BASE_DIR / "docs" / "processed"
CHUNKS_PATH = PROCESSED_DIR / "chunks.jsonl"

CHUNK_SIZE = 800      # número aproximado de palabras por fragmento
CHUNK_OVERLAP = 100   # solapamiento entre fragmentos


def chunk_text(text: str, doc_id: str):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + CHUNK_SIZE
        chunk_words = words[start:end]
        if not chunk_words:
            break
        chunk_text_str = " ".join(chunk_words)
        chunks.append(
            {
                "doc_id": doc_id,
                "start_word": start,
                "end_word": min(end, len(words)),
                "text": chunk_text_str,
            }
        )
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def process_all_txt():
    CHUNKS_PATH.unlink(missing_ok=True)

    with CHUNKS_PATH.open("w", encoding="utf-8") as f_out:
        for txt_path in PROCESSED_DIR.glob("*.txt"):
            print(f"Troceando {txt_path.name}...")
            text = txt_path.read_text(encoding="utf-8")
            doc_id = txt_path.stem
            chunks = chunk_text(text, doc_id)
            for chunk in chunks:
                f_out.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    print(f"Fragmentos guardados en {CHUNKS_PATH}")


if __name__ == "__main__":
    process_all_txt()
