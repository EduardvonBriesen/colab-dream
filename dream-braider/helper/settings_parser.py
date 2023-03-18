import yaml
import json
import random

def read_yaml(file_path):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def load_prompts(path):
    """
    Loads a json file from the specified directory and returns the parsed object.
    """
    parsed_content = ""
    with open(path, 'r') as file:
        parsed_content = json.load(file)
    return parsed_content

def load_json_to_array(path):
    with open(path, 'r') as file:
        return json.load(file)

def load_file_to_array(path):
    with open(path, 'r') as file:
        return file.read().splitlines()

def save_array_to_json(array):
    return json.dumps(array)

def modify_prompt_randomly(input: str) -> str:
    """Optimizes a given prompt with random predifined word groups.

    Takes a prompt and modifies it by adding a random, style forming word group and random negative keywords.
    
    @param input: The prompt to modify.
    """
    data = load_json_to_array("dream-braider\struct\prompt_specifiers.json")

    wordgroups = data['wordgroups']
    neg_keywords = data['neg_keywords']

    word_group = random.choice(wordgroups)
    manipulated_string = input + ', ' + word_group + ', --neg '

    for keyword_type in neg_keywords:
        keyword = random.choice(neg_keywords[keyword_type])
        manipulated_string += keyword + ', '
    return manipulated_string
