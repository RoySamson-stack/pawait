from fastapi import APIRouter, HTTPException, Depends
from app.models import QueryRequest, QueryResponse
from app.services.llm_service import get_llm_service, LLMService
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def process_query(
    request: QueryRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    """
    Process a user query through the selected LLM service
    """
    try:
        # Get response from LLM
        response_text = await llm_service.generate_response(request.query)
        
        # Create response object
        response = QueryResponse(
            query=request.query,
            response=response_text,
            timestamp=datetime.now()
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}