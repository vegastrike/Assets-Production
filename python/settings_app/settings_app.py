import os_utils
import argparse

from main_app import MainApp
from setup_folders import check_config_file_paths
import app_config as ac
import game_config as gc
import os_utils

def main():
    # First some housekeeping
    os_utils.append_subfolders_to_system_path()

    parser = argparse.ArgumentParser(description="Vega Strike Settings Application")
    parser.add_argument(
        "-D", "--assets-dir",
        type=str,
        help="Path to the Vega Strike assets directory"
    )
    
    args = parser.parse_args()
    ac.app_config = ac.AppConfig(args.assets_dir)
    
    
    # Check if the user folder and assets folder are set up correctly
    success_configuring_file_paths = check_config_file_paths()

    if success_configuring_file_paths:
        gc.load_game_config()
        os_utils.change_to_python_settings_app_folder()
        ac.load_schema()

        # Create the main window
        MainApp().run()
    else:
        print("Failed to configure file paths. Exiting.")

if __name__ == "__main__":
    main()



