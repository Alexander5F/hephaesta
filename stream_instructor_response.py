import streamlit as st
from call_stream_response import call_stream_response
from messages_to_string import messages_to_string 
from render_message import render_message
import streamlit as st
from call_stream_response import call_stream_response
from messages_to_string import messages_to_string 

async def stream_instructor_response(messages, placeholder, theme='light', no_expander=True):
    conversation_history = messages_to_string(messages)

    prompt = f"""
    I developed a software called Hephaesta that edits code for users. Unlike GitHub Copilot, which often produces subpar results:

    - Generates unrealistic code (hallucinates) 🤯
    - Hallucinates object methods that don't exist
    - Writes code with obvious bugs
    - Includes subtle, hard-to-detect bugs
    - Lacks context awareness and foresight
    - Struggles with complex code
    - Often breaks or removes existing functionalities when introducing new features

    Hephaesta Code addresses these issues. It uses two LLMs that chat with each other: one ("executor") 
    writes the code, while the other ("instructor") provides feedback. The instructor is an expert 
    coder who identifies and points out issues such as bugs, mistakes, incomplete adherence to user
    instructions, and offers tips for improvement. The instructor ensures the executor’s code does not
    break existing functionality and enforces best coding practices. Additionally, the instructor considers
    potential use cases and looks for likely untrue assumptions that the executor has made.

    Please act as the instructor for the executor based on the conversation history below. I'll feed your 
    full response (instructions) right back to the executor:

    {conversation_history}
    """  
    
    internal_messages = [{"role": "system", "content": prompt, "displayed": False}]
    messages.append({"role": "system", "content": "", "displayed": False})
    
    full_response = ""            
    async for chunk in call_stream_response(internal_messages):
        new_content = chunk["content"][len(full_response):]
        full_response += new_content
        messages[-1]["content"] = full_response
        render_message(placeholder, "Instructor", full_response)
        
    return internal_messages