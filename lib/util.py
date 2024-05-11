import yaml

def retrieveFromYAML(path: str) -> dict:
    with open(path, 'r') as file:
        return yaml.safe_load(file)
        