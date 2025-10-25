"""
Chat Endpoint
Handles conversational interactions with users to collect preferences
"""
from fastapi import APIRouter, Depends, HTTPException
from app.models.schemas import ChatRequest, ChatResponse, ChatMessage
from app.services.llm import LLMService
from app.api.deps import get_llm_service

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    llm_service: LLMService = Depends(get_llm_service)
):
    """
    Process chat message and extract user preferences
    
    The LLM will:
    - Engage in natural conversation
    - Ask clarifying questions about preferences
    - Extract structured preference data
    - Determine when enough info is collected for recommendations
    """
    try:
        response = await llm_service.process_chat(
            messages=request.messages,
            current_preferences=request.user_preferences
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")


@router.post("/reset")
async def reset_chat():
    """Reset conversation state"""
    return {
        "status": "success",
        "message": "Chat conversation reset"
    }

