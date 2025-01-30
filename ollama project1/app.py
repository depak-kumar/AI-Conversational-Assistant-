# # import streamlit as st
# # import ollama
# # from gtts import gTTS
# # import os

# # # Function to generate text or response from the model
# # def generate_response(user_input, task_type):
# #     try:
# #         response = ollama.chat(model="tinyllama:latest", messages=[{"role": "user", "content": user_input}])
        
# #         # Extracting the response based on task type
# #         if task_type == 'Conversational AI':
# #             return response['message']['content']
# #         elif task_type == 'Text Generation' or task_type == 'Text Completion':
# #             return response['message']['content']
# #         else:
# #             return "Unknown task type. Please select a valid task."
    
# #     except Exception as e:
# #         return f"Error: {e}"

# # # Function for Text-to-Speech (TTS)
# # def text_to_speech(text):
# #     tts = gTTS(text=text, lang='en')
# #     tts.save("response.mp3")
# #     os.system("start response.mp3")

# # # Streamlit UI
# # def main():
# #     st.set_page_config(page_title="TinyLlama Conversational AI", layout="wide")

# #     # Sidebar for instructions
# #     with st.sidebar:
# #         st.title("Instructions")
# #         st.write("""
# #         Welcome to the TinyLlama AI Demo!
        
# #         This application allows you to interact with an AI model for multiple tasks:
        
# #         - **Conversational AI**: Engage in a conversation with the AI.
# #         - **Text Generation**: Provide a prompt, and the model will generate text.
# #         - **Text Completion**: Input an incomplete sentence or paragraph, and the model will finish it.
        
# #         Select a task from the sidebar to start interacting with the model.
# #         """)

# #     # Select task from sidebar
# #     task_type = st.sidebar.selectbox(
# #         "Select Task Type",
# #         ["Conversational AI", "Text Generation", "Text Completion"]
# #     )

# #     st.title(f"{task_type} with TinyLlama")
    
# #     # Input for user query or text prompt
# #     if task_type == "Conversational AI":
# #         user_input = st.text_input("Your Message:")
# #     elif task_type == "Text Generation" or task_type == "Text Completion":
# #         user_input = st.text_area("Enter your prompt (or incomplete text):")

# #     # Button to submit the query or prompt
# #     if st.button("Submit"):
# #         if user_input:
# #             response = generate_response(user_input, task_type)
# #             st.write("Response from Model:", response)
# #             text_to_speech(response)  # Optional: Convert text to speech
# #         else:
# #             st.write("Please enter some text.")


import streamlit as st
import ollama
from gtts import gTTS
import io
import os

# Function to generate text or response from the model
def generate_response(user_input, task_type):
    try:
        response = ollama.chat(
            model="tinyllama:latest",
            messages=[{"role": "user", "content": user_input}]
        )
        return response['message']['content']
    except Exception as e:
        return f"Error: {e}"

# Function for Text-to-Speech (TTS) with Streamlit's audio player
def text_to_speech(text, language_code):
    try:
        # Generate TTS audio using gTTS
        tts = gTTS(text=text, lang=language_code)
        
        # Define a local file path to save the audio
        file_path = "response_audio.mp3"
        tts.save(file_path)

        # Confirm the file has been saved
        if os.path.exists(file_path):
            st.success("Audio has been successfully generated and saved locally.")

            # Play the audio using Streamlit
            with open(file_path, "rb") as audio_file:
                st.audio(audio_file.read(), format="audio/mp3")

            # Provide a download button for the audio file
            with open(file_path, "rb") as audio_file:
                st.download_button(
                    label="Download Audio",
                    data=audio_file,
                    file_name="response_audio.mp3",
                    mime="audio/mpeg"
                )
        else:
            st.error("Failed to save the audio file.")
    except Exception as e:
        st.error(f"Text-to-Speech Error: {e}")

# Function to handle feedback
def collect_feedback():
    st.subheader("Provide Your Feedback")

    # Dropdown options for point feedback
    options = ["Poor", "Average", "Good", "Very Good", "Excellent"]

    # Feedback for different aspects
    response_quality = st.selectbox("Rate the response quality:", options)
    # response_relevance = st.selectbox("Rate the relevance of the response:", options)
    # clarity_of_response = st.selectbox("Rate the clarity of the response:", options)

    # Additional comments
    additional_feedback = st.text_area("Any other comments or suggestions?")

    # Submit feedback button
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")
        st.write("### Feedback Summary")
        st.write(f"- **Response Quality**: {response_quality}")
        # st.write(f"- **Response Relevance**: {response_relevance}")
        # st.write(f"- **Clarity of Response**: {clarity_of_response}")

        if additional_feedback:
            st.write(f"- **Additional Comments**: {additional_feedback}")
        else:
            st.write("- **Additional Comments**: None provided.")

# Streamlit UI
def main():
    # st.header("ConversAI Nexus")
    st.set_page_config(page_title="TinyLlama Conversational AI", layout="wide")
    st.header("AI Conversational Platform")
    # Sidebar for instructions
    with st.sidebar:
        st.title("Instructions")
        st.write("""
        Welcome to the TinyLlama AI Demo!
        
        This application allows you to interact with an AI model for multiple tasks:
        
        - **Conversational AI**: Engage in a conversation with the AI.
        - **Text Generation**: Provide a prompt, and the model will generate text.
        - **Text Completion**: Input an incomplete sentence or paragraph, and the model will finish it.
        """)

        # Language selection for TTS
        language = st.selectbox("Select Language for TTS", ["English", "Spanish", "French", "German"])
        language_code_map = {"English": "en", "Spanish": "es", "French": "fr", "German": "de"}
        language_code = language_code_map[language]

        # Task selection
        task_type = st.selectbox("Select Task Type", ["Conversational AI", "Text Generation", "Text Completion"])

    # Layout for user input
    col1, col2 = st.columns([2, 1])

    with col1:
        # Batch input option
        uploaded_file = None
        if st.checkbox("Upload File for Batch Input"):
            uploaded_file = st.file_uploader("Choose a text file", type=["txt"])
        
        user_input = None
        if uploaded_file is not None:
            user_input = uploaded_file.read().decode("utf-8")
        else:
            # User input area
            if task_type == "Conversational AI":
                user_input = st.text_input("Your Message:")
            else:
                user_input = st.text_area("Enter your prompt (or incomplete text):")

    response = None
    with col2:
        # Button to generate response
        if st.button("Submit"):
            if user_input:
                response = generate_response(user_input, task_type)
                st.write("### Response from Model:")
                st.write(response)
            else:
                st.warning("Please enter some text.")

        # Button to read aloud
        if response and st.button("Read Aloud"):
            text_to_speech(response, language_code)

    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Append to chat history only if response exists
    if user_input and response:
        st.session_state.chat_history.append({"user": user_input, "model": response})
    
    # Display chat history
    st.subheader("Chat History")
    for chat in st.session_state.chat_history:
        st.write(f"**User**: {chat['user']}")
        st.write(f"**Model**: {chat['model']}")

    # Collect feedback
    collect_feedback()
    st.subheader("Made by Deepak Kumar")
if __name__ == "__main__":
   
    main()
    