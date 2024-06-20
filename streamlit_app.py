import streamlit as st
import asyncio
import os
import time
from dotenv import load_dotenv

# Custom functions 
from repo_visualizer import visualiserepo
from stream_response import stream_response
from load_custom_html import load_custom_html
from gpt_response import gpt_response
from create_prompt_from_settings import create_prompt_from_settings
from render_message import render_message
from handle_streamed_input import handle_streamed_input
from check_and_delete_file_on_first_load import check_and_delete_file_on_first_load
from analyze_repo import create_json_of_interactions, read_code
from module_for_main import call_initialisation, set_page_config, create_custom_style, set_loggers
from add_context_to_user_prompt import add_context_to_user_prompt

# FUNCTIONS IN THIS FILE:
# main
# send_message
# call_initialisation
# get_json_of_interactions
# handle_button_click

def send_message(settings, github_link=None, repo_json=None):
    prompt = st.chat_input('"Make a webcrawler that avoids bot catchers" | "Speed up my code"')
    # check whether repo_json exists
    if prompt and repo_json is not None and github_link is not None:
        st.toast('Reading through all of your code', icon="📖")
        time.sleep(1)
        st.toast('Figuring out what\'s relevant', icon="🥒")
        print('\n\n\n\n\n\n\n\n Entering augmented_prompt\n\n\n\n\n\n\n\n\n\n')
        prompt_augmentation = add_context_to_user_prompt(repo_json, github_link, prompt)
        print('\n\n\n\n\n\n\n\n Leaving augmented_prompt\n\n\n\n\n\n\n\n\n\n')
        with open('augmented_prompt.txt', 'w') as file:
            file.write(prompt + prompt_augmentation)
        print('\n\n\n\n\n\n\n\n writing augmented_prompt.txt to a file\n\n\n\n\n\n\n\n\n\n')
        st.toast('Done', icon="🛎️")
        asyncio.run(handle_streamed_input(prompt, settings, prompt_augmentation))
        st.toast("Done", icon = "🍪")
    elif prompt and repo_json is None:
        st.toast('**Note** | You can add your repo link, and I\'ll consider it all while answering.', icon="🥷")
        asyncio.run(handle_streamed_input(prompt, settings))    

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
    call_initialisation()    
    set_page_config()
    set_loggers()
    custom_style = create_custom_style()
    st.markdown(custom_style, unsafe_allow_html=True)    
    left_column, middle_column, right_column = st.columns([1, 4, 1])

    with middle_column:
        settings = load_custom_html()
        st.write('### **Give it a try**')
    
        if 'github_link' not in st.session_state:
            st.session_state.github_link = None
        if 'repo_json' not in st.session_state:
            st.session_state.repo_json = None
            
        github_link = st.chat_input('url to your github repo (optional)')
        if github_link:
            st.session_state.github_link = github_link
            if st.session_state.repo_json is None:
                st.session_state.repo_json = get_json_of_interactions(github_link)
            st.write(f'GitHub Link: {st.session_state.github_link}')
            
        on = st.toggle("Tough problem? **Boost.**")
        if on:
            st.session_state.iterations = 1
            st.toast("**Boost activated** for superior problem solving", icon = "🪼")
            
        send_message(settings, st.session_state.github_link, st.session_state.repo_json)
        
        check_and_delete_file_on_first_load()
        output_image_path = "codebase_graph.png"
        if os.path.exists(output_image_path):
            st.image(output_image_path)
        else:
            st.image("https://i.imgur.com/k9YDfOV.png")
            st.write('*Note*: Currently only visualisation, and that is buggy. Loading the context into the conversation background will be here in the next days.')
        st.divider()

    with right_column:
        st.write(' ')

if __name__ == "__main__":
    main()