"""
AI Chatbot Module
Contains the AI brain for generating mental wellness responses
Supports multiple AI backends with rule-based fallback
"""

import os
import random
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import AI libraries
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# System prompt for the AI
SYSTEM_PROMPT = """You are MindEase, a warm and genuinely caring AI mental wellness companion.

CORE APPROACH - Always follow this structure:
1. VALIDATE - "I hear you" / "That sounds really hard" / "Your feelings make sense"
2. NORMALIZE - "You're not alone" / "Many people feel this way"
3. HOPE - "This won't last forever" / "Things can get better"
4. ACTION - Give 2-3 SPECIFIC, SIMPLE things they can try RIGHT NOW

BE SPECIFIC, NOT VAGUE:
❌ BAD: "Try to relax" "Think positive" "It'll be okay"
✅ GOOD: "Take 5 deep breaths - in for 4, out for 6" "Text one friend right now" "Go outside for 2 minutes"

For SADNESS:
- Acknowledge their pain genuinely
- Suggest: calling someone, gentle movement (5-min walk), one small comfort (tea, blanket, favorite song)
- Remind them: feelings are temporary, rest isn't weakness, tiny wins count
- If intense (8-10/10): urge them to not be alone, call helpline if needed

For ANXIETY:
- Ground them: 5-4-3-2-1 senses, feet on floor, cold water on face
- Challenge worries: "Is this thought a fact or a fear?"
- Breathing: 4-7-8 technique
- If severe: cold shock therapy, call for support

For STRESS:
- Help prioritize: what MUST happen vs what can wait
- Suggest boundaries: what to say no to, who can help
- Break tasks into micro-steps
- Immediate: 10 deep breaths, drop shoulders, unclench jaw

TONE:
- Warm friend, not clinical doctor
- Specific actions, not platitudes
- Under 150 words but genuinely helpful
- Light emojis for warmth (💙 🌸) but don't overdo

CRISIS RESPONSE:
If self-harm/suicide mentioned: "I'm really worried. Your life matters. Please call iCall (9152987821) or Vandrevala (1860-2662-345) RIGHT NOW or go to ER. I care about you."

NEVER: diagnose, prescribe, minimize pain, give vague advice

ONE good specific suggestion beats ten vague platitudes."""


class MindEaseAI:
    """AI chatbot for mental wellness support."""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.0-flash"):
        """
        Initialize the AI chatbot.
        
        Args:
            api_key: API key for the AI service (or set GOOGLE_API_KEY env var)
            model_name: Name of the model to use
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model_name = model_name
        self.model = None
        self.chat = None
        self.using_ai = False
        
        self._init_ai()
    
    def _init_ai(self):
        """Initialize the AI model."""
        if GEMINI_AVAILABLE and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(
                    model_name=self.model_name,
                    system_instruction=SYSTEM_PROMPT
                )
                self.chat = self.model.start_chat(history=[])
                self.using_ai = True
                print("✅ Gemini AI initialized successfully")
            except Exception as e:
                print(f"⚠️ Gemini initialization failed: {e}")
                self.using_ai = False
        else:
            if not GEMINI_AVAILABLE:
                print("⚠️ Gemini not available. Using rule-based responses.")
            elif not self.api_key:
                print("⚠️ No API key provided. Using rule-based responses.")
            self.using_ai = False
    
    def generate_response(self, user_message: str, mood: Optional[str] = None, 
                         intensity: Optional[int] = None) -> str:
        """
        Generate a response to the user's message.
        
        Args:
            user_message: The user's input message
            mood: Current mood type if known
            intensity: Mood intensity (1-10) if known
        
        Returns:
            Bot response string
        """
        # Add context if mood info is available
        context = ""
        if mood and intensity:
            context = f"[User's current mood: {mood}, Intensity: {intensity}/10] "
        
        full_message = context + user_message
        
        if self.using_ai:
            try:
                response = self.chat.send_message(full_message)
                return response.text
            except Exception as e:
                print(f"AI response error: {e}")
                return self._fallback_response(user_message, mood, intensity)
        else:
            return self._fallback_response(user_message, mood, intensity)
    
    def _fallback_response(self, message: str, mood: Optional[str] = None,
                          intensity: Optional[int] = None) -> str:
        """Generate rule-based fallback response."""
        message_lower = message.lower()
        
        # Check for greetings first
        if any(word in message_lower for word in ["hello", "hi", "hey", "hii"]) and len(message_lower) < 10:
            return self._get_greeting_response()
        
        # Check for help requests
        if any(word in message_lower for word in ["help me", "help", "i need help", "what do i do"]):
            return self._get_help_response(mood, intensity)
        
        # Check for thanks
        if any(word in message_lower for word in ["thank", "thanks", "helpful"]):
            return self._get_gratitude_response()
        
        # Keyword-based responses (prioritize over mood)
        if any(word in message_lower for word in ["stress", "stressed", "overwhelming"]):
            return self._get_stress_response()
        
        if any(word in message_lower for word in ["anxious", "anxiety", "worried", "worry", "panic"]):
            return self._get_anxiety_response()
        
        if any(word in message_lower for word in ["sad", "depressed", "down", "low", "unhappy", "miserable"]):
            return self._get_sadness_response()
        
        if any(word in message_lower for word in ["angry", "anger", "frustrated", "mad", "furious"]):
            return self._get_anger_response()
        
        if any(word in message_lower for word in ["tired", "exhausted", "sleep", "rest", "fatigue"]):
            return self._get_tiredness_response()
        
        if any(word in message_lower for word in ["breath", "breathing", "calm"]):
            return self._get_breathing_response()
        
        # Use mood context only if message is very short or unclear
        if mood and len(message_lower) < 20:
            return self._get_mood_response(mood, intensity or 5)
        
        # Default supportive response
        return self._get_default_response()
    
    def _get_mood_response(self, mood: str, intensity: int) -> str:
        """Get response based on mood type and intensity."""
        responses = {
            "Stressed": [
                f"I hear you - stress at level {intensity}/10 is really heavy. 💙 Let's take this one step at a time. First, I want you to take a slow, deep breath with me. In through your nose... out through your mouth. Your nervous system will thank you.",
                f"Stress level {intensity}/10 - that's a lot to carry. You're doing your best, and that matters. 🌿 Would you like to try a quick grounding exercise, or would talking about what's bothering you help more?",
            ],
            "Anxious": [
                f"Anxiety at {intensity}/10 can feel so overwhelming. I want you to know: this feeling will pass. 💙 Right now, can you feel your feet on the ground? You're safe in this moment.",
                f"I understand - anxiety at level {intensity} is really tough. Remember: you've gotten through anxious moments before, and you'll get through this one too. Let's try some grounding together.",
            ],
            "Sad": [
                f"Sadness at level {intensity}/10... I'm here with you. 💜 It's okay to feel this way. Your feelings are valid, and you don't have to push them away. Would you like to talk about it, or try something gentle together?",
                f"I'm sorry you're feeling sad ({intensity}/10). Sometimes we need to sit with these feelings. 🌸 Be gentle with yourself today. What's one small kind thing you could do for yourself right now?",
            ],
            "Angry": [
                f"Anger at {intensity}/10 - that's intense energy in your body. 🔥 This feeling is valid. Let's channel it safely. Can you try shaking out your hands for 10 seconds, then take 3 slow breaths?",
                f"I hear you - level {intensity} anger needs attention. Your feelings are trying to tell you something important. 💪 Before we explore that, let's release some of this tension from your body.",
            ],
            "Tired": [
                f"Tiredness at level {intensity}/10... your body and mind need care. 😴 Rest isn't lazy - it's necessary. If you can, step away from screens for a bit. What would gentle rest look like for you right now?",
                f"Feeling this tired ({intensity}/10) is your body sending a message. 🌙 Please be kind to yourself. Can you take a 5-minute break? Sometimes that's the first step to feeling better.",
            ],
        }
        
        mood_responses = responses.get(mood, responses["Stressed"])
        return random.choice(mood_responses)
    
    def _get_stress_response(self) -> str:
        responses = [
            """I can hear that you're stressed, and that's a lot to carry. 💙 Let's bring it down a notch.

**Do this RIGHT NOW:**
1. Take 10 slow breaths - in for 4, out for 6
2. Write down everything bothering you
3. Circle the ONE thing you'll tackle next

You don't have to fix everything at once. One step at a time. What's stressing you most?""",
            """Stress at this level isn't sustainable. Let's lighten the load. 🌿

**Quick relief:**
1. **Drop something** - what can honestly wait or be skipped?
2. **Ask for help** - who can take one thing off your plate?
3. **Set a boundary** - what do you need to say no to?

Your best is good enough. What's the biggest pressure right now?""",
        ]
        return random.choice(responses)
    
    def _get_anxiety_response(self) -> str:
        responses = [
            """Anxiety can make everything feel urgent and scary. Let me help you come back to now. 💙

**Ground yourself (do this):**
1. Feel your feet on the floor - press them down
2. Name 5 things you can see around you
3. Take 3 slow breaths - in for 4, out for 6

You're safe right now, in this moment. Anxiety is lying to you. What are you most worried about?""",
            """I hear the anxiety is really loud right now. Let's quiet your nervous system. 🌊

**Try this immediately:**
1. Splash cold water on your face (this literally calms your nerves)
2. Put both hands over your heart, breathe slowly
3. Say out loud: "I am safe. This will pass."

Anxiety peaks and then it falls. You've survived every anxious moment before this. What triggered this?""",
        ]
        return random.choice(responses)
    
    def _get_sadness_response(self) -> str:
        responses = [
            """I'm really sorry you're feeling sad. That heaviness in your chest is real, and you don't have to pretend it's not there. 💙

Here's what might actually help:
1. **Call or text someone** - even just "feeling down, could use company"
2. **Move gently** - 5-minute walk, even around your room
3. **One comfort** - soft blanket, warm drink, favorite song

Sadness doesn't last forever, even when it feels endless. What's weighing on your heart?""",
            """Your sadness is valid, and I'm here with you. 🌸 Sometimes we just need to let ourselves feel it.

Try this:
1. **Don't isolate** - reach out to one person who cares
2. **Tiny win** - take a shower, make your bed - something small
3. **Be kind to yourself** - would you judge a friend for feeling this way?

You're not broken. You're human. Want to talk about what's causing this?""",
        ]
        return random.choice(responses)
    
    def _get_help_response(self, mood: Optional[str] = None, intensity: Optional[int] = None) -> str:
        """Response when user asks for help."""
        if mood and intensity and intensity >= 8:
            mood_context = f"I know you're feeling {mood.lower()} at a really intense level ({intensity}/10). "
        elif mood:
            mood_context = f"I know you're feeling {mood.lower()} right now. "
        else:
            mood_context = ""
        
        return f"""{mood_context}I'm here to help you. 💙

**Here's what I can do right now:**

1. **Talk you through it** - tell me what's happening and I'll listen
2. **Breathing exercise** - calm your nervous system (click "🌬️ Breathe" below)
3. **Grounding technique** - bring you back to the present (click "🌍 Ground")
4. **Journaling prompts** - help you process your thoughts

**If this is urgent or you're in crisis:**
- iCall: 9152987821
- Vandrevala Foundation: 1860-2662-345 (24/7)

What would help most? You can tell me more about what's going on, or try one of the exercises."""
    
    def _get_anger_response(self) -> str:
        responses = [
            "Anger often shows us where our boundaries are. Your feelings are valid. 💪 Try this: shake your hands out for 10 seconds, then take 3 deep breaths. This can help release some of that intense energy.",
            "I hear your frustration. 🔥 Anger needs healthy outlets. If you can, try walking around for a minute or doing some jumping jacks. Physical movement can help process these feelings.",
        ]
        return random.choice(responses)
    
    def _get_tiredness_response(self) -> str:
        responses = [
            "Rest is not a luxury - it's a need. 😴 Your tiredness is telling you something important. Can you take a short break? Even 5 minutes of closing your eyes can help.",
            "Feeling tired is your body asking for care. 🌙 Please be kind to yourself. If you can, step away from screens for a bit. Hydrate, take a breath, and know it's okay to rest.",
        ]
        return random.choice(responses)
    
    def _get_breathing_response(self) -> str:
        return """Let's try the 4-7-8 breathing technique together. 🌬️

1. Exhale completely through your mouth
2. Inhale through your nose for **4 seconds**
3. Hold your breath for **7 seconds**
4. Exhale through your mouth for **8 seconds**

Repeat 3-4 times. This activates your body's relaxation response. 💙"""
    
    def _get_greeting_response(self) -> str:
        responses = [
            "Hello! I'm MindEase, your mental wellness companion. 💚 I'm here to listen, offer support, and share helpful coping techniques. How are you feeling today?",
            "Hi there! 🌸 Welcome to MindEase. I'm here to support your mental wellbeing. There's no judgment here - just a safe space. What's on your mind?",
        ]
        return random.choice(responses)
    
    def _get_gratitude_response(self) -> str:
        responses = [
            "You're so welcome! 💚 I'm always here when you need support. Remember to be kind to yourself today.",
            "I'm glad I could help! 🌸 Taking care of your mental health takes courage. I'm proud of you for reaching out.",
        ]
        return random.choice(responses)
    
    def _get_default_response(self) -> str:
        responses = [
            """I'm here to listen and support you. 💙

Tell me more about what's on your mind. Or if you'd prefer:
- Try a **breathing exercise** (helps calm your nervous system)
- Do a **mood check-in** (sidebar) to get personalized support
- Get **journaling prompts** to process your thoughts

What would help you most right now?""",
            """Thank you for reaching out. That takes courage. 🌸

I'm here for you. Would you like to:
1. **Talk about** what you're feeling
2. **Try** a grounding or breathing exercise
3. **Get** specific coping strategies

There's no judgment here - just support. What do you need?""",
        ]
        return random.choice(responses)
    
    def reset_conversation(self):
        """Reset the conversation history."""
        if self.model:
            self.chat = self.model.start_chat(history=[])
    
    def is_ai_available(self) -> bool:
        """Check if AI is available."""
        return self.using_ai
    
    def get_status(self) -> dict:
        """Get status of the AI module."""
        return {
            "ai_available": self.using_ai,
            "model": self.model_name if self.using_ai else "Rule-based Fallback",
            "provider": "Google Gemini" if self.using_ai else "Local"
        }
