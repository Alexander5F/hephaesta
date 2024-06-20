import streamlit as st
import json
from gpt_response import gpt_response
from get_text_between_tags import get_text_between_tags
from analyze_repo import read_code
from messages_to_string import messages_to_string

def prompt_for_instructor(repo_json=None):
    json_str = json.dumps(repo_json, indent=4)
    
    if repo_json is not None:    
        instructions = f"**Here's a Json that represents my codebase.**: \n\n {json_str} \n\n\n\n\n\n\n\n ___________________________\n"                
        instructions += '''           
        1. Consider what we're trying to accomplish here.                
        
        Choose up to 5 files that you'd like me to show to another LLm that will then be tasked with solving my task. I'll immediately and without looking run your answer through a string processing algorithm that will look for filenames, and return their source code to you. 
        
        For this to work, it's important to stick with a convention:
        Each filename has to go inside of html tags like this:
        
        <f>readme.rtfd</f>
        <f>main.py</f>
        <f>transcribe_audio.py</f>
        <f>styling.css</f>
        <f>structure.html</f>
        
        (Names from my example above are made up. Make sure to only provide filenames present in the json above). If there's a readme, that's always a good place to start.
        
        In case the source code of these functions has already been added to the conversation, don't duplicate these parts.
            
        Additionally, since you know the bigger picture of my codebase a little, give tips to the LLM pertaining to that, and place it inside of brackets:
        <tips> TIPS </tips>.
        
        Your tips should only be AT MOST a couple paragraphs long. In general, keep it short and tight to speed things up, and just guide the other LLM in solving the problem.
        When writing your tips, consider that the other LLM can't see the json file, and your tips can provide the required context.
        
        GitHub Copilot often produces subpar results:

        - Generates unrealistic code (hallucinates) 🤯
        - Hallucinates object methods that don't exist
        - Writes code with obvious bugs
        - Includes subtle, hard-to-detect bugs
        - Lacks context awareness and foresight
        - Struggles with complex code
        - Often breaks or removes existing functionalities when introducing new features

        I wrote code that uses two LLMs that chat with each other: one ("executor") 
        writes the code, while the other ("instructor", which is you) provides concise feedback, context, guidance by returning TIPS, as well as shows the executor pertinent source code for chosen files.
        
        The instructor is an expert coder who identifies and points out issues such as bugs, mistakes, incomplete adherence to user instructions, and offers tips for improvement. The instructor ensures the executor’s code does not break existing functionality and enforces best coding practices. Additionally, the instructor considers potential use cases and looks for likely untrue assumptions that the executor has made.
        The instructor aims to keep the executor on track, and 80/20's everything.
        
        '''
        
    elif repo_json is None:
        instructions = '''           
        1. Consider what we're trying to accomplish here.

        GitHub Copilot often produces subpar results:

        - Generates unrealistic code (hallucinates) 🤯
        - Hallucinates object methods that don't exist
        - Writes code with obvious bugs
        - Includes subtle, hard-to-detect bugs
        - Lacks context awareness and foresight
        - Struggles with complex code
        - Often breaks or removes existing functionalities when introducing new features

        I wrote code that uses two LLMs that chat with each other: one ("executor") 
        writes the code, while the other ("instructor", which is you) provides concise feedback, context, guidance by returning TIPS, as well as shows the executor pertinent source code for chosen files.
        
        The instructor is an expert coder who identifies and points out issues such as bugs, mistakes, incomplete adherence to user instructions, and offers tips for improvement. The instructor ensures the executor’s code does not break existing functionality and enforces best coding practices. Additionally, the instructor considers potential use cases and looks for likely untrue assumptions that the executor has made.
        The instructor aims to keep the executor on track, and 80/20's everything.
                                    
        I'll immediately and without looking run your answer through a string processing algorithm that will look for a specific html tag, and feed the content to the executor. For this to work, it's important to stick with a convention:
        Each filename has to go inside of html tags like this:
        <tips> TIPS </tips>.
        
        Your tips should AT MOST be a couple paragraphs long. In general, keep it short and tight to speed things up, and just guide the other LLM in solving the problem.
        '''
        
    print(instructions)    
    return instructions

def create_list_of_filenames(input_string):
    start_tag = "<f>"
    end_tag = "</f>"
    list_of_filenames = []
    seen_filenames = set()
    start_index = 0

    while True:
        start_loc = input_string.find(start_tag, start_index)
        if start_loc == -1:
            break
        end_loc = input_string.find(end_tag, start_loc + len(start_tag))
        if end_loc == -1:
            break
        filename = input_string[start_loc + len(start_tag):end_loc]
        if filename not in seen_filenames:
            list_of_filenames.append(filename)
            seen_filenames.add(filename)
        start_index = end_loc + len(end_tag)
    
    return list_of_filenames

def instructor(repo_json=None, github_link=None):
    messages = st.session_state.messages            
    prompt = prompt_for_instructor(repo_json)
    messages.append({"role": "user", "content": prompt, "displayed": False})
    st.toast("Thinking", icon = "🧠")

    messages_str = messages_to_string(messages)
    response = gpt_response(messages_str)
    print(f"gpt_response: {response}")  # Debug print
    
    if response is None:
        st.error("Failed to get a response from the LLM.")
        return
    
    response = response.replace("cloned_repo/", "") # removes "cloned_repo/"
    
    list_of_filenames = create_list_of_filenames(response)
    print(f"List of filenames: {list_of_filenames}")  # Debug print
    
    for filename in list_of_filenames:
        st.toast("Highly pertinent | " + filename, icon = "🪼")

    tips = get_text_between_tags(response, "tips")
    print(f"Tips: {tips}")  # Debug print

    pertinent_source_code = '\n\n__________________________\n'    
    for filename in list_of_filenames:
        nLOC, source_code_for_this_file = read_code(repo_json, filename, github_link)
        pertinent_source_code += f"Source code for {filename}: \n\n {source_code_for_this_file} \n\n\n\n_____________________________\n"        

    # Append the codestring to json_str     
    instructor_response = f"Here's source code from parts of the user's code repo that like are helpful: \n\n\n {pertinent_source_code}\n\n\n—————————————————————\n" 
    instructor_response += f"Some tips: \n\n\n {tips}."
    
    print(f"INSTRUCTOR_RESPONSE: {instructor_response}")  # Debug print
        
    st.session_state.messages.append({"role": "user", "content": instructor_response, "displayed": False})
    return