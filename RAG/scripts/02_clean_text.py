from utils.loader import load_pdf
from utils.cleaner import clean_text
from utils.config import PDF_PATH

docs = load_pdf(PDF_PATH)
cleaned = clean_text(docs[0].page_content)
print(cleaned[:500])
