"""
LLM Service
Handles conversation and preference extraction using OpenAI API
"""
import openai
import json
from typing import List, Optional
from app.models.schemas import ChatMessage, ChatResponse, UserPreferences
from app.core.config import settings
from app.core.prompts import CHAT_SYSTEM_PROMPT, FALLBACK_GREETING


class LLMService:
    """Handles LLM-powered chat interactions"""
    
    def __init__(self):
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client if API key is available"""
        if settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            self.client = openai
        else:
            print("Warning: OPENAI_API_KEY not set. LLM features will use fallback responses.")
    
    async def process_chat(self, messages: List[ChatMessage], 
                          current_preferences: Optional[UserPreferences] = None) -> ChatResponse:
        """
        Process chat message and extract/update user preferences
        
        If OpenAI API is not configured, uses rule-based fallback
        """
        if self.client and settings.OPENAI_API_KEY:
            return await self._process_chat_with_llm(messages, current_preferences)
        else:
            return await self._process_chat_fallback(messages, current_preferences)
    
    async def _process_chat_with_llm(self, messages: List[ChatMessage],
                                    current_preferences: Optional[UserPreferences]) -> ChatResponse:
        """Process chat using OpenAI LLM"""
        
        try:
            # Build message history
            chat_messages = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}]
            
            # Add context about current preferences if available
            if current_preferences:
                pref_summary = f"Current user preferences: {current_preferences.model_dump_json()}"
                chat_messages.append({"role": "system", "content": pref_summary})
            
            # Add conversation history
            for msg in messages:
                chat_messages.append({"role": msg.role, "content": msg.content})
            
            # Call OpenAI API
            response = await openai.ChatCompletion.acreate(
                model=settings.OPENAI_MODEL,
                messages=chat_messages,
                temperature=0.7,
                max_tokens=500
            )
            
            # Parse response
            response_content = response.choices[0].message.content
            parsed = json.loads(response_content)
            
            # Extract data
            message_text = parsed.get("message", "I'm here to help you find the perfect mouse!")
            prefs_dict = parsed.get("preferences", {})
            ready = parsed.get("ready_for_recommendation", False)
            
            # Create UserPreferences object
            updated_prefs = UserPreferences(**prefs_dict) if prefs_dict else current_preferences
            
            return ChatResponse(
                message=ChatMessage(role="assistant", content=message_text),
                updated_preferences=updated_prefs,
                ready_for_recommendation=ready
            )
            
        except Exception as e:
            print(f"LLM API error: {e}")
            # Fallback to rule-based on error
            return await self._process_chat_fallback(messages, current_preferences)
    
    async def _process_chat_fallback(self, messages: List[ChatMessage],
                                    current_preferences: Optional[UserPreferences]) -> ChatResponse:
        """
        Fallback chat processing without LLM
        Uses simple rule-based pattern matching
        """
        if not messages:
            return ChatResponse(
                message=ChatMessage(
                    role="assistant",
                    content=FALLBACK_GREETING
                ),
                updated_preferences=current_preferences,
                ready_for_recommendation=False
            )
        
        last_message = messages[-1].content.lower()
        prefs = current_preferences or UserPreferences()
        
        # Simple pattern matching for preferences
        if not prefs.hand_size:
            if "small" in last_message:
                prefs.hand_size = "small"
            elif "medium" in last_message or "med" in last_message:
                prefs.hand_size = "medium"
            elif "large" in last_message or "big" in last_message:
                prefs.hand_size = "large"
            
            if prefs.hand_size:
                response_text = f"Got it, {prefs.hand_size} hands. What's your grip style? (palm, claw, or fingertip)"
            else:
                response_text = "I didn't catch that. Is your hand size small, medium, or large?"
        
        elif not prefs.grip_type:
            if "palm" in last_message:
                prefs.grip_type = "palm"
            elif "claw" in last_message:
                prefs.grip_type = "claw"
            elif "fingertip" in last_message or "finger" in last_message:
                prefs.grip_type = "fingertip"
            
            if prefs.grip_type:
                response_text = f"{prefs.grip_type.capitalize()} grip noted! What games do you primarily play? (FPS, MOBA, MMO, Battle Royale, or General)"
            else:
                response_text = "What grip style do you use? (palm, claw, or fingertip)"
        
        elif not prefs.genre:
            if "fps" in last_message or "shooter" in last_message:
                prefs.genre = "fps"
            elif "moba" in last_message or "league" in last_message or "dota" in last_message:
                prefs.genre = "moba"
            elif "mmo" in last_message:
                prefs.genre = "mmo"
            elif "battle royale" in last_message or "fortnite" in last_message or "apex" in last_message:
                prefs.genre = "battle_royale"
            elif "general" in last_message or "everything" in last_message or "all" in last_message:
                prefs.genre = "general"
            
            if prefs.genre:
                response_text = f"Great! Do you prefer wireless or wired mice?"
            else:
                response_text = "What type of games do you play? (FPS, MOBA, MMO, Battle Royale, or General)"
        
        elif prefs.wireless_preference is None:
            if "wireless" in last_message:
                prefs.wireless_preference = True
            elif "wired" in last_message:
                prefs.wireless_preference = False
            
            if prefs.wireless_preference is not None:
                response_text = "Perfect! What's your budget range? (e.g., '$50 to $100' or 'under $80')"
            else:
                response_text = "Do you prefer wireless or wired?"
        
        elif not prefs.budget_max:
            # Try to extract budget
            import re
            numbers = re.findall(r'\$?(\d+)', last_message)
            if numbers:
                nums = [float(n) for n in numbers]
                if len(nums) == 1:
                    prefs.budget_max = nums[0]
                elif len(nums) >= 2:
                    prefs.budget_min = min(nums)
                    prefs.budget_max = max(nums)
                
                response_text = "Excellent! I have enough information to make some recommendations. Would you like to see them?"
            else:
                response_text = "What's your budget? (e.g., '$50 to $100' or 'under $80')"
        
        else:
            # Have enough preferences
            response_text = "I have all the information I need! Ready to see your personalized mouse recommendations?"
        
        # Check if we have enough preferences for recommendations
        ready = all([
            prefs.hand_size,
            prefs.grip_type,
            prefs.genre
        ])
        
        return ChatResponse(
            message=ChatMessage(role="assistant", content=response_text),
            updated_preferences=prefs,
            ready_for_recommendation=ready
        )

