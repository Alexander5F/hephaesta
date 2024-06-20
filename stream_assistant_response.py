import streamlit as st
from call_stream_response import call_stream_response
from render_message import render_message

async def stream_assistant_response(placeholder, theme='light', no_expander=True, expanded=False):
    full_response = ""
    async for chunk in call_stream_response(st.session_state.messages):
        new_content = chunk["content"][len(full_response):]
        full_response += new_content
        st.session_state.messages[-1]["content"] = full_response
        render_message(placeholder, "Agent", full_response, theme=theme, expanded=expanded, no_expander=no_expander)
    return
