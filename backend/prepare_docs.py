from pathlib import Path
from pypdf import PdfReader

# Directorios base
BASE_DIR = Path(__file__).resolve().parent.parent  # carpeta bedrock-tutor-pro
SOURCE_DIR = BASE_DIR / "docs" / "source"
PROCESSED_DIR = BASE_DIR / "docs" / "processed"


def extract_text_from_pdf(pdf_path: Path) -> str:
    """Extrae el texto de un PDF página a página."""
    reader = PdfReader(str(pdf_path))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"
    return text


def process_all_pdfs():
    """Procesa todos los PDFs de docs/source y guarda .txt en docs/processed."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    for pdf_path in SOURCE_DIR.glob("*.pdf"):
        print(f"Procesando {pdf_path.name}...")
        try:
            text = extract_text_from_pdf(pdf_path)
        except Exception as e:
            print(f"  !! Error procesando {pdf_path.name}: {e}")
            continue

        out_path = PROCESSED_DIR / (pdf_path.stem + ".txt")
        out_path.write_text(text, encoding="utf-8")
        print(f"  -> Guardado {out_path.name}")



if __name__ == "__main__":
    process_all_pdfs()
