"""
MindEase - AI Mental Wellness Voice Chatbot
Main Streamlit Application
SDG 3: Good Health & Well-being
"""

import streamlit as st
import time
import base64
import tempfile
import os
from datetime import datetime

# Import custom modules
from utils.chatbot import MindEaseAI
from utils.crisis_detector import detect_crisis, is_severe_distress, get_gentle_checkin
from utils.coping_toolkit import (
    get_breathing_exercise, get_grounding_exercise, get_reset_routine,
    get_sleep_tips, get_focus_tips, get_mood_based_exercise, get_all_exercises
)
from utils.journaling import get_random_prompt, get_mood_based_prompts, format_prompts_for_display
from utils.voice_handler import VoiceHandler, check_microphone_availability

# ============= PAGE CONFIGURATION =============

st.set_page_config(
    page_title="MindEase - AI Mental Wellness Companion",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============= CUSTOM CSS STYLING =============

st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6B73FF;
        --secondary-color: #A5E887;
        --bg-color: #0E1117;
        --card-bg: #1E2028;
    }
    
    /* Chat message styling */
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 15px 20px;
        border-radius: 20px 20px 5px 20px;
        margin: 10px 0;
        color: white;
        max-width: 80%;
        margin-left: auto;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 15px 20px;
        border-radius: 20px 20px 20px 5px;
        margin: 10px 0;
        color: white;
        max-width: 80%;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 20px;
    }
    
    .main-header h1 {
        color: white;
        margin: 0;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        margin: 10px 0 0 0;
    }
    
    /* Card styling */
    .feature-card {
        background: linear-gradient(145deg, #1E2028 0%, #2D3040 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
    
    /* Mood slider */
    .stSlider > div > div {
        background: linear-gradient(90deg, #38ef7d, #f9d423, #ff6b6b);
    }
    
    /* Voice button styling */
    .voice-btn {
        background: linear-gradient(135deg, #FF6B6B 0%, #FF8E53 100%);
        color: white;
        padding: 10px 20px;
        border-radius: 25px;
        border: none;
        cursor: pointer;
    }
    
    /* Status indicators */
    .status-online {
        color: #38ef7d;
        font-weight: bold;
    }
    
    .status-offline {
        color: #ff6b6b;
        font-weight: bold;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Smooth animations */
    .stButton > button {
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# ============= SESSION STATE INITIALIZATION =============

def init_session_state():
    """Initialize all session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = MindEaseAI()
    
    if "voice_handler" not in st.session_state:
        st.session_state.voice_handler = VoiceHandler()
    
    if "current_mood" not in st.session_state:
        st.session_state.current_mood = None
    
    if "mood_intensity" not in st.session_state:
        st.session_state.mood_intensity = 5
    
    if "voice_enabled" not in st.session_state:
        st.session_state.voice_enabled = True
    
    if "show_mood_checkin" not in st.session_state:
        st.session_state.show_mood_checkin = False
    
    if "last_audio" not in st.session_state:
        st.session_state.last_audio = None
    
    if "play_message_index" not in st.session_state:
        st.session_state.play_message_index = None
    
    if "conversation_started" not in st.session_state:
        st.session_state.conversation_started = False
    
    if "total_messages" not in st.session_state:
        st.session_state.total_messages = 0

init_session_state()

# ============= HELPER FUNCTIONS =============

def add_message(role: str, content: str):
    """Add a message to the chat history."""
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M")
    })
    st.session_state.total_messages += 1
    if not st.session_state.conversation_started:
        st.session_state.conversation_started = True

def display_messages():
    """Display all messages in the chat history with play buttons."""
    for idx, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg["content"])
        else:
            with st.chat_message("assistant", avatar="🧘"):
                st.markdown(msg["content"])
                # Add play button for bot messages
                if st.button("🔊 Play", key=f"play_{idx}", help="Click to hear this message"):
                    st.session_state.play_message_index = idx

def process_user_input(user_input: str):
    """Process user input and generate response."""
    # Check for crisis content first
    is_crisis, crisis_response = detect_crisis(user_input)
    
    if is_crisis:
        add_message("user", user_input)
        add_message("assistant", crisis_response)
        return crisis_response
    
    # Generate AI response
    add_message("user", user_input)
    
    response = st.session_state.chatbot.generate_response(
        user_input,
        mood=st.session_state.current_mood,
        intensity=st.session_state.mood_intensity
    )
    
    add_message("assistant", response)
    
    return response

def text_to_speech(text: str):
    """Convert text to speech and play it."""
    if st.session_state.voice_enabled and st.session_state.voice_handler.is_tts_available():
        try:
            # Use gTTS for audio file generation (works better in Streamlit)
            audio_path = st.session_state.voice_handler.speak(text, use_gtts=True)
            if audio_path and os.path.exists(audio_path):
                # Read audio bytes before displaying
                with open(audio_path, "rb") as audio_file:
                    audio_bytes = audio_file.read()
                # Clean up temp file first
                try:
                    os.unlink(audio_path)
                except:
                    pass
                # Store in session state to persist
                st.session_state.last_audio = audio_bytes
        except Exception as e:
            st.warning(f"Voice output unavailable: {e}")

def export_conversation() -> str:
    """Export conversation history as formatted text."""
    if not st.session_state.messages:
        return "No conversation to export."
    
    export_text = f"MindEase Conversation Export\n"
    export_text += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
    export_text += f"Total Messages: {len(st.session_state.messages)}\n"
    if st.session_state.current_mood:
        export_text += f"Mood: {st.session_state.current_mood} (Intensity: {st.session_state.mood_intensity}/10)\n"
    export_text += "=" * 50 + "\n\n"
    
    for msg in st.session_state.messages:
        role = "You" if msg["role"] == "user" else "MindEase"
        export_text += f"[{msg['timestamp']}] {role}:\n{msg['content']}\n\n"
    
    export_text += "=" * 50 + "\n"
    export_text += "Remember: This is not a substitute for professional mental health support.\n"
    export_text += "If you're in crisis, contact: iCall (9152987821) or Vandrevala Foundation (1860-2662-345)"
    
    return export_text

# ============= SIDEBAR =============

with st.sidebar:
    # Logo and Title
    st.markdown("""
    <div style='text-align: center; padding: 20px;'>
        <h1 style='color: #667eea;'>🧘 MindEase</h1>
        <p style='color: #888;'>Your AI Mental Wellness Companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Mood Check-in Section
    st.markdown("### 🎭 Mood Check-in")
    
    mood_options = ["Stressed", "Sad", "Anxious", "Angry", "Tired"]
    selected_mood = st.selectbox("How are you feeling?", ["Select mood..."] + mood_options)
    
    if selected_mood != "Select mood...":
        st.session_state.current_mood = selected_mood
        
        intensity = st.slider(
            "Intensity (1 = mild, 10 = severe)",
            min_value=1,
            max_value=10,
            value=st.session_state.mood_intensity,
            key="mood_slider"
        )
        st.session_state.mood_intensity = intensity
        
        # Visual intensity indicator
        if intensity <= 3:
            st.success(f"💚 Mild {selected_mood.lower()}")
        elif intensity <= 6:
            st.warning(f"💛 Moderate {selected_mood.lower()}")
        else:
            st.error(f"❤️ Intense {selected_mood.lower()}")
        
        if st.button("Get Support for This Mood", type="primary"):
            # Check for severe distress
            if is_severe_distress(selected_mood, intensity):
                response = get_gentle_checkin() + "\n\n---\n\n" + get_mood_based_exercise(selected_mood, intensity)
            else:
                response = get_mood_based_exercise(selected_mood, intensity)
            
            add_message("user", f"[Mood Check-in: {selected_mood}, Intensity: {intensity}/10]")
            add_message("assistant", response)
            st.rerun()
    
    st.divider()
    
    # Coping Toolkit
    st.markdown("### 🧰 Coping Toolkit")
    
    toolkit_option = st.selectbox(
        "Quick Exercises",
        ["Select exercise...", "🌬️ Breathing Exercise", "🌍 Grounding (5-4-3-2-1)", 
         "🔄 Quick Reset", "😴 Sleep Tips", "🎯 Focus Tips"]
    )
    
    if toolkit_option != "Select exercise...":
        if st.button("Show Exercise"):
            if "Breathing" in toolkit_option:
                response = get_breathing_exercise("random")
            elif "Grounding" in toolkit_option:
                response = get_grounding_exercise("54321")
            elif "Reset" in toolkit_option:
                response = get_reset_routine("random")
            elif "Sleep" in toolkit_option:
                response = get_sleep_tips()
            elif "Focus" in toolkit_option:
                response = get_focus_tips()
            else:
                response = get_breathing_exercise("random")
            
            add_message("assistant", response)
            st.rerun()
    
    st.divider()
    
    # Journaling Prompts
    st.markdown("### 📝 Journaling")
    
    if st.button("Get Writing Prompts"):
        if st.session_state.current_mood:
            prompts = get_mood_based_prompts(st.session_state.current_mood, 3)
        else:
            prompts = [get_random_prompt() for _ in range(3)]
        
        formatted = format_prompts_for_display(prompts)
        add_message("assistant", formatted)
        st.rerun()
    
    st.divider()
    
    # Voice Settings
    st.markdown("### 🎤 Voice Settings")
    
    voice_status = st.session_state.voice_handler.get_status()
    
    st.session_state.voice_enabled = st.toggle("Enable Voice Output", value=st.session_state.voice_enabled)
    
    col1, col2 = st.columns(2)
    with col1:
        if voice_status["tts_available"]:
            st.markdown("🔊 <span class='status-online'>TTS Ready</span>", unsafe_allow_html=True)
        else:
            st.markdown("🔇 <span class='status-offline'>TTS Unavailable</span>", unsafe_allow_html=True)
    
    with col2:
        if voice_status["stt_available"]:
            st.markdown("🎙️ <span class='status-online'>Mic Ready</span>", unsafe_allow_html=True)
        else:
            st.markdown("🎙️ <span class='status-offline'>Mic Unavailable</span>", unsafe_allow_html=True)
    
    st.divider()
    
    # AI Status
    st.markdown("### 🤖 AI Status")
    ai_status = st.session_state.chatbot.get_status()
    
    if ai_status["ai_available"]:
        st.success(f"✅ {ai_status['provider']}")
        st.caption(f"Model: {ai_status['model']}")
    else:
        st.info(f"💡 {ai_status['model']}")
        st.caption("Add GOOGLE_API_KEY for AI responses")
    
    st.divider()
    
    # Conversation actions
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reset", use_container_width=True, help="Start fresh conversation"):
            st.session_state.messages = []
            st.session_state.chatbot.reset_conversation()
            st.session_state.current_mood = None
            st.session_state.mood_intensity = 5
            st.session_state.conversation_started = False
            st.session_state.total_messages = 0
            st.rerun()
    
    with col2:
        if st.button("💾 Export", use_container_width=True, help="Download conversation"):
            if st.session_state.messages:
                export_text = export_conversation()
                st.download_button(
                    label="📥 Download",
                    data=export_text,
                    file_name=f"mindease_chat_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            else:
                st.info("No conversation to export yet")
    
    # Session Stats
    if st.session_state.conversation_started:
        st.divider()
        st.markdown("### 📊 Session Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Messages", st.session_state.total_messages)
        with col2:
            if st.session_state.current_mood:
                st.metric("Mood", f"{st.session_state.current_mood} ({st.session_state.mood_intensity}/10)")
    
    # Footer
    st.markdown("""
    <div style='text-align: center; padding: 20px; color: #666; font-size: 12px;'>
        <p>MindEase v1.0</p>
        <p>SDG 3: Good Health & Well-being</p>
        <p>IBM SkillsBuild Capstone 2025</p>
    </div>
    """, unsafe_allow_html=True)

# ============= MAIN CONTENT AREA =============

# Header
st.markdown("""
<div class="main-header">
    <h1>🧘 MindEase</h1>
    <p>Your AI Mental Wellness Voice Companion | SDG 3: Good Health & Well-being</p>
</div>
""", unsafe_allow_html=True)

# Welcome message if no messages
if not st.session_state.messages:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>👋 Welcome to MindEase!</h3>
            <p>I'm your AI mental wellness companion, here to support you with compassion and practical help.</p>
            
            <h4>🎯 How I Can Help:</h4>
            <ul>
                <li>💬 <strong>Talk it out</strong> - Share what's on your mind, I'll listen without judgment</li>
                <li>🎭 <strong>Mood check-in</strong> - Track how you're feeling and get personalized support</li>
                <li>🧰 <strong>Instant relief</strong> - Access breathing exercises, grounding techniques</li>
                <li>📝 <strong>Process thoughts</strong> - Get reflective journaling prompts</li>
                <li>🎤 <strong>Voice option</strong> - Speak naturally or listen to responses</li>
            </ul>
            
            <h4>🚀 Quick Start:</h4>
            <p><strong>1.</strong> Do a mood check-in (sidebar) → <strong>2.</strong> Tell me what's bothering you → <strong>3.</strong> Try suggested exercises</p>
            
            <p style='background: #2d3040; padding: 10px; border-radius: 8px; margin-top: 15px;'>
            <strong>⚠️ Important:</strong> I'm here for support and coping strategies, but I'm not a replacement for therapy or medical care. 
            If you're in crisis, please contact: <strong>iCall (9152987821)</strong> or <strong>Vandrevala Foundation (1860-2662-345)</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>💡 Tips for Best Experience:</h4>
            <ul style='font-size: 14px;'>
                <li>Be honest about how you're feeling</li>
                <li>Try the exercises - they really help</li>
                <li>Use voice if typing feels hard</li>
                <li>Export chats to reflect later</li>
                <li>It's okay to take breaks</li>
            </ul>
            
            <h4>🌟 You're Not Alone</h4>
            <p style='font-size: 14px;'>Taking this step shows strength. Let's work through this together.</p>
        </div>
        """, unsafe_allow_html=True)

# Display chat messages
display_messages()

# Play audio if user clicked a play button
if st.session_state.play_message_index is not None:
    msg_idx = st.session_state.play_message_index
    if msg_idx < len(st.session_state.messages):
        msg_content = st.session_state.messages[msg_idx]["content"]
        text_to_speech(msg_content)
    st.session_state.play_message_index = None

# Play audio if available (from play button)
if st.session_state.last_audio:
    st.audio(st.session_state.last_audio, format="audio/mp3", autoplay=True)
    st.session_state.last_audio = None

# ============= CHAT INPUT SECTION =============

# Create columns for text and voice input
col_text, col_voice = st.columns([5, 1])

with col_text:
    user_input = st.chat_input("Type your message here...", key="chat_input")

with col_voice:
    voice_button = st.button("🎤", key="voice_btn", help="Click to speak")

# Handle text input
if user_input:
    response = process_user_input(user_input)
    st.rerun()

# Handle voice input
if voice_button:
    if st.session_state.voice_handler.is_stt_available():
        with st.spinner("🎤 Listening... Speak now!"):
            success, result = st.session_state.voice_handler.listen(timeout=5, phrase_limit=15)
            
            if success:
                st.success(f"Heard: {result}")
                response = process_user_input(result)
                st.rerun()
            else:
                st.error(result)
    else:
        st.error("🎙️ Microphone not available. Please check your audio settings and install PyAudio.")
        st.info("**Windows:** `pip install pyaudio`")
        st.info("**Mac:** `brew install portaudio && pip install pyaudio`")
        st.info("**Linux:** `sudo apt-get install portaudio19-dev && pip install pyaudio`")

# ============= QUICK ACTION BUTTONS =============

st.divider()

st.markdown("### ⚡ Quick Actions")

quick_cols = st.columns(5)

with quick_cols[0]:
    if st.button("🌬️ Breathe", use_container_width=True):
        response = get_breathing_exercise("478")
        add_message("assistant", response)
        st.rerun()

with quick_cols[1]:
    if st.button("🌍 Ground", use_container_width=True):
        response = get_grounding_exercise("54321")
        add_message("assistant", response)
        st.rerun()

with quick_cols[2]:
    if st.button("📝 Journal", use_container_width=True):
        prompts = [get_random_prompt() for _ in range(3)]
        response = format_prompts_for_display(prompts)
        add_message("assistant", response)
        st.rerun()

with quick_cols[3]:
    if st.button("😴 Sleep", use_container_width=True):
        response = get_sleep_tips()
        add_message("assistant", response)
        st.rerun()

with quick_cols[4]:
    if st.button("🎯 Focus", use_container_width=True):
        response = get_focus_tips()
        add_message("assistant", response)
        st.rerun()

# ============= FOOTER =============

st.divider()

# Show stats if conversation started
if st.session_state.conversation_started:
    footer_cols = st.columns(3)
    with footer_cols[0]:
        st.info(f"💬 {st.session_state.total_messages} messages exchanged")
    with footer_cols[1]:
        if st.session_state.current_mood:
            st.info(f"🎭 Mood: {st.session_state.current_mood}")
    with footer_cols[2]:
        st.info("💚 You're doing great by seeking support")

st.markdown("""
<div style='text-align: center; padding: 20px; color: #666;'>
    <p>🆘 <strong>In crisis?</strong> iCall: 9152987821 | Vandrevala Foundation: 1860-2662-345 (24/7)</p>
    <p style='font-size: 12px;'>MindEase is an AI wellness companion, not a substitute for professional mental health support.</p>
    <p style='font-size: 11px; margin-top: 10px;'>💡 Tip: Press <strong>Ctrl+Enter</strong> to send messages quickly</p>
</div>
""", unsafe_allow_html=True)
