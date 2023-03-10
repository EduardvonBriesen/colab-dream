import yaml
import json

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