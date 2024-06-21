import streamlit as st
import asyncio
import os
import time
from dotenv import load_dotenv

# Custom functions 
from repo_visualizer import visualiserepo
from stream_response import stream_response
from custom_html_for_only_chat import custom_html_for_only_chat
from gpt_response import gpt_response
from create_prompt_from_settings import create_prompt_from_settings
from render_message import render_message
from handle_streamed_input import handle_streamed_input
from check_and_delete_file_on_first_load import check_and_delete_file_on_first_load
from analyze_repo import create_json_of_interactions, read_code
from module_for_main import initialisation, create_custom_style, set_loggers, chain_of_thought_toggles, send_message
from add_context_to_user_prompt import add_context_to_user_prompt


# FUNCTIONS IN THIS FILE:
# main
# get_json_of_interactions
# handle_button_click

def set_page_config(): 
    st.set_page_config(
        page_title="Copilot on Steroids",
        page_icon='https://i.imgur.com/gEHSBXK.png',
        layout="wide",
        initial_sidebar_state="collapsed"  # Ensure sidebar is expanded
    )

def chain_of_thought_toggles():
        deep = st.toggle("ChatGPT overwhelmed? **Go deeper.** 🪼 ", value=st.session_state.deep)
        if deep and not st.session_state.deep:
            st.session_state.all_in = False
        st.session_state.deep = deep

        all_in = st.toggle("**Go all in** 🦾 (Will take a minute)", value=st.session_state.all_in)
        if all_in and not st.session_state.all_in:
            st.session_state.deep = False
        st.session_state.all_in = all_in
        
        if deep:
            st.session_state.iterations = 1
            st.toast("**Going deep.** Chain of thought activated.", icon="🪼")
        elif all_in:
            st.session_state.iterations = 2
            st.toast("**Going all in.** This will take a minute", icon="🦾")    

def get_json_of_interactions(github_link, repo_json=None):
    if repo_json is None:
        st.toast('Analyzing your codebase', icon="🛰️")
        repo_json = create_json_of_interactions(github_link)
        if repo_json is None:
            st.toast('Is the link correct?', icon="🐔")
        else:
            st.toast('Finished! Tell me what to do.', icon="🥒")
    return repo_json

def handle_button_click(prompt, settings):
    st.session_state.show_buttons = False # Ensure the button is hidden
    asyncio.run(handle_streamed_input(prompt, settings))

def main():    
    load_dotenv()
    initialisation()    
    set_page_config()
    set_loggers()
    custom_style = create_custom_style()
    st.markdown(custom_style, unsafe_allow_html=True)    
    left_column, middle_column, right_column = st.columns([1, 4, 1])

    with middle_column:
        settings = custom_html_for_only_chat()        
        
        chain_of_thought_toggles()

        github_link_placeholder = st.empty()
        github_link = st.chat_input('url to your github repo (optional)')
        if github_link:
            st.session_state.github_link = github_link
            if st.session_state.repo_json is None:
                st.session_state.repo_json = get_json_of_interactions(github_link)
            st.write(f'GitHub Link: {st.session_state.github_link}')
                        
        send_message(settings, st.session_state.github_link, st.session_state.repo_json)
        
    with right_column:
        st.write(' ')

if __name__ == "__main__":
    main()