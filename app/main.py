from fastapi import FastAPI
from routes.query import router as query_router

app = FastAPI(
    title="RAG API",
    description="A simple RAG API.",
    version="0.1.0"
)

app.include_router(query_router) 
