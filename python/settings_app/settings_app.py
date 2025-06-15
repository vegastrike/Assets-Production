import os_utils
import platform

from main_window import MainWindow
from setup_folders import check_config_file_paths
import app_config as ac
import game_config as gc
import os_utils

if __name__ == "__main__":
    # First some housekeeping
    os_utils.append_subfolders_to_system_path()

    ac.app_config = ac.AppConfig()
    
    
    # Check if the user folder and assets folder are set up correctly
    success_configuring_file_paths = check_config_file_paths()

    if success_configuring_file_paths:
        gc.load_game_config()
        os_utils.change_to_python_settings_app_folder()

        # Create the main window
        main_window = MainWindow()
    else:
        print("Failed to configure file paths. Exiting.")



