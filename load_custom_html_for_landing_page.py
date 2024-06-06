import streamlit as st
from streamlit_extras.buy_me_a_coffee import button
import asyncio
import os
from dotenv import load_dotenv
import logging
from repo_visualizer import visualiserepo
from initialize_session_state import initialize_session_state
from stream_response import stream_response
from gpt_response import gpt_response
from settings_to_system_prompt import settings_to_system_prompt
from create_prompt_from_settings import create_prompt_from_settings
from render_message import render_message
from handle_streamed_input import handle_streamed_input
from check_and_delete_file_on_first_load import check_and_delete_file_on_first_load

def load_custom_html_for_landing_page():
    button(username="alexmhayes", floating=True, width=221)    
    left_column, right_column = st.columns([7, 2])

    with left_column:
        st.image('https://i.imgur.com/gEHSBXK.png', width=100) # icon
        st.write('# **HEPHAESTA** | *Jira ticket to pull request*')
        st.divider()
        
        # Correct path to the page
        st.page_link("pages/🔔 Be_notified_when_its_ready.py", label="**Be notified when it's ready**")
                                    
        st.write("""

### **Usage**

                    📂 Give it your Github repo one time
    💬 Tell it to “Fix the stuff with the thing” in the chat

**What it does**

                🧠 Figures out which files to work on and pulls in the right context.
    🤖 A team of GPT-4o’s fixes it and criticises each other, without you babysitting
                """
                )
        st.divider()    
        st.write("""

### **Save 1h every day**
        ✍️ Short prompts are enough. It already has the context.
        🛋️ Lean back a few seconds and watch it self-improve.
        💩 Stop spending your day sifting through garbage code 
        🔧 It takes care not to drop existing functionalities when modifying
        🧠 Smarter than chatGPT
        🚀 Faster than chatGPT
        🔧 Fixes its own mistakes
        📚 Reads up on newest repos
        🔍 Doesn't break existing functionality 
                """                
                )                                        
        st.divider()
                            
    with right_column:
        st.write("")       
                          
    with right_column:
        st.write("") 
    
    st.sidebar.write("Let's make this better. Please share your feedback with me: autocoder@yahoo.com.\n\n-Alex")
                                     
    return