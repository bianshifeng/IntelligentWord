import json,os

def parse_response_json(json_path):
    with open(json_path,"r",encoding="utf8") as json_file:
        json_str = json_file.read()
        result = json.loads(json_str)
        word_list = result["data"]["wordList"]
        return word_list

# parse_response_json("../data/response.json")