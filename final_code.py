from render_message import render_message
import streamlit as st
from call_stream_response import call_stream_response
from messages_to_string import messages_to_string 

async def final_code(messages, placeholder, theme='light'):    
    internal_messages = messages

    prompt = f"""
    Full disclosure: I (who gave you the initial prompt), left the conversation right after your first response, and actually had my PA take over the chat as me.
    I just came back, and dont want to read through any previous convo, so please very very succinctly, as bullets, tell me what changed between your first code and the most recent version.
    """  
        
    internal_messages.append({"role": "system", "content": prompt, "displayed": False})
    internal_messages.append({"role": "system", "content": "", "displayed": False})
    
    full_response = ""            
    async for chunk in call_stream_response(internal_messages):
        new_content = chunk["content"][len(full_response):]
        full_response += new_content
        internal_messages[-1]["content"] = full_response
        render_message(placeholder, "Agent", full_response)
        
    return internal_messages
