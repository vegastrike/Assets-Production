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
from graphics_factory.label_control_pair import BoolLeafGui, SpinnerLeafGui
from graphics_factory.divider import DividerLine

class GraphicsTab(BoxLayout):
    selected_screen = StringProperty()
    available_resolutions = ListProperty()

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.padding = 10

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


        # Start adding widgets
        # Title
        title_label = Label(text="GRAPHICS", font_size=24, size_hint=(0.8, None), height = 80,
                            halign='center')
        self.add_widget(title_label)

        # Divider
        self.add_widget(DividerLine())

        # Full Screen
        full_screen_leaf = gc.game_config.get_object(["graphics", "full_screen"])
        if full_screen_leaf and isinstance(full_screen_leaf, gc.ConfigLeaf):
            full_screen_gui = BoolLeafGui(parent=self, leaf=full_screen_leaf, tooltip_text="Run the game in a full screen or windowed mode.")
        else:
            print(full_screen_leaf)

        # Screens
        screen_leaf = gc.game_config.get_object(["graphics", "screen"])
        screen_layout = SpinnerLeafGui(parent=self, leaf=screen_leaf, initial_value=self.selected_screen,
                                        values=[screen.name for screen in self.screens],
                                        on_change=self.on_change_screen, 
                                        tooltip_text="The monitor to run the game in, in multi-monitor systems.")


        # Resolutions
        self.resolution_x_leaf = gc.game_config.get_object(["graphics", "resolution_x"])
        self.resolution_y_leaf = gc.game_config.get_object(["graphics", "resolution_y"])
        self.resolution_layout = SpinnerLeafGui(parent=self, leaf=None,
                                          initial_value=self.get_resolution_for_x_and_y(self.screen_resolution),
                                          values=list(self.available_resolutions_for_screen(0).keys()),
                                          on_change=self.on_resolution_change, title="Resolution:", 
                                          tooltip_text="The resolution of the game.")

        spacer = BoxLayout(size_hint_y=1)
        self.add_widget(spacer)

    def on_full_screen_change(self, instance, value):
        gc.game_config.set(["graphics", "full_screen"], value)

    def on_change_screen(self, instance, screen_name):
        if screen_name == None:
            print(f"on_change_screen error. screen_name is None.")
            return
        
        index = self.get_index_for_screen(screen_name)
        if index == -1:
            print(f"on_change_screen error. index is -1.")
            return
        
        print(f"on_change_screen({screen_name}) => previous {self.screen_resolution}")
        print(f"on_change_screen({screen_name}) => {index}")
        self.selected_screen = screen_name
        self.screen_resolution = (self.screens[index].width, self.screens[index].height)
        print(f"on_change_screen({screen_name}) => {self.screen_resolution}")
        self.resolution_layout.set_text(self.get_resolution_for_x_and_y(self.screen_resolution))
        self.resolution_layout.set_values(self.available_resolutions_for_screen(index))
        
        gc.game_config.set(["graphics", "screen"], index)

    def on_resolution_change(self, instance, resolution_text):
        print(f"New resolution {resolution_text}")
        resolution = self.all_resolutions[resolution_text]
        print(f"New resolution {resolution}")
        self.resolution_x_leaf.set(resolution[0])
        self.resolution_y_leaf.set(resolution[1])

    def get_index_for_screen(self, screen_name):
        for index, screen in enumerate(self.screens):
            if screen.name == screen_name:
                return index
        return -1

    def available_resolutions_for_screen(self, index):
        width, height = resolution_for_screen(index)
        return {
            text: resolution
            for text, resolution in self.all_resolutions.items()
            if resolution[0] <= width and resolution[1] <= height
        }

    def get_resolution_for_x_and_y(self, requested_resolution):
        default_resolution = "1024x768"
        if requested_resolution[0]==0 or requested_resolution[1]==0:
            print(f"get_resolution_for_x_and_y({requested_resolution}) error. Invalid resolution value")
            return default_resolution
        
        for text, resolution in self.all_resolutions.items():
            if resolution[0] == requested_resolution[0] and resolution[1] == requested_resolution[1]:
                return text
        print(f"get_resolution_for_x_and_y({requested_resolution}), resolution pair not found")
        return default_resolution

    # Warning: This method is for testing only
    def add_dummy_screen(self):
        dummy = screeninfo.Monitor(x=0,y=0,width=1920,height=1080,name='dummy')
        dummy.is_primary = True
        self.screens[0].is_primary = False
        self.screens.append(dummy)
        print(self.screens)

class GraphicsApp(App):
    def build(self):
        return GraphicsTab()


if __name__ == "__main__":
    GraphicsApp().run()
