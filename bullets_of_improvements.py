import streamlit as st
from call_stream_response import call_stream_response
from messages_to_string import messages_to_string 

async def bullets_of_improvements(messages, placeholder):
    conversation_history = messages_to_string(messages)
    internal_messages = []

    prompt = f"""
    CONVERSATION HISTORY
    {conversation_history}
    
    Compare the first code response to the most recent one, explaining why the most recent one is much 
    better. Your whole response should only be a couple bullet points.        
    """  
        
    internal_messages.append({"role": "user", "content": prompt, "displayed": False})
    
    assistant_response = {"role": "user", "content": "", "displayed": False}
    internal_messages.append(assistant_response)
    
    full_response = ""            
    async for chunk in call_stream_response(internal_messages):
        new_content = chunk["content"][len(full_response):]
        full_response += new_content
        assistant_response["content"] = full_response
        placeholder.markdown(f"""
        <div style='text-align: left; background-color: #e8f0fe; border-radius: 10px; padding: 10px; margin: 10px;'>
            <strong>Instructor:</strong> {full_response}
        </div>
        """, unsafe_allow_html=True)
        
    return internal_messages
