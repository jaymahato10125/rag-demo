import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore

# Load environment variables from .env file
load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_api_key:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

pdf_path = Path(__file__).parent / "data" / "sample.pdf"

# Load the PDF document using PyPDFLoader
loader = PyPDFLoader(str(pdf_path))
docs = loader.load()

# Split the document into smaller chunks using RecursiveCharacterTextSplitter
test_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
    )
chunks = test_splitter.split_documents(documents=docs)

#Embedding the chunks using OpenAIEmbeddings
embedding_model = OpenAIEmbeddings(
    model="openai/text-embedding-3-large",
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
)

# Create a Qdrant Vector Store
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    collection_name="sample_collection",
    url="http://localhost:6333"  # Qdrant server URL
)


print("Vector store created and documents embedded successfully.")
