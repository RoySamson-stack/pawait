from fastapi import APIRouter, HTTPException, Depends, Query, Path
from app.models import QueryRequest, QueryResponse
from app.services.llm_service import get_llm_service, LLMService
import uuid
from datetime import datetime
from typing import List, Optional
import traceback
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/qa",
    tags=["Question Answering"],
    responses={404: {"description": "Not found"}},
)

@router.post(
    "/query", 
    response_model=QueryResponse,
    summary="Process a query through LLM",
    description="Sends a natural language query to the configured LLM service and returns the response",
    response_description="The LLM response with query and timestamp information"
)
async def process_query(
    request: QueryRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    """
    Process a user query through the selected LLM service.
    
    The query is sent to the configured language model which generates
    a response based on its training and the input provided.
    """
    try:
        logger.info(f"Processing query: {request.query}")
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
        # Log the full traceback for debugging
        error_detail = f"Error processing query: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_detail)
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@router.get(
    "/health",
    summary="Health check",
    description="Endpoint to verify the API service is running properly",
    tags=["Status"]
)
async def health_check():
    """
    Health check endpoint to verify the service is operational.
    
    Returns the current status and timestamp.
    """
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}