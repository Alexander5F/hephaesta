import streamlit as st

def show_image_popup(image_url: str):
    popup_html = f"""
    <div id="popup" style="display: block; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.5); z-index: 1000; text-align: center;" onclick="hidePopup()">
        <img id="popup-image" src="{image_url}" style="max-width: 100%; max-height: 100%; margin: auto; position: absolute; top: 0; left: 0; bottom: 0; right: 0;" onclick="event.stopPropagation();">
    </div>

    <script>
        // Function to hide the popup
        function hidePopup() {{
            var popup = document.getElementById("popup");
            popup.style.display = "none";
        }}
    </script>
    """

    # Add the popup HTML and JavaScript to the Streamlit app
    st.markdown(popup_html, unsafe_allow_html=True)