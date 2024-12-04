# Preserve changes to config by overwriting config.json with config.bak

import json
              

def recursive_overwrite(config_json, config_bak):
    if isinstance(config_bak, dict) or isinstance(config_bak, list):
        for key in config_bak:
            # The check is repeated because if we pass a leaf to recursive_overwrite
            # it is passed by value
            if isinstance(config_bak[key], dict) or isinstance(config_bak[key], list):
                recursive_overwrite(config_json[key], config_bak[key])
            else:
                config_json[key] = config_bak[key]
        


if __name__ == "__main__":
    config_bak = {}
    config_json = {}

    with open('config.bak') as file:
        config_bak = json.load(file)

    with open('config.json') as file:
        config_json = json.load(file)

    recursive_overwrite(config_json, config_bak)

    with open('config.json', 'w') as json_file: 
        json.dump(config_json, json_file, ensure_ascii=False, indent=4)

    print("Successfully overwrote config.json with your settings.")