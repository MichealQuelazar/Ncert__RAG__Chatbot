"""
FastAPI backend application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config.settings import settings
from backend.api import routes
from backend.services.vector_db_service import VectorDBService
from backend.services.qa_service import QAService

# Initialize FastAPI app
app = FastAPI(
    title="NCERT Q&A API",
    description="Question-Answering system for NCERT Physics textbooks",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
vector_db_service = VectorDBService(
    vector_db_path=settings.VECTOR_DB_PATH,
    embedding_model=settings.EMBEDDING_MODEL,
    groq_api_key=settings.GROQ_API_KEY,
    llm_model=settings.LLM_MODEL,
    retrieval_k=settings.RETRIEVAL_K
)

qa_service = QAService(
    vector_db_service=vector_db_service,
    groq_api_key=settings.GROQ_API_KEY,
    llm_model=settings.LLM_MODEL
)

# Set the QA service in routes
routes.set_qa_service(qa_service)

# Include routers
app.include_router(routes.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("Starting NCERT Q&A API...")
    print(f"Loading vector database from: {settings.VECTOR_DB_PATH}")
    
    if vector_db_service.load_vector_db():
        vector_db_service.setup_compression_retriever()
        print("✓ Services initialized successfully")
    else:
        print("✗ Warning: Vector database could not be loaded")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("Shutting down NCERT Q&A API...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=True
    )
