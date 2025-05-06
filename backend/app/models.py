from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class QueryRequest(BaseModel):
    query: str = Field(..., description="The user's question")

class QueryResponse(BaseModel):
    query: str = Field(..., description="The original query")
    response: str = Field(..., description="The LLM's response")
    timestamp: datetime = Field(default_factory=datetime.now, description="When the response was generated")

class ConversationItem(BaseModel):
    id: str = Field(..., description="Unique identifier for this conversation item")
    query: str = Field(..., description="The user's question")
    response: str = Field(..., description="The LLM's response")
    timestamp: datetime = Field(..., description="When the response was generated")

class ConversationHistory(BaseModel):
    items: List[ConversationItem] = Field(default_factory=list, description="List of conversation items")