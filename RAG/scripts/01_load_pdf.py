from utils.loader import load_pdf
from utils.config import PDF_PATH

docs = load_pdf(PDF_PATH)

print(f"Pages loaded: {len(docs)}")
print(docs[0].page_content[:500])