from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App

import os
import sys
import json

# TODO: uncomment for running test code
sys.path.append('/home/roy/git/Assets-Production/python/settings_app')

import game_config as gc
from kivy.graphics import Color, Rectangle

import graphics_factory.breadcrumbs as breadcrumbs
import graphics_factory.label_control_pair as label_control_pair


class ConfigPane(BoxLayout):
    def __init__(self, branch:gc.ConfigBranch, navigate):
        super().__init__(size_hint=(1.0,1.0))

        self.branch = branch
        self.navigate = navigate

        self.orientation = 'vertical'
        self.padding = 10
        # self.spacing = 10
       

        # Set background color to pink
        # with self.canvas.before:
        #     Color(1, 0.75, 0.8, 1)  # RGBA for pink
        #     self.rect = Rectangle(size=self.size, pos=self.pos)
        
        # Update rectangle size and position on layout changes
        # self.bind(size=self._update_rect, pos=self._update_rect)


        # Title
        title_label = Label(text=self.branch.key.upper(), font_size=24)
        self.add_widget(title_label)

        # Breadcrumb
        self.breadcrumbs = breadcrumbs.Breadcrumbs(branch=branch, navigate=navigate)
        self.add_widget(self.breadcrumbs)
        self.add_widget(Label())  # Padding from below

        # Configuration
        limit = 10
        count = 0
        for key, value in self.branch.value.items():
            if count == limit:
                break

            if isinstance(value, gc.ConfigBranch):
                print(f"Branch: {value}")
            elif isinstance(value, gc.ConfigLeaf):
                leaf = value
                
                if isinstance(leaf.value, bool):
                    print(f"Leaf: boolean value {leaf.key} {leaf.value}")
                    label_control_pair.BoolLeafGui(parent=self, leaf=leaf)
                elif isinstance(leaf.value, str):
                    label_control_pair.TextLeafGui(parent=self, leaf=leaf)
                    print(f"Leaf: string value {leaf.value}")
                elif isinstance(leaf.value, int):
                    label_control_pair.TextLeafGui(parent=self, leaf=leaf)
                    print(f"Leaf: int value {leaf.value}")
                elif isinstance(leaf.value, float):
                    label_control_pair.TextLeafGui(parent=self, leaf=leaf)
                    print(f"Leaf: float value {leaf.value}")
            else:
                print(f"Illegal value: {value}")

            count += 1

        
    # def _update_rect(self, instance, value):
    #     self.rect.size = instance.size
    #     self.rect.pos = instance.pos

# Test Code
class ConfigPaneApp(App):
    def build(self):
        return ConfigPane(gc.game_config.get_object(['audio', 'unit_audio']))

if __name__ == '__main__':
    assets_config_filename="/home/roy/git/Assets-Production/config.json"
    user_config_filename="/home/roy/.vegastrike/config.json"

    with open(assets_config_filename, 'r') as assets_file:
        assets_config = json.load(assets_file)

    with open(user_config_filename, 'r') as user_file:
        user_config = json.load(user_file)

    gc.game_config = gc.GameConfig(
        assets_config_filename=assets_config_filename,
        assets_config=assets_config,
        user_config_filename=user_config_filename,
        user_config=user_config
    )

    app = ConfigPaneApp().run()