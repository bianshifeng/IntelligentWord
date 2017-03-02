import json, os

from main import get_main_path


def config(key, value, config_file=get_main_path() + "/../data/config.json"):
    if not os.path.exists(config_file):
        open(config_file, "w").close()
    with open(config_file, "r+", encoding="utf8") as rc:
        crt_config = rc.read()

        if len(crt_config):
            config = json.loads(crt_config)
            config[key] = value
        else:
            config = {key: value}
        json.dump(config, fp=open(config_file, "w", encoding="utf8"))


def get_config(key, config_file=get_main_path() + "/../data/config.json"):
    if not os.path.exists(config_file):
        open(config_file, "w").close()
    with open(config_file, "r+", encoding="utf8") as rc:
        str = rc.read()
        if str:
            config_json = json.loads(str)
            if key in config_json:
                return config_json[key]
