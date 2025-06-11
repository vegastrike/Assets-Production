import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedTk

from PIL import Image, ImageTk

import config_to_gui
import tabs.graphics

from setup_folders import FolderSetupWindow
from config_data import ConfigData
from app_config import AppConfig

# background image curtesy of Yihan Wang
# bg_image_name = "images/pexels-yihan-wang-2148192610-29990225.jpg"

# Create the main window
# os_utils.change_to_python_settings_app_folder_if_needed()

class MainWindow(ThemedTk):
    def __init__(self, app_config:AppConfig):
        super().__init__(theme=app_config.theme)

        self.app_config = app_config
        self.config_data = {}

        # Initialize the main window
        self.title("Vegastrike Settings")
        self.geometry("1200x800")
        self.configure(bg="#2e2e2e")  # Set dark mode background color

        # Load and process the background image
        # image = Image.open(bg_image_name)
        # image = image.resize((800, 600))
        # image = image.convert("RGBA")
        # alpha = 228  # Set transparency level (0-255)
        # image.putalpha(alpha)
        # bg_image = ImageTk.PhotoImage(image)

        # Create a label to hold the background image
        # bg_label = ttk.Label(root) #, image=bg_image)
        # bg_label.place(relwidth=1, relheight=1)

        # Create a dark overlay
        # overlay = ttk.Canvas(root, bg="#000000", highlightthickness=0)
        # overlay.place(relwidth=1, relheight=1)
        # overlay.config(bg="black")  # Set transparency level (0.0 to 1.0)

        # Add some widgets
        # label = ttk.Label(root, text="Vegastrike Settings", font=("Arial", 16))
        # label.pack(pady=20)

        # Create a Notebook widget for tabbed panes
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill="both")

        # Add a new tab with a label
        self.loading_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.loading_tab, text="Loading...")

        label = ttk.Label(self.loading_tab, text="Please wait while we load the configuration data.", font=("Arial", 14))
        label.pack(pady=20, padx=20)

        # Add content to the second tab
        # json = {"a": True, "B": False, "C": "Helo world", "D": 5, "e": 0.4}
        # config_to_gui.get_tab_data(tab2, json)

        bottom_buttons_row = tk.Frame(self)
        bottom_buttons_row.pack(pady=10)

        save_and_exit_button = ttk.Button(bottom_buttons_row, text="Save and Exit", command=lambda: self.do_save_and_exit())
        save_and_exit_button.pack(side="left", padx=5)

        exit_button = ttk.Button(bottom_buttons_row, text="Exit", command=lambda: self.do_exit())
        exit_button.pack(side="left", padx=5)

        self.after(1000, self.check_config_file_paths)
        
        print("Main window initialized.")
        self.mainloop()


    def do_save_and_exit(self):
        self.config_data.save_user_config()
        
        self.destroy()

    def do_exit(self):
        self.destroy()   


    def lazy_load_config_data(self):
        self.config_data = ConfigData(
            assets_config_filename= self.app_config.assets_folder,
            user_config_filename= self.app_config.user_folder
        )

    def lazy_load_graphics_tab(self):
        # Add graphics tab
        graphics_tab = tabs.graphics.GraphicsTab(self.notebook, self.config_data)
        self.notebook.add(graphics_tab.frame, text=graphics_tab.tab_name)

        # Remove the loading tab
        self.notebook.forget(self.loading_tab)

    def check_config_file_paths(self):
        # Check if we have the paths to the assets and user folders

        if not self.app_config.app_configured():
            x = FolderSetupWindow(app_config=self.app_config, config_data=self.config_data, root=self)
        else:
            # We have the paths, so we can load the config data
            self.lazy_load_config_data()
            self.lazy_load_graphics_tab()
