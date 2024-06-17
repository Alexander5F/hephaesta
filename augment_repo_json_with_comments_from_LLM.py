import streamlit as st
from analyze_repo import read_code

def augment_repo_json_with_comments_from_LLM(repo_json, github_link):
    
    
    
    nLOC, code_string = read_code(repo_json, "load_custom_html_for_landing_page.py", github_link)
    print('\n\n\n nLOC:' + str(nLOC))
    print('\n\n\n code string:' + code_string)
    st.toast(f'nLOC: {nLOC}\ncode string: {code_string}')
    
    return repo_json