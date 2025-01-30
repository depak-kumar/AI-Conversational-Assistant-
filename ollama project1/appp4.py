import streamlit as st
import ollama
from gtts import gTTS
import os
import time

def generate_response(user_input, task_type):
    """Generates AI response based on user input and task type."""
    try:
        response = ollama.chat(
            model="tinyllama:latest",
            messages=[{"role": "user", "content": user_input}]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error: {e}"

def text_to_speech(text, language_code):
    """Converts text to speech and provides playback & download options."""
    try:
        tts = gTTS(text=text, lang=language_code)
        file_path = "response_audio.mp3"
        tts.save(file_path)

        with open(file_path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")

        st.download_button("Download Audio", open(file_path, "rb"), "response_audio.mp3", "audio/mpeg")
    except Exception as e:
        st.error(f"TTS Error: {e}")

def main():
    st.set_page_config(page_title="AI Chat & TTS", layout="wide")
    st.markdown("""
        <style>
            .stTextInput>div>div>input { background-color: #f0f2f6; }
            .stButton>button { background-color: #4CAF50; color: white; font-size: 16px; }
        </style>
    """, unsafe_allow_html=True)

    st.title("✨ AI Conversational Assistant with TTS ✨")

    with st.sidebar:
        st.subheader("⚙️ Settings")
        language_map = {"English": "en", "Spanish": "es", "French": "fr", "German": "de"}
        language = st.selectbox("Select Language for TTS", list(language_map.keys()))
        task_type = st.selectbox("Select AI Task", ["Conversational AI", "Text Generation", "Text Completion"])
    
    user_input = st.text_area("💬 Enter your message:")

    if st.button("🚀 Generate Response"):
        if user_input.strip():
            with st.spinner("AI is thinking..."):
                time.sleep(1)  # Simulate loading
                response = generate_response(user_input, task_type)
                st.success("Response Generated!")
                st.write("✍️ **AI Response:**")
                st.markdown(f"> {response}")

                if "chat_history" not in st.session_state:
                    st.session_state.chat_history = []
                st.session_state.chat_history.append({"user": user_input, "ai": response})

    if "chat_history" in st.session_state:
        st.subheader("📜 Chat History")
        for chat in reversed(st.session_state.chat_history):
            st.write(f"🧑 **You:** {chat['user']}")
            st.write(f"🤖 **AI:** {chat['ai']}")
            st.markdown("---")

    if st.button("🔊 Read Response"):
        if "chat_history" in st.session_state and st.session_state.chat_history:
            last_response = st.session_state.chat_history[-1]['ai']
            text_to_speech(last_response, language_map[language])

    st.markdown("**Made with ❤️ by Deepak Kumar**")

if __name__ == "__main__":
    main()