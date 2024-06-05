import streamlit as st
import os

def check_and_delete_file_on_first_load():
    if 'first_load' not in st.session_state:
        st.session_state.first_load = True

    if st.session_state.first_load:
        output_image_path = "codebase_graph.png"
        if os.path.exists(output_image_path):
            os.remove(output_image_path)
        st.session_state.first_load = False