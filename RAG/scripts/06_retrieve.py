from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from utils.config import CHROMA_PATH , EMBED_MODEL

embeddings = OllamaEmbeddings(
    model=EMBED_MODEL

)

db = Chroma(
    persist_directory=CHROMA_PATH,
    embeddings=embeddings
)

query = "What is this document about?"

results = db.similarity_search(
    query,
    k=3
)

for i, doc in enumerate(results, 1):
    print(f"\n--- Result {i} ---\n")
    print(doc.page_content[:500])