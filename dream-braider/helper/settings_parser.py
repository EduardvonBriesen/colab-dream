import yaml
import json
import random
import os
import re

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
    data = load_json_to_array("/home/ubuntu/colab-dream/dream-braider/struct/prompt_specifiers.json")

    wordgroups = data['wordgroups']
    neg_keywords = data['neg_keywords']

    word_group = random.choice(wordgroups)
    manipulated_string = input + ', ' + word_group + ', --neg '

    for keyword_type in neg_keywords:
        keyword = random.choice(neg_keywords[keyword_type])
        manipulated_string += keyword + ', '
    return manipulated_string

def get_init_image(folder: str) -> [bool, str]:
    """Returns the last image of the previous prompt.

    @param folder: The folder of the previous prompt.
    """
    try:
        init_image = ""
        first_run = False
        last_mod_time = 0
        image_extensions = [".jpg", ".jpeg", ".png", ".gif"]
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            if os.path.isfile(file_path) and any(filename.lower().endswith(ext) for ext in image_extensions):
                mod_time = os.path.getmtime(file_path)
                if mod_time > last_mod_time:
                    last_mod_time = mod_time
                    init_image = file_path

        # Check if system is windows for path conversion
        if os.name == 'nt':
            init_image = re.sub(r"[\\/]", r"\\\\", init_image)
    except:
        first_run = True

    return first_run, init_image
