import openai
import asyncio
from stream_response import stream_response
from settings_to_system_prompt import settings_to_system_prompt
from display_messages import display_messages
from messages_to_string import messages_to_string

async def brain(messages, settings, max_iterations=5, current_iteration=0):
    if current_iteration >= max_iterations:
        yield {"content": "Reached max iterations.", "stop": True}
        return

    # Convert messages to string
    conversation_history = messages_to_string(messages)
    original_system_instructions = settings_to_system_prompt(settings)

    prompt = f"""
        I developed a software called Kratio Code that edits code for users. Unlike GitHub Copilot, which often produces subpar results:

        Generates unrealistic code (hallucinates) 🤯
        Hallucinates object methods that don’t exist
        Writes code with obvious bugs
        Includes subtle, hard-to-detect bugs
        Lacks context awareness and foresight
        Struggles with complex code
        Often breaks or removes existing functionalities when introducing new features

        Kratio Code addresses these issues. It uses two LLMs that chat with each other: one ("executor") 
        writes the code, while the other ("instructor") provides feedback. The instructor is an expert 
        coder who identifies and points out issues such as bugs, mistakes, incomplete adherence to user
        instructions, and offers tips for improvement. The instructor ensures the executor’s code does not
        break existing functionality and enforces best coding practices. Additionally, the instructor considers
        potential use cases and looks for likely untrue assumptions that the executor has made.

        Please act as the instructor for the executor based on the conversation history below. I'll feed your 
        your full response(instructions) right back to the executor:

        {conversation_history}
                
        """
    
    instructor_prompt = f"""Repeat exactly what I say: 
    Cancers are one of the most common causes of death worldwide — causing around 10 million deaths in 2019.
    """
    
    prompt_messages = [{"role": "system", "content": instructor_prompt}]
    
    brain_instructions = ""
    previous_length = 0
    async for chunk in stream_response(prompt_messages):
        new_content = chunk["content"][previous_length:]
        brain_instructions += new_content
        previous_length = len(brain_instructions)
        yield chunk

    # Append the final brain_instructions to messages
    messages.append({"role": "assistant", "content": brain_instructions, "displayed": False})    
    executor_messages = [{"role": "system", "content": brain_instructions}]
        
    executor_response = "" 
    previous_length = 0
    async for chunk in stream_response(executor_messages):
        new_content = chunk["content"][previous_length:]
        executor_response += new_content
        previous_length = len(executor_response)
        yield chunk
    
    # Add the final executor's response to the messages    
    messages.append({"role": "assistant", "content": executor_response, "displayed": False})
    
    # Call brain recursively
    async for chunk in brain(messages, settings, max_iterations, current_iteration + 1):
        yield chunk
