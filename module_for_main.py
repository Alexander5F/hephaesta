import streamlit as st
import logging

# call_initialisation()
# set_page_config()
# create_custom_style()
# set_loggers()


# Initialize session states
def call_initialisation(): 
    if 'iterations' not in st.session_state:
        st.session_state.iterations = 0  
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

def set_page_config(): 
    st.set_page_config(
        page_title="Copilot on Steroids",
        page_icon='https://i.imgur.com/gEHSBXK.png',
        layout="wide",
        initial_sidebar_state="expanded"  # Ensure sidebar is expanded
    )

def create_custom_style():
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
    return custom_style

def set_loggers():
    logging.getLogger('asyncio').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('openai').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)
    logging.getLogger('fsevents').setLevel(logging.WARNING)        
