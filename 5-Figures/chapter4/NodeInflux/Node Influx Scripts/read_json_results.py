import json
from json import JSONDecodeError

def parse_results(path, first=True):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except JSONDecodeError:
        if not first:
            return None
        with open(path, "a") as f:
            f.write(']')
        return parse_results(path, False)