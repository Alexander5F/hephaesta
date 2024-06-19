import streamlit as st
from create_prompt_from_settings import create_prompt_from_settings
from render_message import render_message
from stream_assistant_response import stream_assistant_response
from stream_instructor_response import stream_instructor_response
from add_context_to_user_prompt import add_context_to_user_prompt  # Import the function here

async def handle_streamed_input(user_input, settings, prompt_augmentation=None, repo_json=None, github_link=None):
    # Append user input
    st.session_state.messages.append({"role": "user", "content": user_input, "displayed": False})
    st.session_state.run = True

    # Append settings as system prompt
    #settings_prompt = create_prompt_from_settings(settings)
    #st.session_state.messages.append({"role": "system", "content": settings_prompt, "displayed": False})

    if repo_json is not None and github_link is not None:
        # Generate and append the augmented prompt
        prompt_augmentation = add_context_to_user_prompt(repo_json, github_link, user_input)
        st.session_state.messages.append({"role": "system", "content": prompt_augmentation, "displayed": False})

    if prompt_augmentation is not None:
        st.session_state.messages.append({"role": "system", "content": prompt_augmentation, "displayed": False})

    # Display user message
    user_input_placeholder = st.empty()
    render_message(user_input_placeholder, "You", user_input, no_expander=True)

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

        instructor_placeholder = st.empty()
        instructor_placeholders.append(instructor_placeholder)

        # Get assistant response
        await stream_assistant_response(st.session_state.messages, assistant_placeholder)

        doing_message = "🔁 🤖 Improving my code"
        render_message(progress_placeholder, "Doing", doing_message, no_expander=True)

        # Get instructor response
        await stream_instructor_response(st.session_state.messages, instructor_placeholder)

    # Final response
    final_response_placeholder = st.empty()
    await stream_assistant_response(st.session_state.messages, final_response_placeholder, no_expander=True)

    st.session_state.run = False
    st.session_state.show_buttons = False