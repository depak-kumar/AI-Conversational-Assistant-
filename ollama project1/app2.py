import streamlit as st
import ollama
from gtts import gTTS
import os

# Function to generate AI response
def generate_response(user_input, task_type):
    try:
        response = ollama.chat(
            model="tinyllama:latest",
            messages=[{"role": "user", "content": user_input}]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error: {e}"

# Function for Text-to-Speech (TTS)
def text_to_speech(text, language_code):
    try:
        tts = gTTS(text=text, lang=language_code)
        file_path = "response_audio.mp3"
        tts.save(file_path)

        # Play the audio in Streamlit
        with open(file_path, "rb") as audio_file:
            st.audio(audio_file.read(), format="audio/mp3")

        # Provide download option
        st.download_button(
            label="Download Audio",
            data=open(file_path, "rb"),
            file_name="response_audio.mp3",
            mime="audio/mpeg"
        )
    except Exception as e:
        st.error(f"TTS Error: {e}")

# Streamlit UI
def main():
    st.set_page_config(page_title="TinyLlama AI", layout="wide")
    st.title("AI Conversational Assistant")

    # Sidebar settings
    with st.sidebar:
        st.subheader("Settings")
        
        # Language selection for TTS
        language_code_map = {"English": "en", "Spanish": "es", "French": "fr", "German": "de"}
        language = st.selectbox("Select TTS Language", list(language_code_map.keys()))
        language_code = language_code_map[language]

        # Task selection
        task_type = st.selectbox("Select Task Type", ["Conversational AI", "Text Generation", "Text Completion"])

    # User input
    user_input = st.text_area("Enter your message:", key="user_input")

    # Generate response
    if st.button("Generate Response"):
        if user_input:
            response = generate_response(user_input, task_type)
            st.subheader("AI Response")
            st.write(response)

            # Store chat history
            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []
            st.session_state.chat_history.append({"user": user_input, "model": response})

            # TTS Button
            if st.button("Read Aloud"):
                text_to_speech(response, language_code)

    # Display Chat History
    if "chat_history" in st.session_state:
        st.subheader("Chat History")
        for chat in st.session_state.chat_history:
            st.write(f"**User**: {chat['user']}")
            st.write(f"**Model**: {chat['model']}")

    st.subheader("Made by Deepak Kumar")

if __name__ == "__main__":
    main()
