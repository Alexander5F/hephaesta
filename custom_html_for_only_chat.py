import streamlit as st
from streamlit_extras.buy_me_a_coffee import button

# Initialize session state for sidebar state
        
def custom_html_for_only_chat():    
    
    if st.session_state.first_load:        
        st.toast("**For when GPT-4 can't hack it**", icon = "🪼")
        st.session_state.first_load = False    

    button(username="alexmhayes", floating=True, width=221)    
    left_column, right_column = st.columns([7, 0.1])

    with left_column:                            
        st.write("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")        
    
        st.image('https://i.imgur.com/F4u8x0x.jpeg', width=200) # Blue Jellyfish, more saturated colors                                                                         
        #st.image('https://i.imgur.com/VZlLzwj.png', width=200) # Alien Octopus         
        #st.image('https://i.imgur.com/k35QRvs.png', width=300) # Blue Jellyfish                        
        #st.image('https://i.imgur.com/OKuRojC.png', width=300) # Purple Jellyfish        
        #st.markdown("<h1 style='font-size: 200px;'>🍩</h1>", unsafe_allow_html=True)
        #st.image('https://i.imgur.com/kgqe1GO.png', width=200) # Doughnut
        #st.image('https://i.imgur.com/gEHSBXK.png', width=100) # Fingerprint            
        #st.image('https://i.imgur.com/VcPyudU.jpeg', width=200) # Peanut
        #st.image('https://i.imgur.com/zN8Jn5X.png', width=400) # Peanut                        
        
        st.write('## Deepcode | *Shorter prompts, better code*')
        #st.write('#### Understands the nuts and bolts of your code')         
        st.divider()           
    
    with st.sidebar.expander("Settings", expanded=True): 
        settings = {            
            "find_mistakes": st.checkbox("🍩 Fix your own mistakes", value=True),
            "iterate_on_code": st.checkbox("🐙 Improve code iteratively", value=True),            
            "no_placeholders": st.checkbox("🪼 No placeholders", value=True), 
            "optimise_speed": st.checkbox("🚀 Speed up my code", value=False),
            "dependency_analysis": st.checkbox("🔥 Save me from dependency hell", value=False),
            "read_documentation": st.checkbox("🥒 Retrieve fresh documentation", value=False),
        }
        
    st.sidebar.write("📣 Feedback | autocoder@yahoo.com")
    
    return settings