import streamlit as st
from call_stream_response import call_stream_response
from render_message import render_message

async def stream_assistant_response(messages, placeholder, theme='light', no_expander=False, expanded=False):
    full_response = ""
    async for chunk in call_stream_response(messages):
        new_content = chunk["content"][len(full_response):]
        full_response += new_content
        messages[-1]["content"] = full_response
        render_message(placeholder, "Agent", full_response, theme=theme, expanded=expanded, no_expander=no_expander)
    return messages
