from nltk.tokenize import word_tokenize

def split_large_sentence(sentence):
    words = word_tokenize(sentence)
    parts = []
    current_part = []
    for word in words:
        current_part.append(word)
        if len(current_part) >= 70:
            parts.append(" ".join(current_part))
            current_part = []
    if current_part:
        parts.append(" ".join(current_part))
    return parts
