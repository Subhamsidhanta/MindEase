"""
Coping Toolkit Module
Contains various coping exercises and techniques for mental wellness
"""

from typing import Dict, List
import random

# ============= BREATHING EXERCISES =============

BREATHING_478 = """
### 🌬️ 4-7-8 Breathing Technique

This calming breath helps activate your parasympathetic nervous system.

**How to do it:**

1. 😮‍💨 **Exhale** completely through your mouth
2. 👃 **Inhale** quietly through your nose for **4 seconds**
3. 🔒 **Hold** your breath for **7 seconds**
4. 😮‍💨 **Exhale** completely through your mouth for **8 seconds**

**Repeat 3-4 times.**

💡 *Tip: Place the tip of your tongue against the ridge behind your upper front teeth throughout.*
"""

BOX_BREATHING = """
### 📦 Box Breathing (4-4-4-4)

Used by Navy SEALs for stress management!

**How to do it:**

1. 👃 **Inhale** for **4 seconds**
2. 🔒 **Hold** for **4 seconds**
3. 😮‍💨 **Exhale** for **4 seconds**
4. 🔒 **Hold** for **4 seconds**

**Repeat 4-5 times.**

💡 *Imagine tracing a square as you breathe - each side is 4 seconds.*
"""

QUICK_CALM_BREATH = """
### ⚡ Quick Calm Breath

Perfect when you need fast relief!

**How to do it:**

1. 👃 Take a deep breath in through your nose (3 seconds)
2. 😮‍💨 Sigh it out through your mouth with an "Ahhh" sound
3. 🔄 Repeat 3 times

💡 *The sigh activates your body's relaxation response instantly.*
"""

# ============= GROUNDING EXERCISES =============

GROUNDING_54321 = """
### 🌍 5-4-3-2-1 Grounding Technique

This technique helps bring you back to the present moment.

**Find and name:**

👀 **5 things you can SEE**
- Look around and notice 5 things (colors, shapes, objects)

👂 **4 things you can HEAR**
- Listen for sounds near and far

✋ **3 things you can TOUCH**
- Feel textures around you

👃 **2 things you can SMELL**
- Notice any scents in your environment

👅 **1 thing you can TASTE**
- What taste is in your mouth right now?

💡 *Take your time with each sense. This pulls your mind from worry to the present.*
"""

BODY_SCAN_QUICK = """
### 🧘 Quick Body Scan (2 minutes)

Release tension you didn't know you were holding.

**Instructions:**

1. 👣 Start at your **feet** - notice any tension, then release
2. 🦵 Move to your **legs** - are they tight? Let them soften
3. 🫁 Notice your **stomach** - let it relax with each breath
4. 💪 Check your **shoulders** - drop them away from your ears
5. 😐 Relax your **face** - unclench your jaw, soften your forehead
6. 🧠 Finally, notice your **mind** - just observe, don't judge

💡 *You can do this sitting, standing, or lying down.*
"""

ANCHORING_EXERCISE = """
### ⚓ Anchoring Exercise

Connect with stability when you feel overwhelmed.

**How to do it:**

1. 👣 Feel your feet firmly on the ground
2. 🪑 Notice where your body touches the chair/floor
3. 🤲 Press your palms together firmly for 5 seconds
4. 💨 Take 3 slow, deep breaths
5. 🔊 Say to yourself: "I am here. I am safe. This will pass."

💡 *Repeat the affirmation as many times as you need.*
"""

# ============= RESET ROUTINES =============

SHORT_RESET = """
### 🔄 2-Minute Reset Routine

Quick mental refresh when you're overwhelmed.

**Do this now:**

1. ⏸️ **STOP** what you're doing
2. 🚶 **STAND UP** and stretch your arms overhead
3. 🌬️ **Take 5 deep breaths** (slow and steady)
4. 🚰 **Drink a glass of water** (hydration matters!)
5. 👀 **Look out a window** or at something far away for 20 seconds
6. 😊 **Smile** (even a fake smile triggers feel-good chemicals)

💡 *Set a reminder to do this every 2 hours during stressful days.*
"""

STRESS_RELEASE_SHAKE = """
### 🐕 Stress Release Shake

Animals naturally shake off stress - so can you!

**How to do it:**

1. 🧍 Stand up with feet shoulder-width apart
2. 🤸 Start gently shaking your hands
3. 💪 Let the shake move up your arms
4. 🦵 Shake your legs one at a time
5. 🕺 Let your whole body shake for 30-60 seconds
6. 🧘 Stop and notice how you feel

💡 *This releases physical tension and resets your nervous system.*
"""

# ============= SLEEP TIPS =============

SLEEP_TIPS = """
### 😴 Sleep Wellness Tips

Quality sleep is foundational for mental health.

**Pre-Sleep Routine:**
- 📱 No screens 1 hour before bed
- 🌡️ Keep your room cool (65-68°F / 18-20°C)
- ☕ No caffeine after 2 PM
- 🛁 Try a warm bath/shower before bed

**Can't Sleep? Try:**
- 🌬️ 4-7-8 breathing technique
- 📖 Read something calming (not on a screen)
- 🧘 Progressive muscle relaxation
- 🎵 Soft, instrumental music or white noise

**Sleep Affirmation:**
*"My body knows how to rest. I release today and welcome peaceful sleep."*
"""

# ============= FOCUS TIPS =============

FOCUS_TIPS = """
### 🎯 Focus & Concentration Tips

When your mind feels scattered:

**Quick Focus Techniques:**
- 🍅 **Pomodoro**: 25 min focus + 5 min break
- ✍️ **Brain dump**: Write all thoughts on paper to clear your mind
- 🎧 **Focus music**: Lo-fi, nature sounds, or binaural beats
- 📵 **Phone away**: Out of sight, out of mind

**Environment Hacks:**
- 💡 Good lighting (natural light is best)
- 🧹 Clear your workspace
- 💧 Stay hydrated
- 🌿 Add a plant if possible

**One Thing Rule:**
*Close all tabs. Pick ONE task. Set a timer. Begin.*
"""

# ============= TOOLKIT FUNCTIONS =============

def get_breathing_exercise(exercise_type: str = "random") -> str:
    """Returns a breathing exercise based on type or random."""
    exercises = {
        "478": BREATHING_478,
        "box": BOX_BREATHING,
        "quick": QUICK_CALM_BREATH
    }
    
    if exercise_type == "random":
        return random.choice(list(exercises.values()))
    return exercises.get(exercise_type, BREATHING_478)


def get_grounding_exercise(exercise_type: str = "random") -> str:
    """Returns a grounding exercise based on type or random."""
    exercises = {
        "54321": GROUNDING_54321,
        "bodyscan": BODY_SCAN_QUICK,
        "anchoring": ANCHORING_EXERCISE
    }
    
    if exercise_type == "random":
        return random.choice(list(exercises.values()))
    return exercises.get(exercise_type, GROUNDING_54321)


def get_reset_routine(routine_type: str = "random") -> str:
    """Returns a reset routine based on type or random."""
    routines = {
        "short": SHORT_RESET,
        "shake": STRESS_RELEASE_SHAKE
    }
    
    if routine_type == "random":
        return random.choice(list(routines.values()))
    return routines.get(routine_type, SHORT_RESET)


def get_sleep_tips() -> str:
    """Returns sleep wellness tips."""
    return SLEEP_TIPS


def get_focus_tips() -> str:
    """Returns focus and concentration tips."""
    return FOCUS_TIPS


def get_mood_based_exercise(mood: str, intensity: int) -> str:
    """
    Returns an appropriate exercise based on mood and intensity.
    
    Args:
        mood: Type of mood (Stressed, Sad, Anxious, Angry, Tired)
        intensity: Intensity level (1-10)
    
    Returns:
        Appropriate coping exercise as string
    """
    recommendations = {
        "Stressed": {
            "low": QUICK_CALM_BREATH,
            "medium": BOX_BREATHING,
            "high": BREATHING_478 + "\n\n---\n\n" + GROUNDING_54321
        },
        "Anxious": {
            "low": ANCHORING_EXERCISE,
            "medium": GROUNDING_54321,
            "high": BREATHING_478 + "\n\n---\n\n" + BODY_SCAN_QUICK
        },
        "Sad": {
            "low": SHORT_RESET,
            "medium": STRESS_RELEASE_SHAKE,
            "high": GROUNDING_54321 + "\n\n---\n\n" + SHORT_RESET
        },
        "Angry": {
            "low": QUICK_CALM_BREATH,
            "medium": BOX_BREATHING,
            "high": STRESS_RELEASE_SHAKE + "\n\n---\n\n" + BREATHING_478
        },
        "Tired": {
            "low": QUICK_CALM_BREATH,
            "medium": SHORT_RESET,
            "high": SLEEP_TIPS
        }
    }
    
    # Determine intensity level
    if intensity <= 3:
        level = "low"
    elif intensity <= 6:
        level = "medium"
    else:
        level = "high"
    
    return recommendations.get(mood, {}).get(level, GROUNDING_54321)


def get_all_exercises() -> Dict[str, List[str]]:
    """Returns a dictionary of all available exercises by category."""
    return {
        "Breathing": ["4-7-8 Breathing", "Box Breathing", "Quick Calm Breath"],
        "Grounding": ["5-4-3-2-1 Technique", "Body Scan", "Anchoring"],
        "Reset Routines": ["2-Minute Reset", "Stress Release Shake"],
        "Wellness": ["Sleep Tips", "Focus Tips"]
    }
