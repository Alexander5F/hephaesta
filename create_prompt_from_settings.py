from settings_to_system_prompt import settings_to_system_prompt

def create_prompt_from_settings(settings):
    original_system_instructions = settings_to_system_prompt(settings)

    settings_prompt = (
            f"If the topic is code, please stick to the following instructions:\n\n"            
            f"START OF INSTRUCTIONS"
            f"{original_system_instructions}\n_________________________\n\n"                         
    )
             
    return settings_prompt