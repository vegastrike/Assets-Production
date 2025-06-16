from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.app import App
from kivy.properties import StringProperty, ListProperty
import screeninfo
import json
import os

from os_utils import number_of_screens, resolution_for_screen
import game_config as gc
from graphics_factory.label_control_pair import BoolLeafGui


class GraphicsTab(BoxLayout):
    selected_screen = StringProperty()
    available_resolutions = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)

        self.tab_name = "Graphics"

        self.num_screens = number_of_screens()
        self.screens = screeninfo.get_monitors()
        self.screen_resolution = resolution_for_screen(0)

        # Make primary screen the first one
        if len(self.screens) > 1:
            self.screens.sort(key=lambda screen: screen.is_primary, reverse=True)

        # Load resolutions from the JSON file
        with open(os.path.join("templates", "resolutions.json"), "r") as file:
            self.all_resolutions = json.load(file)

        self.selected_screen: str = self.screens[0].name
        if gc.game_config.has_key(["graphics", "screen"]):
            screen_index: int = gc.game_config.get(["graphics", "screen"])
            self.selected_screen = self.screens[screen_index].name

        if gc.game_config.has_key(["graphics", "resolution_x"]):
            self.screen_resolution = (
                gc.game_config.get(["graphics", "resolution_x"]),
                gc.game_config.get(["graphics", "resolution_y"]),
            )
        else:
            gc.game_config.set(["graphics", "resolution_x"], self.screen_resolution[0])
            gc.game_config.set(["graphics", "resolution_y"], self.screen_resolution[1])

        # Full Screen
        full_screen_leaf = gc.game_config.get_object(["graphics", "full_screen"])
        if full_screen_leaf and isinstance(full_screen_leaf, gc.ConfigLeaf):
            full_screen_gui = BoolLeafGui(parent=self, leaf=full_screen_leaf)
        else:
            print(full_screen_leaf)

        # Screens
        screens_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
        screens_label = Label(text="Screen", size_hint_x=0.7)
        screens_spinner = Spinner(
            text=self.selected_screen,
            values=[screen.name for screen in self.screens],
            size_hint_x=0.3,
        )
        screens_spinner.bind(text=self.on_change_screen)
        screens_layout.add_widget(screens_label)
        screens_layout.add_widget(screens_spinner)
        self.add_widget(screens_layout)

        # Resolutions
        resolutions_layout = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)
        resolutions_label = Label(text="Resolution", size_hint_x=0.7)
        resolutions_spinner = Spinner(
            text=self.get_resolution_for_width(self.screen_resolution[0]),
            values=list(self.available_resolutions_for_screen(0).keys()),
            size_hint_x=0.3,
        )
        resolutions_spinner.bind(text=self.on_resolution_change)
        resolutions_layout.add_widget(resolutions_label)
        resolutions_layout.add_widget(resolutions_spinner)
        self.add_widget(resolutions_layout)

    def on_full_screen_change(self, instance, value):
        gc.game_config.set(["graphics", "full_screen"], value)

    def on_change_screen(self, instance, screen_name):
        self.selected_screen = screen_name
        self.screen_resolution = resolution_for_screen(self.get_index_for_screen(screen_name))
        gc.game_config.set(["graphics", "screen"], self.get_index_for_screen(screen_name))

    def on_resolution_change(self, instance, resolution_text):
        resolution = self.all_resolutions[resolution_text]
        gc.game_config.set(["graphics", "resolution_x"], resolution[0])
        gc.game_config.set(["graphics", "resolution_y"], resolution[1])

    def get_index_for_screen(self, screen_name):
        for index, screen in enumerate(self.screens):
            if screen.name == screen_name:
                return index
        return 0

    def available_resolutions_for_screen(self, index):
        width, height = resolution_for_screen(index)
        return {
            text: resolution
            for text, resolution in self.all_resolutions.items()
            if resolution[0] <= width and resolution[1] <= height
        }

    def get_resolution_for_width(self, width):
        for text, resolution in self.all_resolutions.items():
            if resolution[0] == width:
                return text
        return None


class GraphicsApp(App):
    def build(self):
        return GraphicsTab()


if __name__ == "__main__":
    GraphicsApp().run()
