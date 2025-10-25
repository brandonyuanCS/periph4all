"""
LLM Service
Handles conversation and preference extraction using Groq API
"""
from groq import Groq
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
        """Initialize Groq client if API key is available"""
        if settings.GROQ_API_KEY:
            self.client = Groq(api_key=settings.GROQ_API_KEY)
            print(f"Groq client initialized with model: {settings.GROQ_MODEL}")
        else:
            print("Warning: GROQ_API_KEY not set. LLM features will use fallback responses.")
    
    async def process_chat(self, messages: List[ChatMessage], 
                          current_preferences: Optional[UserPreferences] = None) -> ChatResponse:
        """
        Process chat message and extract/update user preferences
        
        If Groq API is not configured, uses rule-based fallback
        """
        if self.client and settings.GROQ_API_KEY:
            return await self._process_chat_with_llm(messages, current_preferences)
        else:
            return await self._process_chat_fallback(messages, current_preferences)
    
    # app/services/llm.py

    async def _process_chat_with_llm(self, messages: List[ChatMessage],
                                    current_preferences: Optional[UserPreferences]) -> ChatResponse:
        """Process chat using Groq LLM"""
        
        # Define preference lists and maps once for use in prompt and programmatic fix
        required_prefs = ['hand_size', 'grip_type', 'genre', 'sensitivity', 'budget_min', 'budget_max', 'weight_preference', 'wireless_preference']
        question_map = {
            'hand_size': "What's your hand size? (e.g., 19cm x 10cm or small/medium/large)",
            'grip_type': "What's your preferred grip type? (palm, claw, fingertip, or hybrid)",
            'genre': "What games do you mainly play? (fps, moba, mmo, battle_royale, or general)",
            'sensitivity': "What's your preferred mouse sensitivity? (low, medium, or high)",
            'budget_min': "What's your budget range for a gaming mouse? (e.g., $50 to $100)",
            'budget_max': "What's your budget range for a gaming mouse? (e.g., $50 to $100)",
            'weight_preference': "Is your preferred mouse weight light (<65g), medium (65-85g), or heavy (>85g)?",
            'wireless_preference': "Do you prefer wired or wireless connection?"
        }
        
        # --- NEW: Variable to hold the question type being asked ---
        next_question_type = None
        # -----------------------------------------------------------

        try:
            # Build message history
            chat_messages = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}]
            
            # Add context about current preferences if available
            if current_preferences:
                collected = current_preferences.model_dump(exclude_none=True)
                if collected:
                    pref_list = "\n".join([f"- {key}: {value}" for key, value in collected.items()])
                    
                    # Determine what to ask next
                    missing = [p for p in required_prefs if p not in collected or collected[p] is None]
                    
                    next_question_hint = ""
                    if missing:
                        next_pref = missing[0]
                        # --- NEW: Set the question type based on missing preference ---
                        next_question_type = next_pref 
                        # -------------------------------------------------------------
                        next_question_hint = f"\n\nNEXT QUESTION TO ASK: {question_map.get(next_pref, 'Continue asking about preferences')}"
                    
                    pref_summary = f"ALREADY COLLECTED PREFERENCES (DO NOT change or override these):\n{pref_list}\n\nOnly ask about preferences that are NOT listed above.{next_question_hint}"
                    chat_messages.append({"role": "system", "content": pref_summary})
            
            # Add conversation history
            for msg in messages:
                chat_messages.append({"role": msg.role, "content": msg.content})
            
            # Call Groq API (omitted for brevity)
            response = self.client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=chat_messages,
                temperature=0.5,
                max_tokens=500,
                response_format={"type": "json_object"}
            )
            
            # Parse response
            response_content = response.choices[0].message.content
            parsed = json.loads(response_content)
            
            # Extract data
            message_text = parsed.get("message", "I'm here to help you find the perfect mouse!")
            prefs_dict = parsed.get("preferences", {})
            ready = parsed.get("ready_for_recommendation", False)
            
            # --- START FIX: Programmatic enforcement of next question (including next_question_type update) ---
            # Calculate updated 'missing' list based on the new LLM output
            all_prefs = {}
            if current_preferences:
                all_prefs.update(current_preferences.model_dump(exclude_none=True))
            # New preferences from LLM response
            all_prefs.update({k: v for k, v in prefs_dict.items() if v is not None}) 
            
            missing_after_update = [p for p in required_prefs if all_prefs.get(p) is None]
            
            # Reset next_question_type if we're ready
            if ready:
                next_question_type = None
            
            if not ready and missing_after_update:
                next_pref = missing_after_update[0]
                # --- NEW: Update the question type after the most recent preference extraction ---
                next_question_type = next_pref 
                # ---------------------------------------------------------------------------------
                next_question = question_map.get(next_pref)
                
                # Enforce question in message_text (omitted internal logic for brevity)
                if next_question and '?' not in message_text:
                    separator = " "
                    message_text_stripped = message_text.strip()
                    if message_text_stripped:
                        last_char = message_text_stripped[-1]
                        if last_char not in ['.', '!', '?']:
                            separator = "! "
                        elif last_char == '.':
                            separator = " "
                        
                        message_text = f"{message_text_stripped}{separator}{next_question}"
                    else:
                        message_text = next_question
            
            # --- END FIX ---

            # Create UserPreferences object, merging with current preferences (omitted for brevity)
            if current_preferences:
                updated_prefs_dict = current_preferences.model_dump(exclude_none=True)
                for key, value in prefs_dict.items():
                    if value is not None:
                        updated_prefs_dict[key] = value
                updated_prefs = UserPreferences(**updated_prefs_dict)
            else:
                updated_prefs = UserPreferences(**prefs_dict) if prefs_dict else None
            
            return ChatResponse(
                message=ChatMessage(role="assistant", content=message_text),
                updated_preferences=updated_prefs,
                ready_for_recommendation=ready,
                # --- CRITICAL FIX: Pass the determined question type here ---
                question_type=next_question_type 
                # -----------------------------------------------------------
            )
            
        except Exception as e:
            # Error handling (omitted for brevity)
            print(f"Groq API error: {e}")
            import traceback
            traceback.print_exc()
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
                ready_for_recommendation=False,
                question_type="hand_size"
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
        
        # Determine next question type
        question_type = None
        if not ready:
            if not prefs.hand_size:
                question_type = "hand_size"
            elif not prefs.grip_type:
                question_type = "grip_type"
            elif not prefs.genre:
                question_type = "genre"
            elif not prefs.sensitivity:
                question_type = "sensitivity"
            elif not prefs.budget_min and not prefs.budget_max:
                question_type = "budget"
            elif not prefs.weight_preference:
                question_type = "weight_preference"
            elif prefs.wireless_preference is None:
                question_type = "wireless_preference"
        
        return ChatResponse(
            message=ChatMessage(role="assistant", content=response_text),
            updated_preferences=prefs,
            ready_for_recommendation=ready,
            question_type=question_type
        )

