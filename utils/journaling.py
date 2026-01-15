"""
Journaling Prompts Module
Provides thoughtful journaling prompts for mental wellness
"""

import random
from typing import List, Dict

# ============= JOURNALING PROMPTS BY CATEGORY =============

SELF_REFLECTION_PROMPTS = [
    "What triggered this feeling today? Can you trace it back to a specific moment?",
    "What's one small win you had today, no matter how tiny?",
    "What can you control right now in this situation?",
    "If your best friend was feeling this way, what would you tell them?",
    "What does your body need right now? Rest, movement, nourishment?",
    "What are three things that went well today?",
    "What's one thing you're grateful for in this moment?",
    "How would you describe your current emotional state in one word? Why that word?",
    "What's weighing on your mind the most right now?",
    "What would make tomorrow 1% better than today?"
]

STRESS_RELIEF_PROMPTS = [
    "List 5 things causing you stress. Now circle the ONE you can address today.",
    "What's the worst-case scenario you're imagining? How likely is it really?",
    "What would you do with this time if you weren't stressed?",
    "Who in your life helps you feel calm? Can you reach out to them?",
    "What's one boundary you need to set to protect your peace?",
    "If this stress was a weather pattern, what would it be? How long do storms usually last?",
    "What self-care have you been neglecting lately?",
    "Write down your to-do list. Now cross off 3 things that aren't truly essential.",
    "What's one thing you can delegate or ask for help with?",
    "Describe a time you got through something hard. What helped you then?"
]

ANXIETY_PROMPTS = [
    "What's the thought that keeps repeating in your mind? Write it down.",
    "Is this thought a fact or an assumption? What evidence do you have?",
    "What's the best possible outcome of this situation?",
    "Fast forward one year - how much will this matter?",
    "What would your wisest self say about this situation?",
    "Name 5 things in your immediate environment that are safe and steady.",
    "What's one small action you can take in the next 5 minutes?",
    "Who can you talk to about what you're feeling?",
    "What has helped you manage anxiety in the past?",
    "Write a letter to your anxiety. What do you want to say to it?"
]

SADNESS_PROMPTS = [
    "It's okay to feel sad. What do you need to hear right now?",
    "What memory brings you a sense of warmth or comfort?",
    "Who or what are you grieving? Give yourself permission to feel it.",
    "What's one kind thing you can do for yourself today?",
    "If tears could talk, what would yours say?",
    "Write about a time you felt genuinely happy. What made it special?",
    "What small pleasure could you give yourself in the next hour?",
    "Who makes you feel seen and understood?",
    "What does your inner child need to hear from you right now?",
    "List 3 things that bring you comfort, no matter how small."
]

ANGER_PROMPTS = [
    "What boundary was crossed? What need wasn't met?",
    "If you could say anything to the source of your anger (without consequences), what would it be?",
    "Underneath the anger, what other emotion might be hiding?",
    "What would help you release this anger in a healthy way?",
    "Is this anger protecting you from something? What?",
    "On a scale of 1-10, how important will this feel in a week?",
    "What do you need in order to feel respected in this situation?",
    "Write out all your angry thoughts. Don't filter, just write.",
    "What would resolution look like for you?",
    "How can you honor your anger without letting it control you?"
]

GRATITUDE_PROMPTS = [
    "Name 3 simple things that made today bearable.",
    "Who showed you kindness recently? How did it make you feel?",
    "What's a challenge that taught you something valuable?",
    "What's one thing about your body you're grateful for today?",
    "Look around your space. What object brings you comfort?",
    "What's a skill or ability you're thankful to have?",
    "Who's someone you're glad exists in the world?",
    "What's a recent small pleasure you might usually overlook?",
    "What's something you have today that past-you would be grateful for?",
    "What's beautiful about this exact moment?"
]

EVENING_REFLECTION_PROMPTS = [
    "What's one thing you can let go of before you sleep?",
    "How did you show up for yourself today?",
    "What challenged you today and how did you handle it?",
    "What's one thing you want to remember from today?",
    "If today had a title, what would it be?",
    "What emotion dominated your day? What might tomorrow feel like?",
    "What do you need to forgive yourself for today?",
    "What's one intention you want to set for tomorrow?",
    "Rate your day 1-10. What made it that number?",
    "What are you looking forward to, even if it's something small?"
]

MORNING_INTENTION_PROMPTS = [
    "What's ONE thing that would make today feel successful?",
    "How do you want to feel by the end of today?",
    "What's your mantra or word for the day?",
    "What are you grateful for this morning?",
    "Who can you show kindness to today?",
    "What's one act of self-care you'll do today?",
    "What potential challenge might come up? How will you handle it?",
    "What's the most important task for today?",
    "How will you take care of your mental health today?",
    "Complete this: Today, I give myself permission to..."
]


def get_random_prompt(category: str = "general") -> str:
    """
    Returns a random journaling prompt based on category.
    
    Args:
        category: Category of prompt (general, stress, anxiety, sadness, anger, gratitude, evening, morning)
    
    Returns:
        A journaling prompt string
    """
    category_map = {
        "general": SELF_REFLECTION_PROMPTS,
        "reflection": SELF_REFLECTION_PROMPTS,
        "stress": STRESS_RELIEF_PROMPTS,
        "stressed": STRESS_RELIEF_PROMPTS,
        "anxiety": ANXIETY_PROMPTS,
        "anxious": ANXIETY_PROMPTS,
        "sadness": SADNESS_PROMPTS,
        "sad": SADNESS_PROMPTS,
        "anger": ANGER_PROMPTS,
        "angry": ANGER_PROMPTS,
        "gratitude": GRATITUDE_PROMPTS,
        "grateful": GRATITUDE_PROMPTS,
        "evening": EVENING_REFLECTION_PROMPTS,
        "night": EVENING_REFLECTION_PROMPTS,
        "morning": MORNING_INTENTION_PROMPTS,
        "tired": SADNESS_PROMPTS  # Tired often correlates with low mood
    }
    
    prompts = category_map.get(category.lower(), SELF_REFLECTION_PROMPTS)
    return random.choice(prompts)


def get_mood_based_prompts(mood: str, count: int = 3) -> List[str]:
    """
    Returns multiple prompts based on mood.
    
    Args:
        mood: Type of mood (Stressed, Sad, Anxious, Angry, Tired)
        count: Number of prompts to return
    
    Returns:
        List of journaling prompts
    """
    mood_to_category = {
        "Stressed": STRESS_RELIEF_PROMPTS,
        "Sad": SADNESS_PROMPTS,
        "Anxious": ANXIETY_PROMPTS,
        "Angry": ANGER_PROMPTS,
        "Tired": SADNESS_PROMPTS + GRATITUDE_PROMPTS
    }
    
    prompts = mood_to_category.get(mood, SELF_REFLECTION_PROMPTS)
    return random.sample(prompts, min(count, len(prompts)))


def get_all_categories() -> Dict[str, List[str]]:
    """Returns all prompt categories with their prompts."""
    return {
        "Self-Reflection": SELF_REFLECTION_PROMPTS,
        "Stress Relief": STRESS_RELIEF_PROMPTS,
        "Anxiety": ANXIETY_PROMPTS,
        "Sadness": SADNESS_PROMPTS,
        "Anger": ANGER_PROMPTS,
        "Gratitude": GRATITUDE_PROMPTS,
        "Evening Reflection": EVENING_REFLECTION_PROMPTS,
        "Morning Intentions": MORNING_INTENTION_PROMPTS
    }


def format_prompts_for_display(prompts: List[str]) -> str:
    """Formats multiple prompts for nice display."""
    formatted = "### 📝 Journaling Prompts for You\n\n"
    formatted += "*Choose one that speaks to you, or write about all of them.*\n\n"
    
    for i, prompt in enumerate(prompts, 1):
        formatted += f"**{i}.** {prompt}\n\n"
    
    formatted += "---\n"
    formatted += "*💡 Tip: There are no wrong answers. Write freely without judgment.*"
    
    return formatted
