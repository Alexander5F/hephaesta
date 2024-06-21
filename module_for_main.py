import streamlit as st
import logging
import asyncio
import time
from handle_streamed_input import handle_streamed_input

# FUNCTION DEFINITIONS IN HERE:
# initialisation()
# set_page_config()
# create_custom_style()
# set_loggers()
# chain_of_thought_toggles


def chain_of_thought_toggles():
    deep = st.toggle("**Dive deep** | Chain of thought 🪼 ")                
    all_in = st.toggle("**Even deeper** | More iterations 🪼") 
    
    if deep:
        st.session_state.iterations = 1
        st.toast("**Diving deep.** Chain of thought activated.", icon = "🪼")            
    
    if all_in:
        st.session_state.iterations = 2
        st.toast("**Bottom-of-the-ocean deep.** This will take 20s longer", icon = "🪼")

    st.write("")

# Initialize session states
def initialisation(): 
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
    if 'github_link' not in st.session_state:
        st.session_state.github_link = None
    if 'repo_json' not in st.session_state:
        st.session_state.repo_json = None
    if 'deep' not in st.session_state:
        st.session_state.deep = False
    if 'all_in' not in st.session_state:
        st.session_state.all_in = False        
        

def set_page_config(): 
    st.set_page_config(
        page_title="Copilot on Steroids",
        page_icon='https://i.imgur.com/gEHSBXK.png',
        layout="wide",
        initial_sidebar_state="collapsed"
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

def send_message(settings, github_link=None, repo_json=None):
    prompt = st.chat_input('"Make a webcrawler that avoids bot catchers" | "Speed up my code"')
    # check whether repo_json exists
    if prompt and repo_json is not None and github_link is not None:
        st.toast('Reading through all of your code', icon="📖")
        time.sleep(1)
        st.toast('Figuring out what\'s relevant', icon="🥒")        
        asyncio.run(handle_streamed_input(prompt, settings, repo_json, github_link))
        st.toast("Done", icon = "🍪")
    elif prompt and repo_json is None:
        st.toast('**Note** | You can add your repo link, and I\'ll consider it all while answering.', icon="🥷")
        asyncio.run(handle_streamed_input(prompt, settings))    
