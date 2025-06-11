import os_utils
from main_window import MainWindow
from app_config import AppConfig

if __name__ == "__main__":
    # First some housekeeping
    os_utils.change_to_python_settings_app_folder_if_needed()
    os_utils.append_subfolders_to_system_path()

    app_config = AppConfig()
    main_window = MainWindow(app_config=app_config)