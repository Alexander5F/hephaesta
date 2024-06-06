import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
import logging
from repo_visualizer import visualiserepo
from initialize_session_state import initialize_session_state
from stream_response import stream_response
from load_custom_html_for_landing_page import load_custom_html_for_landing_page
from gpt_response import gpt_response
from settings_to_system_prompt import settings_to_system_prompt
from create_prompt_from_settings import create_prompt_from_settings
from render_message import render_message
from handle_streamed_input import handle_streamed_input
from check_and_delete_file_on_first_load import check_and_delete_file_on_first_load

# Set the page configuration first
st.set_page_config(
    page_title="Copilot on Steroids",
    page_icon='https://i.imgur.com/gEHSBXK.png',
    layout="wide",
    initial_sidebar_state="expanded"  # Ensure sidebar is expanded
)

logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

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
if 'first_load' not in st.session_state:
    st.session_state.first_load = True

def send_message():
    prompt = st.chat_input('"Fix the thing with the stuff"')
    if prompt:        
        st.page_link("pages/Be_notified_when_its_ready.py")

def handle_button_click(prompt):
    st.session_state.show_buttons = False  # Ensure the button is hidden
    st.page_link("pages/Be_notified_when_its_ready.py")

def main():
    load_custom_html_for_landing_page()
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

    left_column, middle_column, right_column = st.columns([0.1, 4, 1])

    with middle_column:
        text_col, button_col = st.columns([4, 1])

        with text_col:
            st.image("https://shorturl.at/BJldr", width=300) # Ron burgundy
            github_link = st.text_input("", value="", placeholder="url to your github repo")
        # Move button to be directly beneath the text input
        if st.button("Pull in my repo"):
            visualiserepo(github_link or "https://github.com/Alexander5F/hephaesta")
        st.write('#### Note: Currently only visualisation, and that is buggy. Loading the context into the conversation background will be here in the next days.')

        st.image("https://i.imgur.com/k9YDfOV.png", caption = "Example visualisation") # Visualisation
        st.divider()

        send_message()
        if st.session_state.show_buttons:
            if st.button("Let's goooooo  🚀"):
                handle_button_click("Write a web crawler")
        
        st.image("https://shorturl.at/OYSRU", width=300) # Let's go gif  

    with right_column:
        st.write(' ')                        

if __name__ == "__main__":
    main()