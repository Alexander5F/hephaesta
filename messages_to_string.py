def messages_to_string(messages):
    messages_as_string = ''
    for message in messages:
        messages_as_string += f"{message['role']}:\n\n + {message['content']} ______________________\n\n\n\n"
    return messages_as_string