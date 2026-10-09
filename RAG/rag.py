import re
import uuid
from typing import List

import chromadb
from pypdf import PdfReader
from rank_bm25 import BM25Okapi

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama


# ==========================================================
# CONFIG
# ==========================================================

PDF_PATH = "data/sample.pdf"

EMBED_MODEL = "nomic-embed-text"
LLM_MODEL = "phi3"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

TOP_K_VECTOR = 5
TOP_K_BM25 = 5
TOP_K_FINAL = 5


# ==========================================================
# STEP 1: LOAD PDF
# ==========================================================

def load_pdf(path: str) -> str:
    reader = PdfReader(path)

    pages = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


# ==========================================================
# STEP 2: CLEAN TEXT
# ==========================================================

def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[^\S\r\n]+", " ", text)

    return text.strip()


# ==========================================================
# STEP 3: CHUNKING
# ==========================================================

def chunk_text(text: str) -> List[str]:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ".", " ", ""]
    )

    return splitter.split_text(text)


# ==========================================================
# STEP 4: EMBEDDINGS
# ==========================================================

embedding_model = OllamaEmbeddings(
    model=EMBED_MODEL
)


# ==========================================================
# STEP 5: CHROMADB
# ==========================================================

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="hybrid_rag_demo"
)


def build_vector_store(chunks: List[str]):

    existing = collection.count()

    if existing > 0:
        print("Vector DB already exists.")
        return

    embeddings = embedding_model.embed_documents(chunks)

    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB.")


# ==========================================================
# STEP 6: BM25 INDEX
# ==========================================================

def build_bm25(chunks: List[str]):

    tokenized = [chunk.lower().split() for chunk in chunks]

    return BM25Okapi(tokenized)


# ==========================================================
# STEP 7: VECTOR SEARCH
# ==========================================================

def vector_search(query: str):

    query_embedding = embedding_model.embed_query(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K_VECTOR
    )

    return results["documents"][0]


# ==========================================================
# STEP 8: BM25 SEARCH
# ==========================================================

def bm25_search(query: str, bm25, chunks):

    tokens = query.lower().split()

    scores = bm25.get_scores(tokens)

    ranked = sorted(
        zip(chunks, scores),
        key=lambda x: x[1],
        reverse=True
    )

    return [doc for doc, _ in ranked[:TOP_K_BM25]]


# ==========================================================
# STEP 9: RECIPROCAL RANK FUSION (RRF)
# ==========================================================

def reciprocal_rank_fusion(results, k=60):

    fused = {}

    for docs in results:

        for rank, doc in enumerate(docs):

            fused[doc] = fused.get(doc, 0) + 1 / (k + rank + 1)

    ranked = sorted(
        fused.items(),
        key=lambda x: x[1],
        reverse=True
    )

    return [doc for doc, _ in ranked[:TOP_K_FINAL]]


# ==========================================================
# STEP 10: GENERATION
# ==========================================================

llm = ChatOllama(
    model=LLM_MODEL,
    temperature=0
)


def generate_answer(query: str, context_docs: List[str]):

    context = "\n\n".join(context_docs)

    prompt = f"""
You are a helpful RAG assistant.

Answer ONLY from the provided context.

If the answer is not available, say:
"I could not find that information in the documents."

Context:
{context}

Question:
{query}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("Loading PDF...")
    raw_text = load_pdf(PDF_PATH)

    print("Cleaning text...")
    cleaned_text = clean_text(raw_text)

    print("Chunking...")
    chunks = chunk_text(cleaned_text)

    print(f"Total chunks: {len(chunks)}")

    print("Building vector store...")
    build_vector_store(chunks)

    print("Building BM25 index...")
    bm25 = build_bm25(chunks)

    print("\nHybrid RAG ready.\n")

    while True:

        query = input("Question: ")

        if query.lower() in ["exit", "quit"]:
            break

        vector_results = vector_search(query)

        bm25_results = bm25_search(
            query,
            bm25,
            chunks
        )

        final_context = reciprocal_rank_fusion(
            [vector_results, bm25_results]
        )

        answer = generate_answer(
            query,
            final_context
        )

        print("\n" + "=" * 80)
        print(answer)
        print("=" * 80 + "\n")


if __name__ == "__main__":
    main()