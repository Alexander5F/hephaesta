import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.buy_me_a_coffee import button

button(username="alexmhayes", floating=True, width=221)

col1, col2, col3 = st.columns([0.1,10,0.1])
# Adjust the proportions of the columns

with col2: 
    
    # Use triple quotes for multi-line strings in markdown
    st.markdown("""       

    ## **🍩 The project**
    It's a one-man show for the first couple weeks, but intended to become a business.
    Happy for contributions: [https://github.com/Alexander5F/hephaesta](https://github.com/Alexander5F/hephaesta)        

    ## **🫀 Why**
    I used GPT-4 and Copilot a ton for coding, and got sick of having to babysit it. I wanted to send-and-forget. That sometimes works if I take 15 minutes to craft a prompt.

    Copilot kept giving me BS-code unprompted, hallucinates, and usually doesn't pull in the right context from my codebase.
        
    ## **🥒 Very fresh, but moving like crazy**
    This project started in June (2024).

    ## **👾 Me**
    I've been an entrepreneur for 12 years. I've founded startups making predictive controllers for high speed doors, space lasers, 🏭 sensors for quality control in automatic manufacturing lines, B2B platforms, to neural rendering software, and I love to code.

    ## **🪼 Feedback**
    What do you find useful, are missing, or unhappy with? Feel free to email me at autocoder@yahoo.com with:

        "Setup is confusing as hell"
        "I use it all day, thanks!"
        "Marry me" (I'm taken though)     

    """)

st.image('https://i.imgur.com/71WosNG.png', width=500)