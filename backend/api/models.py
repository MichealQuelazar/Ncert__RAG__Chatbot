"""
Pydantic models for API request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=1, description="The question to ask")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "What is Newton's first law of motion?"
            }
        }

class DocumentInfo(BaseModel):
    page: str = Field(..., description="Page number where the content was found")
    link: str = Field(..., description="Source document path")
    snippet: str = Field(..., description="Relevant text snippet")

class QueryResponse(BaseModel):
    answer: str = Field(..., description="Generated answer to the question")
    retrieved_documents: List[DocumentInfo] = Field(..., description="List of retrieved documents")
    
class HealthResponse(BaseModel):
    status: str
    message: str
    vector_db_loaded: bool
