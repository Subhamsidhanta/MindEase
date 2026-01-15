"""
Crisis Detection Module - Responsible AI Safety Layer
Detects potential self-harm or crisis situations and provides appropriate support
"""

import re
from typing import Tuple

# Crisis keywords that require immediate safety response
CRISIS_KEYWORDS = [
    # Self-harm related
    "kill myself", "end my life", "want to die", "suicide", "suicidal",
    "self harm", "self-harm", "hurt myself", "cutting myself",
    "don't want to live", "no reason to live", "better off dead",
    "ending it all", "can't go on", "give up on life",
    "take my own life", "not worth living", "overdose",
    # Severe distress
    "nobody cares", "everyone hates me", "completely alone",
    "no hope left", "nothing matters anymore", "can't take it anymore"
]

# Emergency helplines (India-focused, add more as needed)
EMERGENCY_RESOURCES = """
🆘 **If you're in crisis, please reach out immediately:**

**India:**
- 🇮🇳 iCall: 9152987821
- 🇮🇳 Vandrevala Foundation: 1860-2662-345 (24/7)
- 🇮🇳 NIMHANS: 080-46110007
- 🇮🇳 Sneha India: 044-24640050

**International:**
- 🌍 International Association for Suicide Prevention: https://www.iasp.info/resources/Crisis_Centres/

**Immediate Steps:**
1. 📞 Call a trusted friend or family member right now
2. 🏥 Go to your nearest emergency room if you feel unsafe
3. 💬 Text or call any of the helplines above - they're trained to help

**Remember:** You are not alone. This moment will pass. Professional help is available 24/7.
"""

SUPPORTIVE_CRISIS_MESSAGE = """
💚 **I hear you, and I'm really glad you reached out.**

I want you to know that what you're feeling right now is temporary, even if it doesn't feel that way. You deserve support from trained professionals who can truly help.

**I'm an AI and not equipped to provide crisis support**, but real people are ready to help you right now.

{resources}

Would you like me to help you with some grounding exercises while you reach out to someone? 💙
"""


def detect_crisis(message: str) -> Tuple[bool, str]:
    """
    Detects if a message contains crisis-related content.
    
    Args:
        message: User's input message
        
    Returns:
        Tuple of (is_crisis: bool, response: str)
    """
    message_lower = message.lower()
    
    for keyword in CRISIS_KEYWORDS:
        if keyword in message_lower:
            return True, SUPPORTIVE_CRISIS_MESSAGE.format(resources=EMERGENCY_RESOURCES)
    
    return False, ""


def get_emergency_resources() -> str:
    """Returns formatted emergency resources."""
    return EMERGENCY_RESOURCES


def is_severe_distress(mood_type: str, intensity: int) -> bool:
    """
    Checks if user's mood indicates severe distress requiring extra care.
    
    Args:
        mood_type: Type of mood (Stressed, Sad, Anxious, Angry, Tired)
        intensity: Intensity level (1-10)
        
    Returns:
        Boolean indicating if severe distress is detected
    """
    # High intensity negative moods need extra attention
    severe_threshold = 8
    concerning_moods = ["Sad", "Anxious", "Stressed"]
    
    if intensity >= severe_threshold and mood_type in concerning_moods:
        return True
    
    return False


def get_gentle_checkin() -> str:
    """Returns a gentle check-in message for high-distress users."""
    return """
💙 **I notice you're going through a really tough time right now.**

Before we continue, I want to check in: Are you feeling safe right now?

If you're having any thoughts of hurting yourself, please know that support is available:
- 📞 iCall: 9152987821
- 📞 Vandrevala Foundation: 1860-2662-345 (24/7)

If you're safe and would like to continue with some coping exercises, I'm here for you. 💚
"""
