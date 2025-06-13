import tkinter as tk
import tkinter.ttk as ttk


import graphics_factory.label_control_pair as label_control_pair
import graphics_factory.graphic_attributes as graphic_attributes

import game_config as gc

from config_to_gui import generate_first_level_section
from graphics_factory.scrollable_frame import ScrollableFrame

class AdvancedTab:
    def __init__(self, parent):
        self.parent = parent
        self.tab_name = "Advanced"
        
        self.frame = ttk.Frame(parent)

        # Create two frames horizontally
        left_frame = ttk.Frame(self.frame)
        left_frame.configure(width=200, height=1000)
        left_frame.grid(row=0, column=0, sticky="nsew")
        left_frame.columnconfigure(0, weight=1) # stack widgets vertically

        left_inner_frame = ScrollableFrame(left_frame)

        self.right_frame = ttk.Frame(self.frame)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.config(borderwidth=2, relief="solid") # Add border
        self.right_frame.columnconfigure(0, weight=1) # stack widgets vertically

        # Configure grid weights for proper resizing
        self.frame.columnconfigure(0, weight=1, minsize=150)
        self.frame.columnconfigure(1, weight=5)
        self.frame.rowconfigure(0, weight=1)


        # Populate the left frame with config data
        for section, values in gc.game_config.value.items():
            label = ttk.Label(left_inner_frame, text=section, font=("Arial", 12))
            label.pack(anchor="w", padx=10, pady=5)
            label.bind("<Button-1>", self.on_label_click)
            

    def on_label_click(self, event):
        text = event.widget.cget('text')
        self.generate_right_frame(text)
        print(f"Clicked on section: {text}")

    def generate_right_frame(self, section_name: str):
        if self.right_frame:
            self.right_frame.destroy()

        self.right_frame = ttk.Frame(self.frame)
        self.right_frame.configure(width=600, height=1000)
        self.right_frame.grid(row=0, column=1, sticky="nsew")
        self.right_frame.config(borderwidth=2, relief="solid") # Add border
        self.right_frame.columnconfigure(0, weight=1) # stack widgets vertically

        # Populate the right frame with the first level section data
        section: gc.ConfigBranch = gc.game_config.get_object([section_name])
        if not section:
            return
        generate_first_level_section(self.right_frame, section)
    
        # Configure grid weights for proper resizing
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=5)
        self.frame.rowconfigure(0, weight=1)

    

        