import streamlit as st
import streamlit.components.v1 as components
from streamlit_extras.buy_me_a_coffee import button


button(username="alexmhayes", floating=True, width=221)

# Embed the referral code
referral_code = """
<script src="https://b.kickoffpages.com/2.2.0/kol.js" id="koljs" data-campaign-id="181401" async></script>
<div data-kol-snippet="embedpage" data-kolPageId="385937" class="kol-embed-page-frame default" style="width: 100%;"></div>
"""

# Render the HTML
components.html(referral_code, height=600)
