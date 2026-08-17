# PDF RAG API

This project loads a local PDF, splits it into chunks, creates embeddings through OpenRouter, stores the vectors in Qdrant, and exposes a question-answering API.

## Requirements

- Python 3
- Docker and Docker Compose
- An [OpenRouter API key](https://openrouter.ai/keys)

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
```

Place the PDF to index at:

```text
app/data/sample.pdf
```

The local data directory is ignored by Git.

## Index the PDF

Start Qdrant:

```bash
docker compose up -d
```

Run the indexer:

```bash
python -m app.index
```

The script uses the `openai/text-embedding-3-large` embedding model through OpenRouter and stores vectors in the `sample_collection` collection at `http://localhost:6333`.

When indexing finishes, the script prints:

```text
Vector store created and documents embedded successfully.
```

## Start the API

Run the API from the `app` directory:

```bash
cd app
uvicorn main:app --reload
```

The API and interactive Swagger documentation are available at:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`

The `/query/` endpoint accepts a question as a query parameter:

```bash
curl -X POST \
  'http://127.0.0.1:8000/query/?question=What are the phases of the Node.js event loop?' \
  -H 'accept: application/json'
```

The endpoint searches the indexed document, sends the retrieved context to the `openai/gpt-4o-mini` model through OpenRouter, and returns an answer with source pages:

```json
{
  "question": "What are the phases of the Node.js event loop?",
  "answer": "...",
  "sources": [
    {
      "page": "2",
      "content": "..."
    }
  ]
}
```

## Project structure

```text
.
├── app/
│   ├── data/          # Local PDFs; ignored by Git
│   ├── index.py       # PDF loading, chunking, embedding, and indexing
│   ├── main.py        # FastAPI application
│   └── routes/
│       └── query.py   # Retrieval and question-answering endpoint
├── docker-compose.yml # Local Qdrant service
├── requirements.txt   # Python dependencies
└── .env               # Local API key; ignored by Git
```

## Models and services

- Embeddings: `openai/text-embedding-3-large` through OpenRouter
- Answer generation: `openai/gpt-4o-mini` through OpenRouter
- Vector database: Qdrant at `http://localhost:6333`

Run the indexing step before starting a query, otherwise the `sample_collection` collection will not exist.

When you are finished, stop Qdrant:

```bash
docker compose down
```
