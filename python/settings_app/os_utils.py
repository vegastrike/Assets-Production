import os
import screeninfo
import sys

import app_config as ac

# This file cannot be in the utils sub-folder where it belongs
def change_to_python_settings_app_folder():
    os.chdir(os.path.join(ac.app_config.assets_folder, "python", "settings_app"))
    

def append_subfolders_to_system_path():
    subfolders = ['tabs', 'graphics_factory']
    current_folder = os.getcwd()
    for folder in subfolders:
        sys.path.append(os.path.join(current_folder, folder))

def number_of_screens():
    screens = screeninfo.get_monitors()
    return len(screens)

def resolution_for_screen(index):
    screens = screeninfo.get_monitors()
    screen = screens[index]
    return (screen.width, screen.height)

# Test section
if __name__ == "__main__":
    print(number_of_screens())
    resolution_for_screen(0)