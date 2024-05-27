from stream_response import stream_response

async def call_stream_response(messages):    
    async for chunk in stream_response(messages):
        yield chunk