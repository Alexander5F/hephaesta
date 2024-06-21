import streamlit as st

def render_message(placeholder, role, new_content, theme='light', expanded=False, no_expander=False):
    role_styles = {        
        "Agent": {
            "light": {
                "background_color": "#ffffff",
                "text_color": "#000000"
            },            
            "dark": {
                "background_color": "#302c2c",
                "text_color": "#ffffff"
            }
        },
        "Instructor": {
            "light": {
                "background_color": "#ffffff",
                "text_color": "#000000"
            },
            "dark": {
                "background_color": "#302c2c",
                "text_color": "#ffffff"
            }
        },
        "Doing": {
            "light": {
                "background_color": "#000000",
                "text_color": "#ffffff"
            },
            "dark": {
                "background_color": "#7100a7",
                "text_color": "#ffffff"
            }
        },
        "You": {
            "light": {
                "background_color": "#f4f4f4",
                "text_color": "#000000"
            },
            "dark": {
                "background_color": "#00678c",
                "text_color": "#ffffff"
            }
        }
    }

    styles = role_styles.get(role, {}).get(theme, {"background_color": "#ffffff", "text_color": "#000000"})

    if no_expander:
        placeholder.markdown(f"""
        <div style='text-align: left; background-color: {styles["background_color"]}; color: {styles["text_color"]}; border-radius: 10px; padding: 10px; margin: 10px;'>
            <strong>{role}:</strong> {new_content}
        </div>
        """, unsafe_allow_html=True)
    else:
        with placeholder.expander(f"{role}: ", expanded=expanded):
            st.markdown(f"""
            <div style='text-align: left; background-color: {styles["background_color"]}; color: {styles["text_color"]}; border-radius: 10px; padding: 10px; margin: 10px;'>
                {new_content}
            </div>
            """, unsafe_allow_html=True)
