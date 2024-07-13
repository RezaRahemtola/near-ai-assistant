import nltk


def calculate_token_length(text: str):
    """Determine the token length"""
    return len(nltk.word_tokenize(text))
