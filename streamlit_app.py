import streamlit as st
import openai
import asyncio
from initialize_session_state import initialize_session_state
from stream_response import stream_response
from load_custom_html import load_custom_html
from gpt_response import gpt_response
import os
from dotenv import load_dotenv
from settings_to_system_prompt import settings_to_system_prompt
from create_prompt_from_settings import create_prompt_from_settings
from stream_assistant_response import stream_assistant_response
from stream_instructor_response import stream_instructor_response
from bullets_of_improvements import bullets_of_improvements
from final_code import final_code
from render_message import render_message

st.set_page_config(
    page_title="Copilot on Steroids",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load environment variables
load_dotenv()

# Debugging step: print the API key to verify it's loaded
st.write(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")

openai.api_key = os.getenv("OPENAI_API_KEY")


st.markdown("""
<style>
div.stButton {
    position: fixed;
    bottom: 50%;
    width: 100%;
    display: flex;
    justify-content: center;
    z-index: 9999;
}
[data-testid="stSidebar"][aria-expanded="true"] {
    transition: none;
    display: none;
}
[data-testid="stSidebar"][aria-expanded="false"] {
    transition: none;
}
</style>
""", unsafe_allow_html=True)

# Initialize session states
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'run' not in st.session_state:
    st.session_state.run = False
if 'counter' not in st.session_state:
    st.session_state.counter = 0
if 'show_buttons' not in st.session_state:
    st.session_state.show_buttons = True

async def handle_streamed_input(user_input, settings, iterations=1):
    # Append user input
    st.session_state.messages.append({"role": "user", "content": user_input, "displayed": False})
    st.session_state.run = True

    # Append settings as system prompt
    settings_prompt = create_prompt_from_settings(settings)
    st.session_state.messages.append({"role": "system", "content": settings_prompt, "displayed": False})

    # Display user message
    user_input_placeholder = st.empty()
    render_message(user_input_placeholder, "You", user_input, no_expander=True)

    # Placeholders for responses
    assistant_placeholders = []
    instructor_placeholders = []
    progress_placeholders = []
    
    for _ in range(iterations):
        # Add placeholders for responses
        assistant_placeholder = st.empty()
        assistant_placeholders.append(assistant_placeholder)

        progress_placeholder = st.empty()
        progress_placeholders.append(progress_placeholder)

        instructor_placeholder = st.empty()
        instructor_placeholders.append(instructor_placeholder)

        # Get assistant response
        await stream_assistant_response(st.session_state.messages, assistant_placeholder)
        
        doing_message = "🔁 🤖 Improving my code"
        render_message(progress_placeholder, "Doing", doing_message, no_expander=True)

        # Get instructor response
        await stream_instructor_response(st.session_state.messages, instructor_placeholder)

    # final response
    final_response_placeholder = st.empty()
    await stream_assistant_response(st.session_state.messages, final_response_placeholder, no_expander=True)
    
    st.session_state.run = False
    st.session_state.show_buttons = False

def send_message(settings):
    st.session_state.counter += 1
    prompt = st.chat_input("Challenge me")
    if prompt:
        asyncio.run(handle_streamed_input(prompt, settings))

def handle_button_click(prompt, settings):
    st.session_state.show_buttons = False  # Ensure the button is hidden
    asyncio.run(handle_streamed_input(prompt, settings))

def main():
    settings = load_custom_html()
    initialize_session_state()

    # Define the custom CSS style
    custom_style = """
    <style>
        .custom-text {
            font-family: 'Helvetica', sans-serif;
            font-size: 48px;
            letter-spacing: 5px;
            margin-bottom: 20px; /* Add this line to include margin */
        }
    </style>
    """

    # Inject the CSS style
    st.markdown(custom_style, unsafe_allow_html=True)

    left_column, middle_column, right_column = st.columns([2, 4, 2])
    
    with middle_column:        
        # Use the custom style in the markdown text
        st.markdown('<div class="custom-text">HEPHAESTA</div>', unsafe_allow_html=True)
        send_message(settings)

        if st.session_state.show_buttons:
            if st.button("Write a web crawler"):
                handle_button_click("Write a web crawler", settings)

    with right_column:
        st.empty()

if __name__ == "__main__":
    main()
