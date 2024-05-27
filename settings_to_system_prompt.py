# To do (easy): Modify this to work with the new settings definition.
def settings_to_system_prompt(settings):
    read_documentation = False
    iterate_on_code = False
    find_mistakes = False
    optimise_speed = False
    dependency_analysis = False
    no_placeholders = False

    for setting, value in settings.items():
        if value:
            if setting == "read_documentation":
                read_documentation = True
            elif setting == "iterate_on_code":
                iterate_on_code = True
            elif setting == "find_mistakes":
                find_mistakes = True
            elif setting == "optimise_speed":
                optimise_speed = True
            elif setting == "dependency_analysis":
                dependency_analysis = True    
            elif setting == "no_placeholders":
                no_placeholders = True

    system_prompt = '''SYSTEM PROMPT
    General instructions: Be direct, concise. Straight to where it's juicy. Zone in on my question's intent. Simplify complex problems; explain the steps. Write clean, robust, modular code. Correct your errors. If the code calls an unknown function that would be helpful to see, ask the user to show it.

    POSSIBLE CHOICES BY USERS 
    **no_placeholders**: Code needs to be ready for the user to copy and paste, so no placeholders allowed.
    **read_documentation**: Browse the net for relevant documentation before writing any code.
    **optimise_speed**: Before answering, create a table with possible % speed optimisations for the user, and ask the users, which ones to implement.
    
    ACTUAL USER CHOICES
    '''
    
    system_prompt = system_prompt + (
        f"**no_placeholders**: {no_placeholders}\n"
        f"**read_documentation**: {read_documentation}\n"
        f"**optimise_speed**: {optimise_speed}\n"
        f"**iterate_on_code**: {iterate_on_code}\n"
        f"**find_mistakes**: {find_mistakes}\n"
        f"**dependency_analysis**: {dependency_analysis}\n"
    )

    return system_prompt
