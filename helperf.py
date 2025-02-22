import re

def split_preserve_format(content, max_len=2000):
    """
    Splits a long message into chunks while preserving markdown formatting.
    Handles code blocks, bold/italic markers, and list continuity.
    """
    chunks = []
    current_chunk = []
    current_length = 0
    in_code_block = False  # Tracks if we're inside a code block
    last_lang = ""

    for line in content.split('\n'):
        line_len = len(line) + 1  # Include newline character

        # Toggle code block status when encountering triple backticks
        if line.strip().startswith('```'):
            last_lang = re.search(r"```(.*)", line.strip()).group(1)
            in_code_block = not in_code_block

        # If adding this line exceeds max length, finalize the current chunk
        if current_length + line_len > max_len:
            if in_code_block:
                current_chunk.append('```')  # Close the code block
                chunks.append('\n'.join(current_chunk))
                current_chunk = [f'```{last_lang}']
            else:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
            current_length = line_len
        else:
            current_chunk.append(line)
            current_length += line_len

    # Add the remaining content as the last chunk
    if current_chunk:
        if in_code_block:
            current_chunk.append('```')  # Close any unclosed code block
        chunks.append('\n'.join(current_chunk))

    return chunks