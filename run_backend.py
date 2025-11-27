"""
Script to run the FastAPI backend server
"""
import uvicorn
from backend.config.settings import settings

if __name__ == "__main__":
    print(f"Starting FastAPI backend on {settings.BACKEND_HOST}:{settings.BACKEND_PORT}")
    print(f"API Documentation: http://localhost:{settings.BACKEND_PORT}/docs")
    print(f"Health Check: http://localhost:{settings.BACKEND_PORT}/api/v1/health")
    
    uvicorn.run(
        "backend.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=True
    )
