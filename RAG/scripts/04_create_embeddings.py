from langchain_ollama import OllamaEmbeddings
from utils.config import EMBED_MODEL

embeddings = OllamaEmbeddings(
    model=EMBED_MODEL
)

vector = embeddings.embed_query(
    "What is retrieval augmented generation?"
)

print(len(vector))
print(vector[:10])