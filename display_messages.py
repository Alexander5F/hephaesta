import streamlit as st

def display_messages(messages):
    for i, message in enumerate(messages):
        if not message.get('displayed', False):
            if message['role'] == 'assistant':
                if 'placeholder' not in message:
                    message['placeholder'] = st.empty()
                message['placeholder'].markdown(f"""
                <div style='text-align: left; background-color: #f1f1f1; border-radius: 10px; padding: 10px; margin: 10px;'>
                    <strong>AI:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            elif message['role'] == 'user':
                st.markdown(f"""
                <div style='text-align: left; background-color: #e8f0fe; border-radius: 10px; padding: 10px; margin: 10px;  margin-right: 0%; width: 50%;'>
                    <strong>You:</strong> {message['content']}
                </div>
                """, unsafe_allow_html=True)
            message['displayed'] = True
