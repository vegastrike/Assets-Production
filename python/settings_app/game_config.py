# A class to manage the configuration, both from user folder and from the assets folder.

import json
import os
import getpass
import platform
import copy

import app_config as ac

CONFIG_FILE_NAME = "config.json"

# A class to manage the configuration, both from user folder and from the assets folder.
# There are several design issues here:
# 1. The assets configuration is read-only, while the user configuration can be modified.
# 2. The user configuration can override the assets configuration.
# 3. The user configuration is saved to a file in the user folder.
# 4. The assets configuration is read from a file in the assets folder.
# 
# Thank you co-pilot for the initial blurb, but here is some meaningful text:
# 1. GameConfig is a dictionary of dedicated branches and leaves
# 2. Both branches and leaves support 'dirty' - meaning that user overrode assets
# 3. Every branch and leaf has a link to the parent to allow traversing up.
# This would allow changes in a leaf to propagate upward.


class ConfigBranch():
    def __init__(self, parent, key: str, asset_dict: dict, user_dict: dict = None):
        self.parent: ConfigBranch = parent
        self.key: str = key
        self.value = {}
        self.dirty: bool = False  # Indicates if this branch has been modified by the user

        for key, value in asset_dict.items():
            # Branch
            if isinstance(value, dict):
                # We have a user branch
                if user_dict != None and key in user_dict:
                    self.value[key] = ConfigBranch(parent = self, key = key, asset_dict = value, user_dict = user_dict[key])
                    dirty = True
                # No user branch
                else:
                    self.value[key] = ConfigBranch(parent = self, key = key, asset_dict = value)
            # Leaf
            else:
                # We have a user leaf
                if user_dict != None and key in user_dict:
                    self.value[key] = ConfigLeaf(parent = self, key = key, value = user_dict[key], original_value = value)
                    dirty = True
                # No user branch
                else:
                    self.value[key] = ConfigLeaf(parent = self, key = key, value = value, original_value = value)

    def set_dirty(self, dirty: bool):
        self.dirty = dirty
        if dirty and self.parent:
            self.parent.set_dirty(True)

    # Recursive get - gets the underlying value
    def get(self, key: list[str]):
        if not key or len(key) == 0:
            return None
        if len(key) == 1:
            if key[0] in self.value:
                return self.value[key[0]].value
        if key[0] in self.value:
            return self.value[key[0]].get(key[1:])
        else:
            return None
        
    # This gets the ConfigBranch or ConfigLeaf object
    def get_object(self, key: list[str]):
        if not key or len(key) == 0:
            return None
        if len(key) == 1:
            if key[0] in self.value:
                return self.value[key[0]]
        if key[0] in self.value:
            return self.value[key[0]].get_object(key[1:])
        else:
            return None
        
    def get_changes_dictionary(self):
        dict = {}
        for key, value in self.value.items():
            if not value.dirty:
                continue

            if isinstance(value, ConfigBranch):
                dict[key] = value.get_changes_dictionary()
            elif isinstance(value, ConfigLeaf):
                dict[key] = value.value
        return dict
        
    # Recursive has_key
    def has_key(self, key: list[str]):
        if not key or len(key) == 0:
            return False
        if len(key) == 1:
            return key[0] in self.value
        if key[0] in self.value:
            return self.value[key[0]].has_key(key[1:])
        else:
            return False

    # Recursive set
    def set(self, key: list[str], new_value):
        if len(key) == 1:
            self.value[key[0]].value = new_value
            self.value[key[0]].dirty = True
            self.dirty = True
            return
        
        if key[0] not in self.value:
            print(key)
            raise KeyError(f"{key[0]} not found in ConfigBranch. Cannot set value {new_value}.")
        
        self.value[key[0]].set(key[1:], new_value)
        self.dirty = True

    def print(self, tabs = ""):
        output = f"{tabs}{self.key}:\n"
        for key, value in self.value.items():
            output += value.print(tabs + "\t")
        if self.parent:
            return output
        else: 
            print(output)

    

class ConfigLeaf():
    def __init__(self, parent: ConfigBranch, key: str, value, original_value):
        self.parent = parent
        self.key = key
        self.value = value
        self.original_value = original_value  # Store the original value for comparison
        self.dirty = False  # Indicates if this leaf has been modified by the user

    def override_value(self, new_value):
        if new_value != self.original_value:
            self.set_dirty(True)
        else:
            # We can't traverse up for false, as other leaves may also be dirty
            self.dirty = False
        self.value = new_value

    def set_dirty(self, dirty: bool):
        self.dirty = dirty
        if dirty and self.parent:
            self.parent.set_dirty(True)

    # Returns a string for the recursion to add to the print function
    def print(self, tabs = ""):
        return f"{tabs}{self.key}: {self.value} {f"(original: {self.original_value})" if self.original_value != self.value else ""} {"dirty" if self.dirty else ""}\n"

class GameConfig(ConfigBranch):
    def __init__(self, assets_config_filename: str, assets_config: dict,
                 user_config_filename: str = None, user_config: dict = None):
        super().__init__(parent = None, key = None, asset_dict = assets_config, user_dict = user_config)
        
        self.assets_config_filename = assets_config_filename
        self.user_config_filename = user_config_filename
        
    def _recursive_get_merged_dictionary(self, assets_dict, user_dict, merged_dict):
        dirty = False
        for key, value in assets_dict.items():
            if isinstance(value, dict) or isinstance(value, list):
                if key in user_dict:
                    merged_dict[key] = {}
                    self.recursive_get_merged_dictionary(value, user_dict[key], merged_dict[key])
                else:
                    merged_dict[key] = assets_dict[key]
            else:
                if key in user_dict:
                    dirty = True
                    merged_dict[key] = (value, user_dict[key])
                else:
                    merged_dict[key] = value

        # Mark as dirty
        if dirty:
            merged_dict['__dirty__'] = True

    def recursive_get_merged_dictionary(self):
        merged_dict = {}
        return self._recursive_get_merged_dictionary(self.assets_config, self.user_config, merged_dict)


    def save_user_config(self):
        if self.user_config_filename is None:
            raise ValueError("User config filename is not set.")
        
        user_config = self.get_changes_dictionary()
        if len(user_config) == 0:
            print("No changes to save. User configuration is empty.")
            return
        
        with open(self.user_config_filename, 'w') as file:
            json.dump(self.get_changes_dictionary(), file, indent=4)
        
        print(f"User configuration saved to {self.user_config_filename}")


# The game_config singleton instance
# Don't initialize here. Let ??? do it.
game_config: GameConfig = None

def load_game_config():
    global game_config
    # Load the two config files
    assets_config_filename = os.path.join(ac.app_config.assets_folder, CONFIG_FILE_NAME)
    user_config_filename = os.path.join(ac.app_config.user_folder, CONFIG_FILE_NAME)

    with open(assets_config_filename, 'r') as file:
        assets_config = json.load(file)

    user_config = None
    if os.path.exists(user_config_filename):
        with open(user_config_filename, 'r') as file:
            user_config = json.load(file)

    game_config = GameConfig(
        assets_config_filename= assets_config_filename,
        user_config_filename= user_config_filename,
        assets_config=assets_config,
        user_config=user_config
    )

# Test Code
if __name__ == "__main__":
    # Sample dictionaries
    assets_config = {
        "branch1": {
            "subbranch1": {
                "leaf1": True,
                "leaf2": 3.14,
                "leaf3": 42,
                "leaf4": "Asset String 1"
            },
            "subbranch2": {
                "leaf1": False,
                "leaf2": 2.71,
                "leaf3": 84,
                "leaf4": "Asset String 2"
            }
        },
        "branch2": {
            "subbranch1": {
                "leaf1": True,
                "leaf2": 1.61,
                "leaf3": 21,
                "leaf4": "Asset String 3"
            },
            "subbranch2": {
                "leaf1": True,
                "leaf2": 0.99,
                "leaf3": 63,
                "leaf4": "Asset String 4"
            }
        },
        "branch3": {
            "subbranch3": {
                "leaf1": False,
                "leaf2": 9.91,
                "leaf3": 666,
                "leaf4": "Asset String 5"
            },
            "subbranch3": {
                "leaf1": False,
                "leaf2": 1090.99,
                "leaf3": 115,
                "leaf4": "Asset String 6"
            }
        }
    }

    user_config = copy.deepcopy(assets_config)
    del user_config["branch3"]
    del user_config["branch2"]["subbranch2"]
    del user_config["branch2"]["subbranch1"]["leaf1"]
    
    
    # Initialize GameConfig
    game_config = GameConfig(
        assets_config_filename="/path/to/assets",
        assets_config=assets_config,
        user_config_filename="/path/to/user",
        user_config=user_config
    )

    game_config.set(["branch2","subbranch1","leaf2"], 2.01)
    game_config.set(["branch2","subbranch1","leaf3"], 12)
    game_config.set(["branch2","subbranch1","leaf4"], "Modified")


    print(game_config.has_key(["branch2","subbranch1","leaf4"]))
    print(game_config.get(["branch2","subbranch1","leaf4"]))
    print(game_config.get_changes_dictionary())

    #print(user_config)

    # Example usage
    # print(config.get(["branch1", "subbranch1", "leaf1"]))  # Should print False (user override)
    # print(config.get(["branch1", "subbranch1", "leaf2"]))  # Should print 3.14 (asset value)
    # print(config.get(["branch1", "subbranch1", "leaf4"]))  # Should print "User String 1" (user override)
    # print(config.get(["branch2", "subbranch2", "leaf3"]))  # Should print 63 (asset value)

    game_config.print()


