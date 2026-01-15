"""
Voice Handler Module
Handles speech-to-text and text-to-speech functionality
Uses Edge TTS for natural sounding voices
"""

import os
import tempfile
import threading
import asyncio
from typing import Optional, Tuple

# Edge TTS (Natural sounding voices)
try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

# Text-to-Speech
try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False

# Speech Recognition
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False

# Google TTS (backup)
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except ImportError:
    GTTS_AVAILABLE = False

# Natural sounding voice options for Edge TTS
VOICE_OPTIONS = {
    "female_warm": "en-US-JennyNeural",      # Warm, friendly female voice
    "female_calm": "en-US-AriaNeural",        # Calm, soothing female voice  
    "male_calm": "en-US-GuyNeural",           # Calm male voice
    "female_indian": "en-IN-NeerjaNeural",    # Indian English female
    "male_indian": "en-IN-PrabhatNeural",     # Indian English male
}

# Default to a warm, calming voice for mental wellness
DEFAULT_VOICE = "en-US-JennyNeural"


class VoiceHandler:
    """Handles voice input and output for the chatbot."""
    
    def __init__(self, voice: str = DEFAULT_VOICE):
        """Initialize voice handler with available engines."""
        self.tts_engine = None
        self.recognizer = None
        self.voice = voice
        self._init_tts()
        self._init_stt()
    
    def _init_tts(self):
        """Initialize text-to-speech engine."""
        if PYTTSX3_AVAILABLE:
            try:
                self.tts_engine = pyttsx3.init()
                # Configure voice settings
                self.tts_engine.setProperty('rate', 150)  # Speed
                self.tts_engine.setProperty('volume', 0.9)  # Volume
                
                # Try to set a pleasant voice
                voices = self.tts_engine.getProperty('voices')
                if voices:
                    # Prefer female voice if available (often index 1)
                    if len(voices) > 1:
                        self.tts_engine.setProperty('voice', voices[1].id)
            except Exception as e:
                print(f"pyttsx3 initialization failed: {e}")
                self.tts_engine = None
    
    def _init_stt(self):
        """Initialize speech-to-text recognizer."""
        if SPEECH_RECOGNITION_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                # Adjust for ambient noise sensitivity
                self.recognizer.energy_threshold = 300
                self.recognizer.dynamic_energy_threshold = True
            except Exception as e:
                print(f"Speech recognition initialization failed: {e}")
                self.recognizer = None
    
    def speak(self, text: str, use_gtts: bool = False) -> Optional[str]:
        """
        Convert text to speech.
        
        Args:
            text: Text to speak
            use_gtts: Whether to use Google TTS (ignored, Edge TTS preferred)
        
        Returns:
            Path to audio file
        """
        # Clean text for speech (remove markdown formatting)
        clean_text = self._clean_text_for_speech(text)
        
        # Prefer Edge TTS for natural voice
        if EDGE_TTS_AVAILABLE:
            return self._speak_edge_tts(clean_text)
        elif GTTS_AVAILABLE:
            return self._speak_gtts(clean_text)
        elif self.tts_engine:
            self._speak_pyttsx3(clean_text)
            return None
        else:
            print("No TTS engine available")
            return None
    
    def _speak_edge_tts(self, text: str) -> Optional[str]:
        """Generate speech using Edge TTS (natural sounding)."""
        try:
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
                temp_path = f.name
            
            # Run async function
            asyncio.run(self._generate_edge_audio(text, temp_path))
            
            return temp_path
        except Exception as e:
            print(f"Edge TTS failed: {e}")
            # Fallback to gTTS
            if GTTS_AVAILABLE:
                return self._speak_gtts(text)
            return None
    
    async def _generate_edge_audio(self, text: str, output_path: str):
        """Async function to generate audio with Edge TTS."""
        communicate = edge_tts.Communicate(text, self.voice)
        await communicate.save(output_path)
    
    def _speak_pyttsx3(self, text: str) -> None:
        """Speak text using pyttsx3."""
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"pyttsx3 speech failed: {e}")
    
    def _speak_gtts(self, text: str) -> Optional[str]:
        """Generate speech audio file using Google TTS."""
        try:
            tts = gTTS(text=text, lang='en', slow=False)
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as f:
                temp_path = f.name
            tts.save(temp_path)
            return temp_path
        except Exception as e:
            print(f"gTTS failed: {e}")
            return None
    
    def _clean_text_for_speech(self, text: str) -> str:
        """Remove markdown and special formatting for cleaner speech."""
        import re
        
        # Remove markdown headers
        text = re.sub(r'#{1,6}\s*', '', text)
        # Remove bold/italic markers
        text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', text)
        # Remove bullet points
        text = re.sub(r'^[-•]\s*', '', text, flags=re.MULTILINE)
        # Remove emojis (basic approach)
        text = re.sub(r'[^\w\s.,!?;:\'\"-]', '', text)
        # Clean up extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Limit length for speech
        if len(text) > 500:
            text = text[:500] + "... Please read the full response on screen."
        
        return text
    
    def listen(self, timeout: int = 5, phrase_limit: int = 10) -> Tuple[bool, str]:
        """
        Listen for speech and convert to text.
        
        Args:
            timeout: Maximum seconds to wait for phrase to start
            phrase_limit: Maximum seconds of speech to capture
        
        Returns:
            Tuple of (success: bool, text_or_error: str)
        """
        if not self.recognizer:
            return False, "Speech recognition not available. Please install SpeechRecognition package."
        
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                print("Listening...")
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit
                )
                
                print("Processing speech...")
                text = self.recognizer.recognize_google(audio)
                return True, text
                
        except sr.WaitTimeoutError:
            return False, "No speech detected. Please try again."
        except sr.UnknownValueError:
            return False, "Could not understand audio. Please speak clearly."
        except sr.RequestError as e:
            return False, f"Speech recognition service error: {e}"
        except Exception as e:
            return False, f"Microphone error: {e}. Please check your microphone."
    
    def is_tts_available(self) -> bool:
        """Check if text-to-speech is available."""
        return EDGE_TTS_AVAILABLE or self.tts_engine is not None or GTTS_AVAILABLE
    
    def is_stt_available(self) -> bool:
        """Check if speech-to-text is available."""
        return self.recognizer is not None
    
    def set_voice(self, voice_key: str):
        """Set the voice for Edge TTS."""
        if voice_key in VOICE_OPTIONS:
            self.voice = VOICE_OPTIONS[voice_key]
        else:
            self.voice = voice_key
    
    def get_status(self) -> dict:
        """Get status of voice capabilities."""
        if EDGE_TTS_AVAILABLE:
            tts_engine = "Edge TTS (Natural)"
        elif self.tts_engine:
            tts_engine = "pyttsx3"
        elif GTTS_AVAILABLE:
            tts_engine = "gTTS"
        else:
            tts_engine = None
            
        return {
            "tts_available": self.is_tts_available(),
            "tts_engine": tts_engine,
            "voice": self.voice if EDGE_TTS_AVAILABLE else "default",
            "stt_available": self.is_stt_available(),
            "stt_engine": "Google Speech Recognition" if self.recognizer else None
        }
    
    def get_available_voices(self) -> dict:
        """Get available voice options."""
        return VOICE_OPTIONS


# Alternative async speech for non-blocking TTS
def speak_async(text: str, voice_handler: VoiceHandler):
    """Speak text in a background thread."""
    thread = threading.Thread(target=voice_handler.speak, args=(text,))
    thread.daemon = True
    thread.start()
    return thread


def check_microphone_availability() -> Tuple[bool, str]:
    """Check if microphone is available and accessible."""
    if not SPEECH_RECOGNITION_AVAILABLE:
        return False, "SpeechRecognition package not installed."
    
    try:
        mics = sr.Microphone.list_microphone_names()
        if not mics:
            return False, "No microphone found."
        return True, f"Found {len(mics)} microphone(s): {mics[0]}"
    except Exception as e:
        return False, f"Microphone check failed: {e}"
