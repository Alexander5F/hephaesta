import time
import openai
import os
from dotenv import load_dotenv


def gpt_response(prompt):        
    load_dotenv() 
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    max_retry = 3
    retry_counter = 0
    modelversion = 'gpt-4o'
                    
    message_history = []

    if isinstance(prompt, str):        
        message_history.append({"role": "user", "content": prompt})

    elif isinstance(prompt, list):
        for message in prompt:
            if "content" in message:                                
                message_history.append(message)

    else:
        print(f"Data: {prompt}")
        print(f"Type : {type(prompt)}")
        print("Invalid prompt type. It must be a string or list of message objects.")
        return None
                    
    while retry_counter <= max_retry:
        try:
            response = openai.chat.completions.create( # "chat.completions" needs to stay this way
                model=modelversion,
                messages=message_history,
                stream=False,
            )
            return response.choices[0].message.content
        
        except Exception as e:
            if retry_counter < max_retry:
                print(f"   *** An error occurred ({str(e)}). Trying again in 300ms. ***")
                time.sleep(0.3)
                retry_counter += 1
            else:
                print("   *** Retry limit reached. Ending execution. ***")
                return None

# Test function
def test():
    prompt = 'How are ya?'
    response = gpt_response(prompt)
    print(response)

if __name__ == "__main__":
    test()
