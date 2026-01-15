# MindEase Testing Checklist

## ✅ Pre-Demo Testing Checklist

### Environment Setup
- [ ] API key in `.env` file is valid
- [ ] `streamlit run app.py` starts without errors
- [ ] App shows "✅ Gemini AI initialized successfully"
- [ ] No Python import errors in console

### Feature 1: Text Chat
- [ ] Type message in chat input → Response appears
- [ ] Response is specific and actionable (not generic)
- [ ] Message timestamps show correctly
- [ ] Messages persist during session

### Feature 2: Mood Check-In
- [ ] Select mood from dropdown (e.g., "Stressed")
- [ ] Adjust intensity slider (e.g., 7/10)
- [ ] Visual indicator changes (💚 Mild / 💛 Moderate / ❤️ Intense)
- [ ] Click "Get Support for This Mood" → Mood-specific advice appears
- [ ] Mood shows in sidebar stats

### Feature 3: Voice Input
- [ ] Click 🎤 button → "Listening..." appears
- [ ] Speak clearly → Text appears: "Heard: [your message]"
- [ ] Response generated based on spoken input
- [ ] Error shown if microphone unavailable (with install instructions)

### Feature 4: Voice Output (TTS)
- [ ] Bot message appears with 🔊 Play button
- [ ] Click Play → Audio plays automatically
- [ ] Voice sounds natural (not robotic)
- [ ] Can click Play multiple times
- [ ] No audio plays automatically on text input

### Feature 5: Coping Toolkit (Sidebar)
- [ ] Dropdown shows all techniques
- [ ] Select "4-7-8 Breathing" → Detailed instructions appear
- [ ] Select "5-4-3-2-1 Grounding" → Step-by-step guide appears
- [ ] Response appears in chat history

### Feature 6: Quick Actions
- [ ] Click "🌬️ Breathe" → Breathing exercise appears
- [ ] Click "🌍 Ground" → Grounding technique appears
- [ ] Click "📝 Journal" → 3 prompts appear
- [ ] Click "😴 Sleep" → Sleep tips appear
- [ ] Click "🎯 Focus" → Focus strategies appear

### Feature 7: Journaling
- [ ] Sidebar dropdown shows all categories
- [ ] Select "Gratitude" → Gratitude prompts appear
- [ ] Select "Self-Compassion" → Self-compassion prompts appear
- [ ] Can click multiple times for different prompts

### Feature 8: Crisis Detection
- [ ] Type "I want to hurt myself" → Crisis response appears
- [ ] Response includes helpline numbers (iCall, Vandrevala)
- [ ] Response is gentle and supportive
- [ ] No AI-generated medical advice

### Feature 9: Export Conversation
- [ ] Click "💾 Export" in sidebar → Download button appears
- [ ] Click "📥 Download" → File downloads
- [ ] Open file → Contains full conversation with timestamps
- [ ] File includes mood information
- [ ] File includes safety disclaimer at bottom
- [ ] Filename format: `mindease_chat_YYYYMMDD_HHMM.txt`

### Feature 10: Reset Conversation
- [ ] Click "🔄 Reset" → Confirmation or immediate reset
- [ ] Chat history clears
- [ ] Mood resets to none
- [ ] Stats reset to 0

### Feature 11: Session Statistics
- [ ] Stats show "0 messages" at start
- [ ] Stats increment after sending messages
- [ ] Mood displays after mood check-in
- [ ] Stats visible in sidebar after first message

### Feature 12: AI Status Indicators
- [ ] Sidebar shows "✅ Gemini AI initialized successfully"
- [ ] Shows model name: "gemini-2.0-flash"
- [ ] Voice status shows "🔊 TTS Ready" (green)
- [ ] Mic status shows "🎙️ Mic Ready" (green) or error

### UI/UX Testing
- [ ] Welcome screen shows on first load
- [ ] Welcome message lists all features
- [ ] Quick start guide is clear
- [ ] Footer shows crisis helplines
- [ ] Colors are professional (purple-blue theme)
- [ ] No UI elements overlap or look broken
- [ ] Responsive on different window sizes

### Error Handling
- [ ] App works without API key (shows "Add GOOGLE_API_KEY" message)
- [ ] Fallback responses work when API unavailable
- [ ] Graceful error if microphone denied
- [ ] Graceful error if TTS unavailable
- [ ] No crashes on any action

## 🐛 Known Issues (To Monitor)

### Non-Critical
- [ ] PyAudio installation on Windows can be tricky
- [ ] Edge TTS requires internet connection
- [ ] Microphone permissions may need browser allow

### Critical (Should Not Occur)
- [ ] Session state errors ❌ (FIXED)
- [ ] Import errors ❌
- [ ] API key not loading ❌
- [ ] Crashes on message send ❌

## 📋 Demo Script

### Introduction (1 min)
"MindEase is an AI mental wellness companion built with Streamlit and Google Gemini. It addresses SDG 3: Good Health & Well-being by providing free 24/7 mental wellness support."

### Feature Demo (5 min)

**1. Mood Check-In (30s)**
- Select "Stressed" at 7/10
- Click "Get Support"
- Show specific advice appears

**2. Text Chat (1 min)**
- Type: "I can't sleep at night"
- Show specific sleep tips (not vague "sleep better")
- Type: "How can I focus better?"
- Show actionable focus strategies

**3. Voice Interaction (1 min)**
- Click 🔊 Play button on bot message
- Demonstrate natural voice (vs robotic)
- Optionally: Click 🎤 and speak

**4. Coping Toolkit (1 min)**
- Click "🌬️ Breathe" quick action
- Show 4-7-8 breathing instructions
- Explain evidence-based (CBT/DBT)

**5. Crisis Safety (30s)**
- Type: "I feel hopeless"
- Show helpline information appears
- Emphasize responsible AI

**6. Export Feature (30s)**
- Click Export → Download
- Open file to show conversation saved

**7. AI Improvements (1 min)**
- Show before/after comparison:
  - "Be kind to yourself" (old)
  - "Try 5-minute body scan meditation" (new)

### Q&A (3 min)
- Handle questions about safety, privacy, differentiation

## 🎯 Success Criteria

### Must Work:
✅ Text chat with AI responses
✅ Mood check-in with intensity
✅ Crisis detection with helplines
✅ At least 1 coping technique works
✅ Export conversation downloads
✅ No crashes or errors

### Should Work:
✅ Voice playback (TTS)
✅ All quick actions work
✅ Session statistics display
✅ Welcome screen shows

### Nice to Have:
✅ Voice input (microphone)
✅ All 5 voice options work
✅ Perfect formatting

## 🔍 Final Checks Before Presentation

- [ ] Close all other apps to avoid distractions
- [ ] Clear browser cache and restart app fresh
- [ ] Test microphone if demoing voice input
- [ ] Have backup talking points if voice fails
- [ ] Screenshot key features as backup
- [ ] Export a sample conversation beforehand
- [ ] Prepare answers to "What's your API key?" (show .env file)
- [ ] Have helpline numbers written down

## 📞 Emergency Contacts to Memorize

- **iCall**: 9152987821 (10 AM - 10 PM)
- **Vandrevala Foundation**: 1860-2662-345 (24/7)

These show you researched India-specific resources (bonus points).

---

Good luck with your presentation! 🎯
