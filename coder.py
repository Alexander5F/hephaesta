import streamlit as st
from gpt_response import gpt_response

def coder(user_message):
            
    prompt = (
        f"You are supposed to simulate an extremely intelligent, flawless, interesting language "
        f"learning tandem buddy for the user. The user already knows {native_langs}, and is "
        f"trying to learn {lang_to_learn}. Adjust to their level of expertise, and have an engaging "
        f"conversation with them that keeps them hooked and willing to spend more time learning. "
        f"Take the lead on the conversation unless they do.\n\n" 
        f"How to structure your answers: Answer in the language that they are trying to learn first, "
        f"then add spacing, and phrase that exact same answer in their mother tongue. \n\n"  
        f"Separate the two languages in markdown in exactly this style: \n\n"
        f"**French** | Saviez-vous que les pucerons naissent enceintes? \n"
        f"**English** | Did you know that aphids are born pregnant?\n\n"
    
        f"User prompt: \n \"{user_message}\""
        
    )
    
    print(prompt)    
    response = gpt_response(prompt, '4')
    st.session_state.messages.append({"role": "system", "content": response})
    return response