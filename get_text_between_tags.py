def get_text_between_tags(stream, start_tag, end_tag=None):
    if end_tag is None:
        end_tag = start_tag
    start_tag = "<" + start_tag + ">"
    end_tag = "</" + end_tag + ">"
    content = []
    buffer = ""
    
    def extract_content(buffer, start_tag, end_tag):
        start_index = 0
        while True:
            start_loc = buffer.find(start_tag, start_index)
            if start_loc == -1:
                break
            if end_tag:
                end_loc = buffer.find(end_tag, start_loc + len(start_tag))
                if end_loc == -1:
                    break
                content.append(buffer[start_loc + len(start_tag):end_loc])
                start_index = end_loc + len(end_tag)
            else:
                end_loc = buffer.find('<', start_loc + len(start_tag))
                if end_loc == -1:
                    break
                content.append(buffer[start_loc + len(start_tag):end_loc])
                start_index = end_loc
        return buffer[start_index:]
    
    for chunk in stream:
        buffer += chunk
        buffer = extract_content(buffer, start_tag, end_tag)
    
    # Process any remaining content in the buffer
    extract_content(buffer, start_tag, end_tag)
    
    return ''.join(content)
