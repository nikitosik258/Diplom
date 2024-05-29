import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import spacy

# Словарь для хранения моделей и токенизаторов
models = {}
tokenizers = {}

def load_models():
    # Загрузка моделей T5
    models["modelT5_large"] = T5ForConditionalGeneration.from_pretrained("modelT5_large")
    tokenizers["modelT5_large"] = T5Tokenizer.from_pretrained("modelT5_large")

    models["keyT5-custom_Large"] = T5ForConditionalGeneration.from_pretrained("keyT5-custom_Large")
    tokenizers["keyT5-custom_Large"] = T5Tokenizer.from_pretrained("keyT5-custom_Large")

    # Загрузка модели BERT с использованием SpaCy
    models["bert"] = spacy.load("model-best-sol")
    if not models["bert"].has_pipe("sentencizer"):
        models["bert"].add_pipe("sentencizer")

current_model = None
current_tokenizer = None
model_type = "t5"

def set_active_model(model_name):
    global current_model, current_tokenizer, model_type
    current_model = models[model_name]
    current_tokenizer = tokenizers.get(model_name)
    model_type = "bert" if model_name == "bert" else "t5"

def get_model():
    return current_model

def get_tokenizer():
    return current_tokenizer

def get_model_type():
    return model_type

# Вызов функции при инициализации модуля
load_models()
