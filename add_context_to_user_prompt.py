import streamlit as st
from analyze_repo import read_code
import json
from gpt_response import gpt_response
from get_text_between_tags import get_text_between_tags

def create_instructions_for_LLM(json_str, user_prompt):
    instructions_for_LLM = f"**Here's a Json that represents my codebase.**: \n\n {json_str}"
    instructions_for_LLM += ''' 
    
    
    
    
    _________________________
    What I want to accomplish:
    ''' 
    instructions_for_LLM += f"{user_prompt}"
        
    instructions_for_LLM += ''' 
    
    
    

    ________________________
    Please don't write any code unless I explicitly ask you to. Before we start with all that, please choose up to four files that you'd like me to show you that would help you solve my task.
    I'll immediately and without looking run your answer through a string processing algorithm that will look for filenames, and return their source code to you. 
    
    For this to work, it's important to stick with a convention:
    Each filename has to go inside of html tags like this:
    
    <f>render_messages.py</f>
    <f>main.py</f>
    <f>transcribe_audio.py</f>
    
    (Names from my example above are made up. Make sure to only provide filenames present in the json above).       
    '''
    return instructions_for_LLM

def add_context_to_user_prompt(repo_json, github_link, user_prompt):	
    
    # Have gpt look at the json, and return a list with up to n entries of filanmes.                
    json_str = json.dumps(repo_json)
    instructions_for_LLM = create_instructions_for_LLM(json_str, user_prompt)
    response = gpt_response(instructions_for_LLM)
    
    filenames = get_text_between_tags([response], 'f')

    context = '__________________________'
    # Loop over the list and append the code for the chosen files and iteratively append them to context
    for filename in filenames.split():
        nLOC, codestring = read_code(repo_json, filename, github_link)
        codestring = f"Source code for {filename}: \n\n {codestring} \n\n\n\n"        
        context += codestring

    # Append the codestring to json_str
    context = json_str + codestring
    augmented_prompt = f"What I want to accomplish \"{user_prompt}\". \n\n _______________________ " 
    augmented_prompt += f"Here's a json file representing my github repo, that explains some of the structure, "
    augmented_prompt += f"and for a likely relevant subset of files, the source code: \n\n" 
    augmented_prompt += f"{context}"        
    return augmented_prompt