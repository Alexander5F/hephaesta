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
    Please don't write any code unless I explicitly ask you to. Before we start with all that, please choose up to five files that you'd like me to show to another LLm that will then be tasked with solving my task.
    I'll immediately and without looking run your answer through a string processing algorithm that will look for filenames, and return their source code to you. 
    
    For this to work, it's important to stick with a convention:
    Each filename has to go inside of html tags like this:
    
    <f>render_messages.py</f>
    <f>main.py</f>
    <f>transcribe_audio.py</f>
    
    (Names from my example above are made up. Make sure to only provide filenames present in the json above).       
    
    
    Additionally, since you know the bigger picture of my codebase a little, give tips to the LLM pertaining to that, and place it inside of brackets:
    <tips> TIPS </tips>. 
    
    Your tips should only be a couple paragraphs long.    
    '''
    return instructions_for_LLM

def create_list_of_filenames(input_string):
    start_tag = "<f>"
    end_tag = "</f>"
    list_of_filenames = []
    start_index = 0

    while True:
        start_loc = input_string.find(start_tag, start_index)
        if start_loc == -1:
            break
        end_loc = input_string.find(end_tag, start_loc + len(start_tag))
        if end_loc == -1:
            break
        list_of_filenames.append(input_string[start_loc + len(start_tag):end_loc])
        start_index = end_loc + len(end_tag)
    
    return list_of_filenames

        
def add_context_to_user_prompt(repo_json, github_link, user_prompt):	
    
    # Have gpt look at the json, and return a list with up to n entries of filanmes.                
    json_str = json.dumps(repo_json, indent=4)    
    instructions_for_LLM = create_instructions_for_LLM(json_str, user_prompt)
        
    response = gpt_response(instructions_for_LLM)
    response = response.replace("cloned_repo/", "") # removes "cloned_repo/"
    list_of_filenames = create_list_of_filenames(response)

    pertinent_source_code = '\n\n__________________________'
    # Loop over the list and append the code for the chosen files and iteratively append them to context
    tips = get_text_between_tags(response, "tips")
    
    for filename in list_of_filenames:
        nLOC, source_code_for_this_file = read_code(repo_json, filename, github_link)
        pertinent_source_code += f"Source code for {filename}: \n\n {source_code_for_this_file} \n\n\n\n_____________________________"        

    # Append the codestring to json_str     
    augmented_prompt = f"Here's source code from parts of the user's code repo that like are helpful: \n\n\n {pertinent_source_code}\n\n\n—————————————————————" 
    augmented_prompt += f"Some tips: \n\n\n {tips}."
    
    print("________________\n\n\n\n\LLM RESPONSE: \n\n\n\n" + response + "\n\n\n\n\n\n\n\n")
    print("________________\n\n\n\n\INSTRUCTIONS FOR LLM: \n\n\n\n" + instructions_for_LLM + "\n\n\n\n\n\n\n\n")
    print("________________\n\n\n\n\FILENAMES: \n\n\n\n" + str(list_of_filenames) + "\n\n\n\n\n\n\n\n")
    print("________________\n\n\n\n\TIPS: \n\n\n\n" + tips + "\n\n\n\n\n\n\n\n")
        
    print("________________\n\n\n\n\nAUGMENTED PROMPT: \n\n\n\n" + augmented_prompt + "\n\n\n\n\n\n\n\n")
    return augmented_prompt