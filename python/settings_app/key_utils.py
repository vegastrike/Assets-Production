acronyms = ['ai']

def format_key(key: str) -> str:
    """
    Formats a key by converting underscores to spaces, capitalizing the first letter of each word,
    and fully capitalizing words that are acronyms.

    Args:
        key (str): The input key to format.
        acronyms (list): A list of acronyms to check against.

    Returns:
        str: The formatted key.
    """
    words = key.replace('_', ' ').split()
    formatted_words = [
        word.upper() if word in acronyms else word.capitalize()
        for word in words
    ]
    return ' '.join(formatted_words)


# Test
if __name__ == "__main__":
    keys = ['ai','audio_in_cockpit']
    
    for key in keys:
        print(format_key(key))