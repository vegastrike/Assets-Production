import os
import tkinter as tk
from tkinter import ttk, filedialog
from ttkthemes import ThemedTk

from app_config import AppConfig
from config_data import ConfigData

CONFIG_FILE_NAME = "/config.json"

class FolderSetupWindow(tk.Toplevel):
    def __init__(self, app_config:AppConfig, config_data: ConfigData, root):
        super().__init__(root)

        self.app_config = app_config
        self.config_data = config_data
        self.root = root

        # Show on top of main screen
        # Doesn't actually work
        # TODO: figure out how to make the filedialog.askdirectory go on top of this
        #root.wm_attributes('-topmost', 1)

        self.success = False
        
        self.title("Setup Folders")
        self.geometry("640x480")

        # Variables for entry fields
        self.assets_entry_var = tk.StringVar(self, app_config.assets_folder)
        self.user_entry_var = tk.StringVar(self, app_config.user_folder)

        # Add a callback to validate when the assets_entry_var/user_entry_var changes
        self.assets_entry_var.trace_add("write", lambda *args: self.validate())
        self.assets_entry_var.trace_add("write", lambda *args: self.validate())

        if app_config.assets_folder != None:
            self.assets_entry_var.set(app_config.assets_folder)
        if app_config.user_folder != None:
            self.user_entry_var.set(app_config.user_folder)

        # Label and entry for the assets folder
        label1 = ttk.Label(self, text="Assets Folder:")
        label1.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry1 = ttk.Entry(self, textvariable=self.assets_entry_var, width=40)
        entry1.grid(row=0, column=1, padx=10, pady=5)
        button1 = ttk.Button(self, text="Browse...", command=self.select_assets_folder)
        button1.grid(row=0, column=2, padx=10, pady=5)

        # Label and entry for user folder
        label2 = ttk.Label(self, text="User Folder:")
        label2.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry2 = ttk.Entry(self, textvariable=self.user_entry_var, width=40)
        entry2.grid(row=1, column=1, padx=10, pady=5)
        button2 = ttk.Button(self, text="Browse...", command=self.select_user_folder)
        button2.grid(row=1, column=2, padx=10, pady=5)

        # OK and Cancel buttons
        self.ok_button = ttk.Button(self, text="OK", command=self.on_ok)
        self.ok_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")
        self.ok_button.state(['disabled'])  # Disable the OK button by default
        cancel_button = ttk.Button(self, text="Cancel", command=self.on_cancel)
        cancel_button.grid(row=2, column=2, padx=10, pady=10, sticky="w")


    def show_ask_directory(self, title):
        temp_root = tk.Tk()
        temp_root.withdraw()  # Hide the main window
        temp_root.attributes('-topmost', True)  # Make sure it's on top

        folder_selected = filedialog.askdirectory(parent=temp_root, title=title)
        
        temp_root.destroy()  # Clean up the temporary window
        return folder_selected

    def select_assets_folder(self):
        folder = self.show_ask_directory(title="Select Assets Folder")
        if folder:
            self.app_config.assets_folder = folder
            self.assets_entry_var.set(folder)
            

    def select_user_folder(self):
        folder = self.show_ask_directory(title="Select User Folder")
        if folder:
            self.app_config.user_folder = folder
            self.user_entry_var.set(folder)
            
           

    def on_ok(self):
        # TODO: better checks that the config file actually exists
        # if not, grey out the OK button
        self.destroy()

        self.app_config.serialize()
        self.root.lazy_load_config_data()
        self.root.lazy_load_graphics_tab()


    def on_cancel(self):
        self.assets_folder = None
        self.user_folder = None
        self.success = False

        self.destroy()

        print("Could not set up the folders correctly. Exiting.")
        exit(1)
        

    def validate(self):
        if not self.app_config.assets_folder or not self.app_config.user_folder:
            return 
        
        # The assets folder must exist and contain the config file
        # The user folder must exist but may not contain a config file
        if (not os.path.exists(os.path.join(self.app_config.assets_folder, CONFIG_FILE_NAME)) or 
           not os.path.exists(self.app_config.user_folder)):
            return 
        
        # If we reach here, both folders are valid and have a config file
        self.ok_button.state(['!disabled'])
        self.success = True

# Test Code
if __name__ == "__main__":
    dummy = FolderSetupWindow(
        assets_folder="path/to/assets",
        user_folder="path/to/user",
        user_config_filename="path/to/user_config.json"
    )

    print(dummy)



