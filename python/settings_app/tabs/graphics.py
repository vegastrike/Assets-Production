import tkinter as tk
import tkinter.ttk as ttk
import screeninfo
import json
import os

import graphics_factory.label_control_pair as label_control_pair
import graphics_factory.graphic_attributes as graphic_attributes

from os_utils import number_of_screens, resolution_for_screen 

import game_config as gc

class GraphicsTab:
    def __init__(self, parent):
        self.parent = parent
        self.tab_name = "Graphics"
        self.num_screens = number_of_screens()
        self.screens = screeninfo.get_monitors()
        self.screen_resolution = resolution_for_screen(0)

        self.frame = ttk.Frame(parent)

        # Make primary screen the first one
        if len(self.screens) > 1:
            self.screens.sort(key=lambda screen: screen.is_primary, reverse=True)

        # Resolution options
        # Load resolutions from the JSON file
        with open(os.path.join("templates","resolutions.json"), "r") as file:
            self.all_resolutions = json.load(file)
        
        # Unlike other settings, here we set some defaults not based on assets
        # but on the current hardware 

        self.selected_screen = 0
        if gc.game_config.has_key(["graphics", "screen"]):
            self.selected_screen = gc.game_config.get(["graphics", "screen"])

        # We just check x but not y
        if gc.game_config.has_key(["graphics", "resolution_x"]):
            # Already have a resolution in user config, modify screen_resolution variable only
            self.screen_resolution = (
                gc.game_config.get(["graphics", "resolution_x"]),
                gc.game_config.get(["graphics", "resolution_y"])
            )
        else:
            # Don't have a resolution in user config, set it to the current max screen resolution
            gc.game_config.set(["graphics", "resolution_x"], self.screen_resolution[0])
            gc.game_config.set(["graphics", "resolution_y"], self.screen_resolution[1])

        # Full screen
        full_screen_control = label_control_pair.LabelCheckboxPair(
            parent=self.frame,
            key=["graphics", "full_screen"],
            text="Full Screen",
            attributes=graphic_attributes.GraphicAttributes(
                background="#2e2e2e",
                foreground="white",
                font="Arial",
                font_size=12,
                padding_x=5,
                padding_y=10,
                alignment=tk.LEFT
            ),
            initial_value=gc.game_config.get(["graphics", "full_screen"])
        )

        # Screens
        screens_control = label_control_pair.LabelComboboxPair(
            parent = self.frame,
            key = ["graphics","screen"],
            text = "Screen",
            attributes = graphic_attributes.GraphicAttributes(
                background="#2e2e2e",
                foreground="white",
                font="Arial",
                font_size=12,
                padding_x=5,
                padding_y=10,
                alignment=tk.LEFT
            ),
            options=[screen.name for screen in self.screens],
            initial_value=self.screens[0].name,
            on_change=self.on_change_screen
        )

        # Resolutions
        resolutions_control = label_control_pair.ResolutionPair(
            parent=self.frame,
            first_key=["graphics", "resolution_x"],
            second_key=["graphics", "resolution_y"],
            text="Resolution",
            attributes=graphic_attributes.GraphicAttributes(
                background="#2e2e2e",
                foreground="white",
                font="Arial",
                font_size=12,
                padding_x=5,
                padding_y=10,
                alignment=tk.LEFT
            ),
            resolutions = self.available_resolutions(self.selected_screen),
            initial_value= self.get_resolution_for_width(self.screen_resolution[0])
        )

    def get_index_for_screen(self, screen_name):
        for index, screen in enumerate(self.screens):
            if screen.name == screen_name:
                return index
        return 0

    def on_change_screen(self, screen_name):
        # Handle screen change logic here
        self.selected_screen = self.get_index_for_screen(screen_name)
        self.screen_resolution = resolution_for_screen(self.selected_screen)
        gc.game_config.set(["graphics", "screen"], self.get_index_for_screen(screen_name))

    def available_resolutions(self, index: int):
        # This may fail to get the max resolution if the screen is set by the OS to a lower resolution
        width, height = resolution_for_screen(index)

        available_resolutions = {text: resolution for text, resolution in self.all_resolutions.items() 
                                 if resolution[0] <= width and resolution[1] <= height}

        return available_resolutions

    def get_max_resolution(self, index: int):
        # This works because we are running python > 3.7 and
        # "Python dictionaries are inherently unordered prior to version 3.7. 
        # However, since Python 3.7, dictionaries maintain the order of insertion."
        return list(self.available_resolutions(index).keys())[-1]

    def get_resolution_for_width(self, width: int):
        for text, resolution in self.all_resolutions.items():
            if resolution[0] == width:
                return text
        return None
    

        