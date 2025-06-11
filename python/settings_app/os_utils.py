import os
import screeninfo
import sys

# This file cannot be in the utils sub-folder where it belongs
def change_to_python_settings_app_folder_if_needed():
    # Check if we're running in the right folder
    current_folder = os.getcwd()
    expected_folder_suffix = "python/settings_app"
    if not current_folder.endswith(expected_folder_suffix):
        os.chdir(os.path.join(current_folder, expected_folder_suffix))
        print(f"Changed current working directory from {current_folder} to {os.getcwd()}")

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
    print(screens)
    return (screen.width, screen.height)

# Test section
if __name__ == "__main__":
    print(number_of_screens())
    resolution_for_screen(0)