import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
import logging
from repo_visualizer import visualiserepo
from stream_response import stream_response
from load_custom_html import load_custom_html
from gpt_response import gpt_response
#from settings_to_system_prompt import settings_to_system_prompt
from create_prompt_from_settings import create_prompt_from_settings
from render_message import render_message
from handle_streamed_input import handle_streamed_input
from check_and_delete_file_on_first_load import check_and_delete_file_on_first_load
from analyze_repo import analyze_repo, read_code
from module_for_main import *

# Set the page configuration first

load_dotenv()

def send_message(settings):
    prompt = st.chat_input('"Make a webcrawler that avoids bot catchers" | "Speed up my code"')
    if prompt:
        st.toast('🐝 **Already got started**')
        st.toast('🙈 **Relax your eyes for a few seconds**')
        asyncio.run(handle_streamed_input(prompt, settings))

def github_link_input():
    github_link = st.chat_input('url to your github repo')
    if github_link: 
        st.toast('👾 **Pulling repo**') 
        #png_filename = visualiserepo(github_link or "https://github.com/Alexander5F/hephaesta")
        #st.image('png_filename', caption='Codebase Structure Visualization')
        
        repo_json_for_LLM = analyze_repo(github_link)
        if repo_json_for_LLM is None:
            st.toast('🐔 **Is the link correct?**')
        else:    
            st.toast('🛰️ **Analyzing relationships**')
            nLOC, code_string = read_code(repo_json_for_LLM, "load_custom_html_for_landing_page.py", github_link)
            print('\n\n\n nLOC:' + str(nLOC))
            print('\n\n\n code string:' + code_string)
            st.toast(f'nLOC: {nLOC}\ncode string: {code_string}')
        
def handle_button_click(prompt, settings):
    st.session_state.show_buttons = False  # Ensure the button is hidden
    asyncio.run(handle_streamed_input(prompt, settings))

def main():
    call_initialisation()
    set_page_config()
    custom_style = create_custom_style()
    st.markdown(custom_style, unsafe_allow_html=True)

    left_column, middle_column, right_column = st.columns([1, 4, 1])

    with middle_column: 
        st.toast('🦑 **AI is ready**')
        settings = load_custom_html()    
        st.write('### **Give it a try**')
        #st.image('https://i.imgur.com/gEHSBXK.png', width=40) # icon        
        github_link_input()
        send_message(settings)

        # Display the output image from the visualiserepo function if exists
        check_and_delete_file_on_first_load()        
        output_image_path = "codebase_graph.png"
        if os.path.exists(output_image_path):  # assuming visualiserepo saves output to this file
            st.image(output_image_path)
        else:            
            st.image("https://i.imgur.com/k9YDfOV.png") # vizualisation placeholder png if viz hasn't been generated yet
            st.write('*Note*: Currently only visualisation, and that is buggy. Loading the context into the conversation background will be here in the next days.')
        st.divider()
        
        #clickable prompt
        #if st.session_state.show_buttons:
            #if st.button("Write a web crawler"):
                #handle_button_click("Write a web crawler", settings)
        
    with right_column:
        st.write(' ')

if __name__ == "__main__":
    main()