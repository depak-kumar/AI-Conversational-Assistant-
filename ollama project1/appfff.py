# import streamlit as st
# import ollama
# import pyttsx3  # Offline TTS
# import speech_recognition as sr  # Offline Speech Recognition
# import time
# import os

# # Function to recognize voice input (Offline)
# def recognize_voice():
#     """Capture and convert voice input to text using offline CMU Sphinx."""
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.info("🎤 Speak now...")
#         try:
#             recognizer.adjust_for_ambient_noise(source)
#             audio = recognizer.listen(source, timeout=5)
#             text = recognizer.recognize_sphinx(audio)  # Offline recognition
#             return text
#         except sr.UnknownValueError:
#             return "⚠️ Could not understand audio."
#         except sr.RequestError:
#             return "⚠️ Speech recognition engine unavailable."

# # Function to generate AI response
# def generate_response(user_input, task_type, response_length):
#     """Generate AI response based on user input, task type, and response length."""
#     try:
#         adjusted_input = f"{user_input}\n\n[Provide a {response_length} response.]"
#         response = ollama.chat(
#             model="tinyllama:latest",
#             messages=[{"role": "user", "content": adjusted_input}]
#         )
#         return response['message']['content']
#     except Exception as e:
#         return f"Error: {e}"

# # Function to convert text to speech (offline)
# def text_to_speech(text, voice):
#     """Convert AI response to speech and provide playback/download options."""
#     try:
#         engine = pyttsx3.init()
#         voices = engine.getProperty('voices')
        
#         voice_index = 0 if voice == "Male" else 1
#         engine.setProperty('voice', voices[voice_index].id)

#         file_path = "response_audio.mp3"
#         engine.save_to_file(text, file_path)
#         engine.runAndWait()

#         with open(file_path, "rb") as audio_file:
#             st.audio(audio_file.read(), format="audio/mp3")
#             st.download_button("⬇️ Download Audio", audio_file, file_path, "audio/mpeg")
#     except Exception as e:
#         st.error(f"TTS Error: {e}")

# # Main Streamlit App
# def main():
#     st.set_page_config(page_title="AI Chat with Voice Input", layout="wide")

#     st.markdown("""<style>
#         .stTextInput>div>div>input { background-color: #f0f2f6; }
#         .stButton>button { background-color: #4CAF50; color: white; font-size: 16px; }
#         .stMarkdown { font-size: 18px; }
#     </style>""", unsafe_allow_html=True)

#     st.title("🤖 AI Assistant with Offline Voice & TTS")

#     with st.sidebar:
#         st.header("⚙️ Settings")
#         task_type = st.selectbox("Select AI Task", ["Conversational AI", "Text Generation", "Text Completion"])
#         response_length = st.selectbox("Response Length", ["Short", "Medium", "Long"], index=1)
#         voice = st.radio("Choose Voice", ["Male", "Female"], index=0)

#     user_input = st.text_area("💬 Enter your message:", height=120)

#     col1, col2, col3 = st.columns([1, 1, 1])
#     with col1:
#         generate_clicked = st.button("🚀 Generate Response")
#     with col2:
#         clear_clicked = st.button("🗑️ Clear Chat History")
#     with col3:
#         voice_input_clicked = st.button("🎤 Voice Input")

#     # Handle voice input
#     if voice_input_clicked:
#         with st.spinner("🎙️ Listening..."):
#             voice_text = recognize_voice()
#             st.text_area("🎙️ Recognized Text:", value=voice_text, height=100)
#             user_input = voice_text  # Use voice input as query

#     if clear_clicked:
#         st.session_state.chat_history = []

#     if generate_clicked and user_input.strip():
#         with st.spinner("AI is thinking..."):
#             time.sleep(1)
#             response = generate_response(user_input, task_type, response_length)
#             st.success("Response Generated!")
#             st.markdown(f"✍️ **AI Response:**\n\n> {response}")

#             if "chat_history" not in st.session_state:
#                 st.session_state.chat_history = []
#             st.session_state.chat_history.append({"user": user_input, "ai": response})

#     if "chat_history" in st.session_state and st.session_state.chat_history:
#         st.subheader("📜 Chat History")
#         for chat in reversed(st.session_state.chat_history[-5:]):
#             st.markdown(f"🧑 **You:** {chat['user']}")
#             st.markdown(f"🤖 **AI:** {chat['ai']}")
#             st.markdown("---")

#     if st.button("🔊 Read Response"):
#         if "chat_history" in st.session_state and st.session_state.chat_history:
#             text_to_speech(st.session_state.chat_history[-1]['ai'], voice)

#     st.markdown("**Made with ❤️ by Deepak Kumar**")

# if __name__ == "__main__":
#     main()

#  attached voice option


import streamlit as st
import ollama
import pyttsx3  # Offline TTS
import speech_recognition as sr  # Offline Speech Recognition
import os
import time

def recognize_speech():
    """Capture voice input and convert it to text (Offline)."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Speak now...")
        try:
            audio = recognizer.listen(source, timeout=5)  # Listen for 5 seconds
            text = recognizer.recognize_sphinx(audio)  # Offline recognition using PocketSphinx
            st.success(f"✅ Recognized: {text}")
            return text
        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio. Please try again.")
        except sr.RequestError:
            st.error("⚠️ Could not access the speech recognition system.")
    return ""

def generate_response(user_input, task_type, response_length):
    """Generate AI response based on user input, task type, and response length."""
    try:
        adjusted_input = f"{user_input}\n\n[Provide a {response_length} response.]"
        response = ollama.chat(
            model="tinyllama:latest",
            messages=[{"role": "user", "content": adjusted_input}]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error: {e}"

def text_to_speech(text, voice):
    """Convert AI response to speech and provide playback/download options."""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        # Adjust voice selection dynamically
        voice_index = 0 if voice == "Male" else 1
        engine.setProperty('voice', voices[voice_index].id)

        file_path = "response_audio.mp3"
        engine.save_to_file(text, file_path)
        engine.runAndWait()

        with open(file_path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")
            st.download_button("⬇️ Download Audio", audio_file, file_path, "audio/mpeg")
    except Exception as e:
        st.error(f"TTS Error: {e}")

def main():
    st.set_page_config(page_title="AI Chat & TTS", layout="wide")
    
    st.markdown("""
        <style>
            .stTextInput>div>div>input { background-color: #f0f2f6; }
            .stButton>button { background-color: #4CAF50; color: white; font-size: 16px; }
            .stMarkdown { font-size: 18px; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🤖 AI Conversational Assistant with TTS & Voice Input")

    with st.sidebar:
        st.header("⚙️ Settings")
        task_type = st.selectbox("Select AI Task", ["Conversational AI", "Text Generation", "Text Completion"])
        response_length = st.selectbox("Response Length", ["Short", "Medium", "Long"], index=1)
        voice = st.radio("Choose Voice", ["Male", "Female"], index=0)

    user_input = st.text_area("💬 Enter your message:", height=120)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        generate_clicked = st.button("🚀 Generate Response")
    with col2:
        clear_clicked = st.button("🗑️ Clear Chat History")
    with col3:
        voice_input_clicked = st.button("🎤 Voice Input")

    if clear_clicked:
        st.session_state.chat_history = []

    if voice_input_clicked:
        user_input = recognize_speech()  # Capture offline speech and convert to text

    if generate_clicked and user_input.strip():
        with st.spinner("AI is thinking..."):
            time.sleep(1)
            response = generate_response(user_input, task_type, response_length)
            st.success("Response Generated!")
            st.markdown(f"✍️ **AI Response:**\n\n> {response}")

            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            st.session_state.chat_history.append({"user": user_input, "ai": response})

    if "chat_history" in st.session_state and st.session_state.chat_history:
        st.subheader("📜 Chat History")
        for chat in reversed(st.session_state.chat_history[-5:]):  # Show last 5 messages
            st.markdown(f"🧑 **You:** {chat['user']}")
            st.markdown(f"🤖 **AI:** {chat['ai']}")
            st.markdown("---")

    if st.button("🔊 Read Response"):
        if "chat_history" in st.session_state and st.session_state.chat_history:
            text_to_speech(st.session_state.chat_history[-1]['ai'], voice)

    st.markdown("**Made with ❤️ by Deepak Kumar**")

if __name__ == "__main__":
    main()
