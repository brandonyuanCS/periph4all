"""
Pydantic Models for API Request/Response
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum


# Enums for categorical data
class GripType(str, Enum):
    PALM = "palm"
    CLAW = "claw"
    FINGERTIP = "fingertip"
    HYBRID = "hybrid"


class HandSize(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class Genre(str, Enum):
    FPS = "fps"
    MOBA = "moba"
    MMO = "mmo"
    BATTLE_ROYALE = "battle_royale"
    GENERAL = "general"


# User Preferences
class UserPreferences(BaseModel):
    """User preferences for mouse recommendation"""
    hand_size: Optional[str] = Field(None, description="Hand size: exact dimensions (e.g., '19cm x 10cm') or small/medium/large")
    grip_type: Optional[str] = Field(None, description="palm, claw, fingertip, or hybrid")
    genre: Optional[str] = Field(None, description="fps, moba, mmo, battle_royale, or general")
    sensitivity: Optional[str] = Field(None, description="low, medium, high")
    budget_min: Optional[float] = Field(None, ge=0)
    budget_max: Optional[float] = Field(None, ge=0)
    weight_preference: Optional[str] = Field(None, description="light, medium, heavy")
    wireless_preference: Optional[bool] = None
    additional_notes: Optional[str] = None


# Mouse Information
class MouseInfo(BaseModel):
    """Mouse product information"""
    name: str
    brand: str
    price: Optional[float] = None
    weight: Optional[float] = None
    dpi_max: Optional[int] = None
    wireless: Optional[bool] = None
    shape: Optional[str] = None
    grip_compatibility: Optional[List[str]] = None
    sensor: Optional[str] = None
    url: Optional[str] = None


# Recommendation Response
class MouseRecommendation(BaseModel):
    """Single mouse recommendation with similarity score"""
    mouse: MouseInfo
    score: float = Field(..., ge=0, le=1, description="Similarity/match score")
    reasoning: Optional[str] = None


class RecommendationResponse(BaseModel):
    """Response containing top K mouse recommendations"""
    recommendations: List[MouseRecommendation]
    user_preferences: UserPreferences


# Chat Models
class ChatMessage(BaseModel):
    """Single chat message"""
    role: str = Field(..., pattern="^(user|assistant|system)$")
    content: str


class ChatRequest(BaseModel):
    """Chat request with conversation history"""
    messages: List[ChatMessage]
    user_preferences: Optional[UserPreferences] = None


class ChatResponse(BaseModel):
    """Chat response with assistant message and updated preferences"""
    message: ChatMessage
    updated_preferences: Optional[UserPreferences] = None
    ready_for_recommendation: bool = False
    question_type: Optional[str] = Field(None, description="Type of question being asked: hand_size, grip_type, genre, sensitivity, budget, weight_preference, wireless_preference")


# Visualization Models
class EmbeddingPoint(BaseModel):
    """2D point in embedding space"""
    x: float
    y: float
    mouse_name: str
    mouse_info: Optional[MouseInfo] = None


class VisualizationResponse(BaseModel):
    """Embedding visualization data"""
    mouse_points: List[EmbeddingPoint]
    user_point: Optional[EmbeddingPoint] = None
    recommended_points: Optional[List[EmbeddingPoint]] = None


# Recommendation Request
class RecommendationRequest(BaseModel):
    """Request for mouse recommendations"""
    user_preferences: UserPreferences
    include_reasoning: bool = True
    top_k: Optional[int] = Field(3, ge=1, le=10)


# Generic Response
class StatusResponse(BaseModel):
    """Generic status response"""
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None

# visualization stuff
class GraphEdge(BaseModel):
    """Similarity edge between two mice or user and a mouse"""
    source: str  # e.g., 'mouse-1' (original index) or 'user-preference'
    target: str  # e.g., 'mouse-2' (original index)
    similarity: float = Field(..., ge=0, le=1)

class ForceGraphResponse(BaseModel):
    """Response model for ForceGraph visualization, matching frontend expectation."""
    visualization: VisualizationResponse
    edges: List[GraphEdge] = Field(..., description="Edges between mouse nodes (similarity links)")
    user_edges: Optional[List[GraphEdge]] = Field(None, description="Edges between user node and mice")

