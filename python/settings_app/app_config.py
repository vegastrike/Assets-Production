# This holds the configuration for the settings app.
# Primarily the assets folder and the app theme.
import platform
import getpass
import os
import json

CONFIG_FILE_SUFFIX = "config.json"
SETTINGS_APP_CONFIG_FILE_SUFFIX = "settings_app.json"

# Some setup to initialize the assets and user folders based on the platform.
initial_setup_locations = {
    "windows": {
        "assets_location": "C:\\Games\\.vegastrike\\Assets",
        "user_location": "C:\\Users\\<user>\\AppData\\Local\\.vegastrike"
    },
    "darwin": {
        "assets_location": "/Applications/.vegastrike/Assets",
        "user_location": "/Users/<user>"
    },
    "linux": {
        "assets_location": "/usr/share/vegastrike",
        "user_location": "/home/<user>/.vegastrike"
    }
}


def get_locations_for_platform():
    os_name = platform.system().lower()
    user_name = getpass.getuser()

    if os_name not in initial_setup_locations:
        raise ValueError(f"Unsupported platform: {os_name}")
    
    asset_location = initial_setup_locations[os_name]["assets_location"]
    user_location = initial_setup_locations[os_name]["user_location"].replace("<user>", user_name)

    # Ensure the directories exist
    if not os.path.exists(asset_location):
        print(f"Assets location does not exist: {asset_location}")
        asset_location = None
    else:
        print(f"Found assets at {asset_location}")

    if not os.path.exists(user_location):
        print(f"User folder does not exist: {user_location}")
        user_location = None
    else:
        print(f"Found user folder at {user_location}")

    return asset_location, user_location

class AppConfig:
    def __init__(self):
        self.assets_folder, self.user_folder = get_locations_for_platform()
        self.theme = "equilux" # Default theme, can be overridden by settings_app.json

        # User folder exists
        if self.user_folder != None:
            # Check if the settings_app.json exists
            # It holds the user defined assets folder location (and theme)
            self.settings_app_config_filename = os.path.join(self.user_folder, SETTINGS_APP_CONFIG_FILE_SUFFIX)

            if os.path.exists(self.settings_app_config_filename):
                with open(self.settings_app_config_filename, "r") as file:
                    app_settings = json.load(file)

                    self.assets_folder = app_settings.get("assets_folder", self.assets_folder)
                    self.theme = app_settings.get("theme", self.theme)

        # Create the user folder if it doesn't exist
        os_name = platform.system().lower()
        if self.user_folder is None and (os_name == "linux" or os_name == "darwin"):
            try:
                os.makedirs(self.user_folder, exist_ok=True)
                print(f"Created user folder at {self.user_folder}")
            except Exception as e:
                raise RuntimeError(f"Failed to create user folder at {self.user_folder}: {e}")


        # Can't continue if assets location is None
        if self.assets_folder is None or self.user_folder is None:
            return 

        # We can't recover from this. The assets folder is there but config.json isn't
        # Consider just returning and have the user deal with it.
        if not os.path.exists(os.path.join(self.assets_folder, CONFIG_FILE_SUFFIX)):
            raise FileNotFoundError(f"Assets location exists at {self.assets_folder} but config.json is missing. Please check your installation.")
        
    def serialize(self):
        # This shouldn't happen
        if self.user_folder is None or self.assets_folder is None:
            raise ValueError("Cannot serialize configuration. User folder or assets folder is not set.")
        
        json_struct = {
            "assets_folder": self.assets_folder,
            "theme": self.theme
        }

        with open(self.settings_app_config_filename, "w") as file:
            json.dump(json_struct, file, indent=4)

    def app_configured(self):
        # Returns True if the app is configured correctly, i.e. both assets and user folders are set.
        return self.assets_folder is not None and self.user_folder is not None

# The app_config singleton instance
# Don't initialize here. Let settings_app do it after changing folders.
app_config: AppConfig = None

# Test Code
if __name__ == "__main__":
    x = AppConfig()
    print(f"Assets folder: {x.assets_folder}")
    print(f"User folder: {x.user_folder}")
    print(f"Theme: {x.theme}")

    x.serialize()