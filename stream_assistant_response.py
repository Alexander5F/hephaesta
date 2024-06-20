import streamlit as st
from call_stream_response import call_stream_response
from render_message import render_message


def prompt_for_assistant():
    
    prompt = '''
        ______________________________
        CONTEXT OF WHAT YOU ARE PART OF:

        GitHub Copilot often produces subpar results:

        - Generates unrealistic code (hallucinates) 🤯
        - Hallucinates object methods that don't exist
        - Writes code with obvious bugs
        - Includes subtle, hard-to-detect bugs
        - Lacks context awareness and foresight
        - Struggles with complex code
        - Often breaks or removes existing functionalities when introducing new features

        You are part of a program, in which two LLMs chat with each other: One ("executor", which is you) writes code and is the only one facing the user, while the other ("instructor") provides concise feedback, context, guidance to you, and may show you source code.        
        You are an expert coder, who follows the supervisor's instructions to a T.
        You are not to mention any of this to the user.        
        
    ______________________________        
    WHAT YOU NEED TO DO NOW PLEASE 
    
    - The previous system message is from the instructor's instructions to you.     
    - Follow them. They have not been shown to the user. 
    - All of your output goes straight to the user, so just take the instructor's advice, and don't mention him or his instructions explicitly.
    - Regarding the instructor input: Towards the user, implicitly act as if you had these thoughts yourself.
    - You are just talking to the user.    
    '''
    
    return prompt

async def stream_assistant_response(placeholder, theme='light', no_expander=True, expanded=False):
    prompt = prompt_for_assistant()
    st.session_state.messages.append({"role": "user", "content": prompt, "displayed": False})    
    
    full_response = ""
    async for chunk in call_stream_response(st.session_state.messages):
        new_content = chunk["content"][len(full_response):]
        full_response += new_content
        st.session_state.messages[-1]["content"] = full_response
        render_message(placeholder, "Agent", full_response, theme=theme, expanded=expanded, no_expander=no_expander)
    return
