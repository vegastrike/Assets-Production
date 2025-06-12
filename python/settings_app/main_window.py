import tkinter as tk
import tkinter.ttk as ttk
from ttkthemes import ThemedTk

#from PIL import Image, ImageTk

import tabs.graphics
import tabs.advanced

from setup_folders import FolderSetupWindow
import game_config as gc
import app_config as ac

# background image curtesy of Yihan Wang
# bg_image_name = "images/pexels-yihan-wang-2148192610-29990225.jpg"

# Create the main window
# os_utils.change_to_python_settings_app_folder_if_needed()

class MainWindow(ThemedTk):
    def __init__(self):
        super().__init__(theme=ac.app_config.theme)

        # Initialize the main window
        self.title("Vegastrike Settings")
        self.geometry("1200x800")
        #self.configure(bg="#2e2e2e")  # Set dark mode background color

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

        # Add graphics tab
        graphics_tab = tabs.graphics.GraphicsTab(self.notebook)
        self.notebook.add(graphics_tab.frame, text=graphics_tab.tab_name)

        # Add advanced tab
        advanced_tab = tabs.advanced.AdvancedTab(self.notebook)
        self.notebook.add(advanced_tab.frame, text=advanced_tab.tab_name)

        # Add content to the second tab
        # json = {"a": True, "B": False, "C": "Helo world", "D": 5, "e": 0.4}
        # config_to_gui.get_tab_data(tab2, json)

        bottom_buttons_row = tk.Frame(self, height=50)
        bottom_buttons_row.pack(pady=10)

        save_and_exit_button = ttk.Button(bottom_buttons_row, text="Save and Exit", command=lambda: self.do_save_and_exit())
        save_and_exit_button.pack(side="left", padx=5)

        exit_button = ttk.Button(bottom_buttons_row, text="Exit", command=lambda: self.do_exit())
        exit_button.pack(side="left", padx=5)

        #self.after(1000, self.check_config_file_paths)
        
        print("Main window initialized.")
        self.mainloop()


    def do_save_and_exit(self):
        gc.game_config.save_user_config()

        self.destroy()

    def do_exit(self):
        self.destroy()   

