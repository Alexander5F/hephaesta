
import streamlit as st 

def initialize_session_states():
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