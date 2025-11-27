"""
API routes for the FastAPI backend
"""
from fastapi import APIRouter, HTTPException
from backend.api.models import QueryRequest, QueryResponse, HealthResponse
from backend.services.qa_service import QAService

router = APIRouter()

# This will be injected by the main app
qa_service: QAService = None

def set_qa_service(service: QAService):
    global qa_service
    qa_service = service

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    if qa_service is None:
        return HealthResponse(
            status="error",
            message="QA service not initialized",
            vector_db_loaded=False
        )
    
    is_ready = qa_service.vector_db_service.is_ready()
    return HealthResponse(
        status="healthy" if is_ready else "degraded",
        message="Service is running" if is_ready else "Vector database not loaded",
        vector_db_loaded=is_ready
    )

@router.post("/ask", response_model=QueryResponse)
async def ask_question(query: QueryRequest):
    """
    Ask a question and get an answer based on the document corpus
    """
    if qa_service is None:
        raise HTTPException(status_code=503, detail="QA service not initialized")
    
    if not qa_service.vector_db_service.is_ready():
        raise HTTPException(status_code=503, detail="Vector database not ready")
    
    try:
        result = qa_service.generate_answer(query.question)
        return QueryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "NCERT Q&A API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "ask": "/ask (POST)",
            "docs": "/docs"
        }
    }
