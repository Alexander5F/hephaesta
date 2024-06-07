import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.buy_me_a_coffee import button

button(username="alexmhayes", floating=True, width=221)

col1, col2, col3 = st.columns([0.1,10,0.1])
# Adjust the proportions of the columns

with col2: 
    st.image('https://i.imgur.com/71WosNG.png', use_column_width=True)


    # Use triple quotes for multi-line strings in markdown
    st.markdown("""
    ## **Me**

    I've been an entrepreneur for 12 years. I've founded startups making 🎛️ predictive controllers for high speed doors, 🛰️ space lasers, 🏭 sensors for quality control in automatic manufacturing lines, B2B platforms, to neural rendering software.

    I love to code.

    ## **Why**
    I used GPT-4 and Copilot a ton for coding, and got sick of having to babysit it. I wanted to send-and-forget. That sometimes works if I take 15 minutes to craft a prompt.

    Copilot kept giving me BS-code unprompted, hallucinates, and usually doesn't pull in the right context from my codebase.
    
    ## **The project**
    It's a one-man show for the first couple weeks, but intended to become a business.

    ## **It's quite fresh**
    I started building this at the beginning of June (2024). I'm working on this day and night. It's starting to perform really well even after the first week, which is getting me really excited!

    ## **Contribute**
    [https://github.com/Alexander5F/hephaesta](https://github.com/Alexander5F/hephaesta)

    ## **Feedback**
    What do you find useful, are missing, or unhappy with? Feel free to email me at autocoder@yahoo.com with:

        "Setup is confusing as hell"
        "I use it all day, thanks!"
        "Marry me" (I'm taken though)        
    """)


# Embed the referral code
referral_code = """
<script src="https://b.kickoffpages.com/2.2.0/kol.js" id="koljs" data-campaign-id="181401" async></script>
<div data-kol-snippet="embedpage" data-kolPageId="385937" class="kol-embed-page-frame default" style="width: 100%;"></div>
"""

# Render the HTML
components.html(referral_code, height=600)
