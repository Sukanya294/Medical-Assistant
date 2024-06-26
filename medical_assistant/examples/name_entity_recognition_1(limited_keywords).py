import nltk
import pandas as pd
from nltk import ne_chunk, word_tokenize, pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
import os
import re
import configparser

config = configparser.ConfigParser()
config.read('../config/config.ini')


def download_nltk_resources():
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')


def generate_absolute_path(relative_path):
    absolute_path = os.path.abspath(relative_path)
    return absolute_path


def extract_entities(text):
    entities = {
        'name': None,
        'age': None,
        'weight': None,
        'symptoms': None
    }

    # Extract name using regex pattern
    name_pattern = config.get('entity_recognition', 'name_pattern')
    match = re.search(name_pattern, text)
    if match:
        entities['name'] = match.group(1)

    # Extract age and weight using regex patterns
    age_pattern = config.get('entity_recognition', 'age_pattern')
    weight_pattern = config.get('entity_recognition', 'weight_pattern')
    age_match = re.search(age_pattern, text)
    weight_match = re.search(weight_pattern, text)
    if age_match:
        entities['age'] = age_match.group(1)
    if weight_match:
        entities['weight'] = weight_match.group(1)

    # Extract symptoms using keyword matching
    values = config.get('entity_recognition', 'symptoms_keywords').split(',')
    symptoms_keywords = [value.strip("[ ] '") for value in values]
    for keyword in symptoms_keywords:
        if keyword in text:
            entities['symptoms'] = keyword
            break

    return entities


def highlight_entities(text, entities):
    highlighted_text = text
    for key, value in entities.items():
        if value:
            highlighted_text = highlighted_text.replace(value, f'*{value}*')
    return highlighted_text


def main():
    entities_list = []
    for conversation_number in range(1, 6):
        input_file = generate_absolute_path(f'../examples/data/text_conversations/con_{conversation_number}.txt')
        output_file = generate_absolute_path(f'../examples/data/text_conversations_with_highlights/con_{conversation_number}_highlighted.txt')

        with open(input_file, 'r') as file:
            text = file.read()

        entities = extract_entities(text)
        highlighted_text = highlight_entities(text, entities)
        entities_list.append(entities)
        print(entities)

        with open(output_file, 'w') as file:
            file.write(highlighted_text)

        print(f'Named entities extracted and stored in {output_file}')

    df = pd.DataFrame(entities_list)
    excel_file_path = generate_absolute_path(f'../examples/data/excel_report/entities_data.xlsx')
    df.to_excel(excel_file_path, index=False)


if __name__ == "__main__":
    download_nltk_resources()
    main()
