# PDF RAG Indexer

This project loads a local PDF, splits it into chunks, creates embeddings through OpenRouter, and stores the vectors in a local Qdrant database.

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

## Run

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

Stop Qdrant when finished:

```bash
docker compose down
```

## Project structure

```text
.
├── app/
│   ├── data/          # Local PDFs; ignored by Git
│   └── index.py       # PDF loading, chunking, embedding, and indexing
├── docker-compose.yml # Local Qdrant service
├── requirements.txt   # Python dependencies
└── .env               # Local API key; ignored by Git
```

## Current scope

The project currently handles document ingestion and vector storage. A search or question-answering endpoint has not been added yet.
