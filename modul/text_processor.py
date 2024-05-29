from model_loader import get_model, get_tokenizer, get_model_type
from yargy_rules import check_if_problem
from nltk_utils import split_large_sentence
from nltk.tokenize import sent_tokenize, word_tokenize
import torch
from itertools import groupby
from file_io import read_text_from_file

def process_text(file_path):
    model_type = get_model_type()
    model = get_model()
    tokenizer = get_tokenizer()
    if model_type == "t5":
        with open(file_path, 'r', encoding='utf-8') as file:
            document = file.read()
        sentences = sent_tokenize(document)
        results = []
        found_effects = False
        for sentence in sentences:
            if check_if_problem(sentence):
                found_effects = True
                words = word_tokenize(sentence)
                fragments = split_large_sentence(sentence) if len(words) > 70 else [sentence]
                sentence_effects = []
                for fragment in fragments:
                    inputs = tokenizer(fragment, return_tensors='pt')
                    with torch.no_grad():
                        hypotheses = model.generate(**inputs, num_beams=5, top_p=1.0, max_length=512)
                    s = tokenizer.decode(hypotheses[0], skip_special_tokens=True)
                    s = s.replace('; ', ';').replace(' ;', ';').lower().split(';')[:-1]
                    s = [el for el, _ in groupby(s)]
                    sentence_effects.extend(s)
                if sentence_effects:
                    effects_string = "; ".join(list(dict.fromkeys(sentence_effects)))
                    results.append(sentence + "\n" + effects_string + "\n\n")
        return ("".join(results), found_effects)
    else:
        # Use SpaCy for the bert model
        document = read_text_from_file(file_path)
        return ("\n".join(extract_entities(document)), True)

def extract_entities(text):
    model = get_model()
    doc = model(text)
    results = []
    for sentence in doc.sents:
        if check_if_problem(sentence.text):
            sentence_results = f"{sentence.text}\n"
            if sentence.ents:
                entities = ', '.join([f"{ent.text} ({ent.label_})" for ent in sentence.ents])
                sentence_results += f"Извлеченные фразы: {entities}\n"
            else:
                sentence_results += "No entities found.\n"
            results.append(sentence_results)
    return results
