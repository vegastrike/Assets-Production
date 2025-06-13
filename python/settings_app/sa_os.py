'''import platform
import os
import getpass
import json
import python.settings_app.os_utils as os_utils

def identify_os():
    os_name = platform.system()
    print(f"The operating system is: {os_name}")
    return os_name

def check_vegastrike_folder_linux():
    home_dir = os.path.expanduser("~")
    vegastrike_path = os.path.join(home_dir, ".vegastrike")
    folder_exists = os.path.isdir(vegastrike_path)
    config_json_exists = os.path.isfile(os.path.join(vegastrike_path, "config.json"))
    vegastrike_config_exists = os.path.isfile(os.path.join(vegastrike_path, "vegastrike.config"))
    return (folder_exists, config_json_exists, vegastrike_config_exists)

if __name__ == "__main__":
    os_name = identify_os()
    if os_name == "Windows":
        print("Running on Windows")
    elif os_name == "Linux":
        print("Running on Linux")
        configs = check_vegastrike_folder_linux()
        print(configs)
    elif os_name == "Darwin":
        print("Running on macOS")

def modify_settings_username():
    filename = "settings_app.json"
    os_list = ["windows", "linux", "darwin"]
    username = getpass.getuser()
    current_os = platform.system().lower()

    # Check if we're running in the right folder
    os_utils.change_to_python_settings_app_folder_if_needed()

    # Open the settings file 
    try:
        with open(filename, "r") as file:
            settings = json.load(file)

        # Check and update "first_run" flag
        if not settings.get("first_run", False):
            return
            
        settings["first_run"] = False

        # Remove settings for other OS and rename current to 'folders'
        for os_item in os_list:
            if os_item == current_os:
                settings['folders'] = settings[os_item]
            del settings[os_item]
        
        # Rename <user> to the real username
        for key, value in settings['folders'].items():
            if isinstance(value, str) and "<user>" in value:
                settings[key] = value.replace("<user>", username)

        with open(filename, "w") as file:
            json.dump(settings, file, indent=4)

        print("Settings updated successfully.")
    except Exception as e:
        print(f"An error occurred while modifying the settings: {e}")
    

# Call the function
modify_settings_username()'''