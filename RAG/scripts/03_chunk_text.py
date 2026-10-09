from utils.loader import load_pdf
from utils.chunker import chunk_documents
from utils.config import PDF_PATH

docs = load_pdf(PDF_PATH)

chunks = chunk_documents(docs)

print(f"Total chunks: {len(chunks)}")
print(chunks[0].page_content)