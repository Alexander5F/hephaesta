import streamlit as st
from streamlit_extras.buy_me_a_coffee import button

# Initialize session state for sidebar state

def load_custom_html():
    custom_html = f"""
        <style>
            div[data-testid="column"]:nth-of-type(1) {{
                padding-right: 2rem;
            }}
            div[data-testid="column"]:nth-of-type(2) {{
                padding-left: 2rem;
            }}
            /* Custom CSS for the expander background color */
            div[role="group"] > div {{
                background-color: #ADD8E6 !important; /* Replace this with your desired CSS color */
            [data-testid="stSidebar"] > div:first-child {{
                width: 500px !important;
                transition: width 0.3s;
            }}
        </style>
    """
    
    button(username="alexmhayes", floating=True, width=221)
    
    st.markdown(custom_html, unsafe_allow_html=True)

    left_column, right_column = st.columns([7, 2])

    with left_column:
        st.write("")                
                    
    with right_column:
        st.write("")

    #st.sidebar.image("https://i.postimg.cc/6q36FdD0/icon.png", width=200)   # Cute logo        

    with st.sidebar.expander("Benefits", expanded=False):
        st.markdown("""
            - 🧠 Smarter    
            - 🚀 3x faster
            - 🔧 Fixes its own mistakes
            - 📚 Reads up on newest repos
            - 🔍 Doesn't break existing functionality
        """)
        

        # Show gif
        st.markdown(
            """
            <img src="https://s12.gifyu.com/images/SfIBy.gif" alt="GIF" style="width:0%">
            """,
            unsafe_allow_html=True,
        )        
        
    
    with st.sidebar.expander("Settings", expanded=False): 
        settings = {            
            "find_mistakes": st.checkbox("🔧 Fix own mistakes", value=True),
            "iterate_on_code": st.checkbox("🔁 Improve code iteratively", value=True),            
            "no_placeholders": st.checkbox("✍️ Write full code", value=True), 
            "optimise_speed": st.checkbox("🚀 Make code run faster", value=False),
            "dependency_analysis": st.checkbox("🔗 Save me from dependency hell", value=False),
            "read_documentation": st.checkbox("📚 Read newest repos", value=False),
        }

    with st.sidebar.expander("Feedback", expanded=False):
        st.write("Let's make this better. Please share your feedback with me: autocoder@yahoo.com.\n\n-Alex")

    return settings
    return settings