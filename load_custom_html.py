import streamlit as st
from streamlit_extras.buy_me_a_coffee import button

# Initialize session state for sidebar state

def load_custom_html():

    button(username="alexmhayes", floating=True, width=221)    
    left_column, right_column = st.columns([7, 2])

    with left_column:
        st.markdown('<div class="custom-text">HEPHAESTA</div>', unsafe_allow_html=True)        
        st.divider()
        
    
        st.write("""


**WHAT YOU DO**

                📂 Give it your Github repo one time
    💬 Tell it to “Fix the stuff with the thing” in the chat

**WHAT IT DOES**

                🧠 It figures out which files to work on and pulls in the right context.
    🤖 A team of GPT-4o’s fixes it and criticises each other, without you babysitting
    

                """
                
                
                
                )                
        st.divider()    
                          
    with right_column:
        st.write("")                    

    with st.sidebar.expander("Benefits", expanded=False):
        st.markdown("""
            - ✍️ Short prompts are enough. It already has the context.
            - 🛋️ Lean back a few seconds and watch it self-improve.
            - 💩 Stop spending your day sifting through garbage code.
            - 🔧 It takes care not to drop existing functionalities when modifying
        """)   
             
    with st.sidebar.expander("Benefitss", expanded=False):
        st.markdown("""
            - 🧠 Smarter    
            - 🚀 3x faster
            - 🔧 Fixes its own mistakes
            - 📚 Reads up on newest repos
            - 🔍 Doesn't break existing functionality
        """)                                    
        
    
    with st.sidebar.expander("Settings", expanded=False): 
        settings = {            
            "find_mistakes": st.checkbox("🔧 Fix own mistakes", value=True),
            "iterate_on_code": st.checkbox("🔁 Improve code iteratively", value=True),            
            "no_placeholders": st.checkbox("✍️ Write full code", value=True), 
            "optimise_speed": st.checkbox("🚀 Make code run faster", value=False),
            "dependency_analysis": st.checkbox("🔗 Save me from dependency hell", value=False),
            "read_documentation": st.checkbox("📚 Read newest repos", value=False),
        }

    with st.sidebar.expander("Feedback", expanded=True):
        st.write("Let's make this better. Please share your feedback with me: autocoder@yahoo.com.\n\n-Alex")

    return settings
