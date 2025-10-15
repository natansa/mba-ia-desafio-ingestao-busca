import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

def ingest_pdf(llm_model):
    PDF_PATH = os.getenv("PDF_PATH")
    if not PDF_PATH:
        raise SystemExit("PDF_PATH is not set")

    if llm_model == "openai":
        for k in ("OPENAI_API_KEY", "DATABASE_URL","PG_VECTOR_COLLECTION_NAME"):
            if not os.getenv(k):
                raise RuntimeError(f"Environment variable {k} is not set")
    elif llm_model == "gemini":
        for k in ("GOOGLE_API_KEY", "DATABASE_URL","PG_VECTOR_COLLECTION_NAME"):
            if not os.getenv(k):
                raise RuntimeError(f"Environment variable {k} is not set")
    else:
        raise SystemExit("Invalid LLM model")

    current_dir = Path(__file__).parent
    pdf_path = current_dir / PDF_PATH
    if not pdf_path.exists():
        raise FileNotFoundError(f"File {pdf_path} not found")

    docs = PyPDFLoader(str(pdf_path)).load()
    if not docs:
        raise SystemExit("Failed to load documents")

    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150, 
        add_start_index=False).split_documents(docs)
    if not splits:
        raise SystemExit("Failed to split documents")

    documents = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in splits
    ]
    if not documents:
        raise SystemExit("Failed to create documents")

    ids = [f"doc-{i}" for i in range(len(documents))]
    if not ids:
        raise SystemExit("Failed to create ids from documents")

    if llm_model == "openai":
        embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))
    elif llm_model == "gemini":
        embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL"))
    else:
        raise SystemExit("Invalid LLM model")

    if not embeddings:
        raise SystemExit("Failed to create embeddings")

    vectorStore = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )
    if not vectorStore:
        raise SystemExit("Failed to create vector store")

    if not vectorStore.add_documents(documents=documents, ids=ids):
        raise SystemExit("Failed to add documents to vector store")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python ingest.py <openai|gemini>")
        sys.exit(1)
    ingest_pdf(llm_model=sys.argv[1])