from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from utils.loader import load_pdf
from utils.chunker import chunk_documents
from utils.config import PDF_PATH , CHROMA_PATH , EMBED_MODEL

docs = load_pdf(PDF_PATH)
chunks = chunk_documents(docs)

embeddings = OllamaEmbeddings(
    model=EMBED_MODEL
)

db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=CHROMA_PATH

)

db.persist()

print("Documents saved to ChromaDB")
