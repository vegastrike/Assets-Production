# A class to manage the configuration, both from user folder and from the assets folder.

import json
import os
import getpass
import platform

CONFIG_FILE_NAME = "config.json"

class ConfigData():
    def __init__(self, assets_config_filename: str, user_config_filename: str = None):
        self.assets_config_filename = os.path.join(assets_config_filename, CONFIG_FILE_NAME)
        self.user_config_filename = os.path.join(user_config_filename, CONFIG_FILE_NAME)

        with open(self.assets_config_filename, 'r') as file:
            self.assets_config = json.load(file)

        self.user_config = {}
        if os.path.exists(self.user_config_filename):
            with open(self.user_config_filename, 'r') as file:
                self.user_config = json.load(file)

    # Recursive has_key
    def _has_key(self, key: list[str], dict):
        if len(key) == 0:
            return False
        if len(key) == 1:
            return key[0] in dict
        if key[0] in dict:
            return self._has_key(key[1:], dict[key[0]])
        else:
            return False

    # Recursive get
    def _get(self, key: list[str], dict):
        if len(key) == 0:
            return None
        if len(key) == 1:
            if key[0] in dict:
                return dict[key[0]]
        if key[0] in dict:
            return self._get(key[1:], dict[key[0]])
        else:
            return None

    def get(self, key: list[str]):
        user_value = self._get(key, self.user_config)
        asset_value = self._get(key, self.assets_config)

        if user_value is not None:
            return user_value
        
        if asset_value is not None:
            return asset_value
            
        raise KeyError(f"Key '{" ".join(key)}' not found in user or assets configuration.")
        
    # Recursive set
    def _set(self, key: list[str], value, dict):
        if len(key) == 0:
            return
        if len(key) == 1:
            dict[key[0]] = value
            return

        if key[0] not in self.user_config:
            dict[key[0]] = {}
        
        self._set(key[1:], value, dict[key[0]])


    def set(self, key: list[str], value):
        self._set(key, value, self.user_config)


    def save_user_config(self):
        if self.user_config_filename is None:
            raise ValueError("User config filename is not set.")
        
        with open(self.user_config_filename, 'w') as file:
            json.dump(self.user_config, file, indent=4)
        
        print(f"User configuration saved to {self.user_config_filename}")






