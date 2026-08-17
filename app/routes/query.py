from fastapi import APIRouter
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
import os

from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()


router = APIRouter(
    prefix="/query",
    tags=["query"]
)

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if not openrouter_api_key:
    raise RuntimeError("OPENROUTER_API_KEY is not set")

#Embedding the chunks using OpenAIEmbeddings
embedding_model = OpenAIEmbeddings(
    model="openai/text-embedding-3-large",
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
)

openai_client = OpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
)

vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    collection_name="sample_collection",
    url="http://localhost:6333"  # Qdrant server URL
)

@router.post("/")
async def query(question: str):
    search_results = vector_db.similarity_search(query=question)
   # print(f"Search Result for the question '{question}': {search_results}")

    context = " ".join(
        [
            f"[Page {result.metadata.get('page_label', result.metadata.get('page', 'unknown'))}] "
            f"{result.page_content}"
            for result in search_results
        ]
    )

    system_prompt = """
    You are a helpful assistant that answers questions based on the context provided.
    If the context does not contain the answer, respond with "I don't know."

    Also include the page number of the context in your answer if applicable.
    Context: {context}
    """.format(context=context)

    response = openai_client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        max_tokens=200,
    )

    return {
        "question": question,
        "answer": response.choices[0].message.content,
        "sources": [
            {
                "page": result.metadata.get(
                    "page_label", result.metadata.get("page", "unknown")
                ),
                "content": result.page_content,
            }
            for result in search_results
        ],
    }
    
