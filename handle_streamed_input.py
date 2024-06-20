import streamlit as st

from instructor import instructor
from create_prompt_from_settings import create_prompt_from_settings
from render_message import render_message
from stream_assistant_response import stream_assistant_response
from stream_instructor_response import stream_instructor_response
from add_context_to_user_prompt import add_context_to_user_prompt  # Import the function here


async def handle_streamed_input(user_input, settings, prompt_augmentation=None, repo_json=None, github_link=None):
    # Display user message
    user_input_placeholder = st.empty()
    render_message(user_input_placeholder, "You", user_input, no_expander=True)

    # Append user input
    st.session_state.messages.append({"role": "user", "content": user_input, "displayed": False})
    st.session_state.run = True
    
    if repo_json is not None and github_link is not None:
        # Generate and append the augmented prompt
        instructor(repo_json, github_link)

    # Placeholders for responses
    assistant_placeholders = []
    instructor_placeholders = []
    progress_placeholders = []

    for _ in range(st.session_state.iterations):
        # Add placeholders for responses
        assistant_placeholder = st.empty()
        assistant_placeholders.append(assistant_placeholder)

        progress_placeholder = st.empty()
        progress_placeholders.append(progress_placeholder)

        #instructor_placeholder = st.empty()
        #instructor_placeholders.append(instructor_placeholder)

        # Get assistant response
        await stream_assistant_response(assistant_placeholder)
        st.session_state.messages.append({"role": "assistant", "content": prompt_augmentation, "displayed": False})

        doing_message = "🪼 Deep in thought"
        render_message(progress_placeholder, "Doing", doing_message, no_expander=True)

        # Get instructor response                
        if repo_json is not None and github_link is not None:        
            instructor(repo_json, github_link)
        else:
            instructor()
        #await stream_instructor_response(instructor_placeholder) # DEPRECATED 
        
    # Final response
    final_response_placeholder = st.empty()
    await stream_assistant_response(final_response_placeholder, no_expander=True)

    st.session_state.run = False
    st.session_state.show_buttons = False