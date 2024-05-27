import streamlit as st

def initialize_session_state():
    if "run" not in st.session_state:
        st.session_state.run = False
