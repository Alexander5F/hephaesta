import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.buy_me_a_coffee import button

# Adding the 'Buy Me a Coffee' button
button(username="alexmhayes", floating=True, width=221)

# Creating columns with specified proportions
col1, col2, col3 = st.columns([0.1, 10, 0.1])

# Adjusting layout and content within the middle column
with col2:
    
    st.image('https://i.imgur.com/F4u8x0x.jpeg', width=200)
    st.write("## The project is now *Deepcode*.")
    st.markdown("[Go chat with Deepcode](https://deepcode.streamlit.app/)", unsafe_allow_html=True)
