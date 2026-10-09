from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings

from langchain_community.vectorstores import Chroma

from utils.config import (
    CHROMA_PATH,
    EMBED_MODEL,
    LLM_MODEL
)

embeddings = OllamaEmbeddings(
    model=EMBED_MODEL
)

db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embeddings
)

retriever = db.as_retriever(
    search_kwargs={"k": 3}
)

question = input("Ask: ")

docs = retriever.invoke(question)

context = "\n\n".join(
    doc.page_content for doc in docs
)

prompt = f"""
Answer the question using only the context below.

Context:
{context}

Question:
{question}

Answer:
"""

llm = OllamaLLM(
    model=LLM_MODEL
)

response = llm.invoke(prompt)

print("\nAnswer:\n")
print(response)