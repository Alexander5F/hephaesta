import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
import logging
from repo_visualizer import visualiserepo
from initialize_session_state import initialize_session_state
from stream_response import stream_response
from load_custom_html import load_custom_html
from gpt_response import gpt_response
from settings_to_system_prompt import settings_to_system_prompt
from create_prompt_from_settings import create_prompt_from_settings
from render_message import render_message
from handle_streamed_input import handle_streamed_input

# Set the page configuration first
st.set_page_config(
    page_title="Copilot on Steroids",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

st.markdown("""
<style>
[data-testid="stSidebar"][aria-expanded="true"] {
    transition: none;
    display: none;
}
[data-testid="stSidebar"][aria-expanded="false"] {
    transition: none;
}
#expand-toggle {
    position: fixed; 
    top: 10px; 
    right: 10px; 
    z-index: 10000;
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
if 'expand_all' not in st.session_state:
    st.session_state.expand_all = True

def send_message(settings):
    prompt = st.chat_input("Challenge me")
    if prompt:
        st.session_state.show_buttons = False  # Ensure the button is hidden
        asyncio.run(handle_streamed_input(prompt, settings))

def handle_button_click(prompt, settings):
    st.session_state.show_buttons = False  # Ensure the button is hidden
    asyncio.run(handle_streamed_input(prompt, settings))

def toggle_expand_all():
    st.session_state.expand_all = not st.session_state.expand_all

def main():
    settings = load_custom_html()
    initialize_session_state()

    custom_style = """
    <style>
        .custom-text {
            font-family: 'Helvetica', sans-serif;
            font-size: 48px;
            letter-spacing: 5px;
            margin-bottom: 20px;
        }
    </style>
    """
    st.markdown(custom_style, unsafe_allow_html=True)

    left_column, middle_column, right_column = st.columns([1, 4, 1])

    with middle_column: 
        st.markdown('<div class="custom-text">HEPHAESTA</div>', unsafe_allow_html=True)        
        
        # the image and st.write below should be 
        st.image('https://i.imgur.com/gEHSBXK.png', width=40)
        
        
        text_col, button_col = st.columns([4, 1])

        with text_col:
            github_link = st.text_input("Fingerprint your repo and for code gen with stellar context awareness.", value="", placeholder="url to your github repo")
        st.write('Note: Currently only visualisation. Loading the context into the conversation background will be here in the next days.')
        # Move button to be directly beneath the text input
        if st.button("Visualize Repo"):
            visualiserepo(github_link or "https://github.com/Alexander5F/hephaesta")

        # Display the output image from the visualiserepo function if exists
        output_image_path = "codebase_graph.png"
        if os.path.exists(output_image_path):  # assuming visualiserepo saves output to this file
            st.image(output_image_path)
        else:
            # Show placeholder image if visualization hasn't been generated yet
            st.image("https://i.imgur.com/k9YDfOV.png")
        st.divider()
        send_message(settings)

        if st.session_state.show_buttons:
            if st.button("Write a web crawler"):
                handle_button_click("Write a web crawler", settings)

    with right_column:
        st.write(' ')

    with st.sidebar:
        st.session_state.expand_all = st.checkbox("Expand all messages", value=True)

    with st.container():
        st.markdown('<div id="expand-toggle"></div>', unsafe_allow_html=True)
        st.sidebar.button("Expand all outputs", on_click=toggle_expand_all)

if __name__ == "__main__":
    main()