import openai
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def stream_response(messages):

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=True,
    )
    
    collected_messages = []
    for chunk in response:
        if hasattr(chunk.choices[0].delta, 'content'):
            chunk_message = chunk.choices[0].delta.content
            if chunk_message:
                collected_messages.append(chunk_message)
                response_text = ''.join(collected_messages)
                yield {"content": response_text}
        await asyncio.sleep(0)  # Yield control to the event loop