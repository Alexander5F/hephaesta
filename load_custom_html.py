import streamlit as st
from streamlit_extras.buy_me_a_coffee import button

# Initialize session state for sidebar state

def load_custom_html():

    button(username="alexmhayes", floating=True, width=221)    
    left_column, right_column = st.columns([7, 0.1])







    with left_column:
            st.image('https://i.imgur.com/gEHSBXK.png', width=100) # icon
            st.write('# **HEPHAESTA** | *Shorter prompts. Better code.*')
            st.divider()
            
            # Correct path to the page                                    
            st.write("""

    ### **Usage**

                        📂 Give it your Github repo one time
        💬 Tell it to “Fix the stuff with the thing” in the chat

    **What it does**

                    🧠 Figures out which files to work on and pulls in the right context.
        🤖 A team of GPT-4o’s fixes it and criticises each other, to deliver better code than chatGPT, and without you babysitting. 
                    """
                    )
            st.divider()    
            st.write("""

    ### **Save an hour each day**
            ✍️ Short prompts are enough. It already has the context.
            🛋️ Lean back a few seconds and watch it self-improve.
            💩 Stop spending your day sifting through garbage code 
            🔧 It takes care not to drop existing functionalities when modifying
            🧠 Smarter than chatGPT
            🚀 Faster than chatGPT
            🔧 Fixes its own mistakes
            📚 Reads up on newest repos
            🔍 Doesn't break existing functionality 
                    """                
                    )                                        
            st.divider()
    
    
    
    
    
    
    
    
    
    
    
    st.sidebar.write("📣 Feedback | autocoder@yahoo.com")
    
    """
    with st.sidebar.expander("Settings", expanded=True): 
        settings = {            
            "find_mistakes": st.checkbox("🔧 Fix your own mistakes", value=True),
            "iterate_on_code": st.checkbox("🔁 Improve code iteratively", value=True),            
            "no_placeholders": st.checkbox("✍️ Write full code", value=True), 
            "optimise_speed": st.checkbox("🚀 Make code run faster", value=False),
            "dependency_analysis": st.checkbox("🔗 Save me from dependency hell", value=False),
            "read_documentation": st.checkbox("📚 Read newest repos", value=False),
        }
    return settings
    """