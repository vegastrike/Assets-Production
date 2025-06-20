import tkinter as tk
import tkinter.ttk as ttk
from graphics_factory.graphic_attributes import GraphicAttributes 

import game_config as gc
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.properties import BooleanProperty
from kivy.graphics import Color, Rectangle
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner

import key_utils

from graphics_factory.tooltip import TooltipIcon


class BoolLeafGui(BoxLayout):
    def __init__(self, parent: BoxLayout, leaf: gc.ConfigLeaf, on_toggle = None):
        super().__init__(orientation='horizontal', height=70, size_hint_y=None)
        self.leaf = leaf

        parent.add_widget(self)

        label = Label(text=f"{key_utils.format_key(leaf.key)}:", valign='middle', halign="left", height=70)
        label.bind(size=self.update_text_size)
        self.add_widget(label)

        self.toggle_button = CheckBox(active=self.leaf.value, height=70)
        self.add_widget(self.toggle_button)

        if on_toggle:
            self.toggle_button.bind(active=on_toggle)
        else:
            self.toggle_button.bind(active=self.on_change)

        # Set background color to pink
        # with self.canvas.before:
        #     Color(0.2, 0.75, 0.8, 1)  # RGBA for pink
        #     self.rect = Rectangle(size=self.size, pos=self.pos)
        
        # Update rectangle size and position on layout changes
        # self.bind(size=self._update_rect, pos=self._update_rect)

    def on_change(self, checkbox, value):
        print(f"Checkbox {checkbox} {value} replacing {self.leaf.value}")
        self.leaf.set(value)

    def update_text_size(self, instance, size):
        instance.text_size = size

    # def _update_rect(self, instance, value):
    #     self.rect.size = instance.size
    #     self.rect.pos = instance.pos

# TODO: figure out how to differentiate int from float
# isinstance(value, int) returns True only if value is an integer (e.g., 5, -3, 0).
# isinstance(value, float) returns True only if value is a floating-point number (e.g., 3.14, -2.5, 0.0).
# Floats that represent integers - 5.0 is not considered an integer by isinstance(value, int).
# This means config.json needs to be sanitised for this to work properly.
class TextLeafGui(BoxLayout):
    def __init__(self, parent: BoxLayout, leaf: gc.ConfigLeaf, on_change = None, tooltip = None):
        super().__init__(orientation='horizontal', height=70, size_hint_y=None)
        self.leaf = leaf

        parent.add_widget(self)

        tooltip_text = tooltip or "This is a test tooltip"

        label = TooltipIcon(text=f"{key_utils.format_key(leaf.key)} ", tooltip_text=tooltip_text, valign='middle', halign="left")
        label.bind(size=self.update_text_size)
        self.add_widget(label)

        self.text_field = TextInput(text=str(self.leaf.value), multiline=False, size_hint=(0.8, None), height = 45,
                                       halign='center')
        self.add_widget(self.text_field)

        if on_change:
            self.text_field.bind(text=on_change)
        else:
            self.text_field.bind(text=self.on_change)


        # Set background color to pink
        # with self.canvas.before:
        #     Color(0.2, 0.75, 0.8, 1)  # RGBA for pink
        #     self.rect = Rectangle(size=self.size, pos=self.pos)
        
        # Update rectangle size and position on layout changes
        # self.bind(size=self._update_rect, pos=self._update_rect)

    def on_change(self, instance, value):
        print(f"Text field changed from {self.leaf.value} to {value}")
        try:
            # Attempt to cast the value to the type of the leaf's original value
            if isinstance(self.leaf.value, int):
                self.leaf.set(int(value))
            elif isinstance(self.leaf.value, float):
                self.leaf.set(float(value))
            else:
                self.leaf.set(value)
        except ValueError:
            print(f"Invalid value: {value}. Could not cast to {type(self.leaf.value).__name__}.")

    def update_text_size(self, instance, size):
        instance.text_size = size
        
    # def _update_rect(self, instance, value):
    #     self.rect.size = instance.size
    #     self.rect.pos = instance.pos

        
        


class SpinnerLeafGui(BoxLayout):
    def __init__(self, parent: BoxLayout, leaf: gc.ConfigLeaf, initial_value:str, values: list[str], on_change = None, title = None):
        super().__init__(orientation='horizontal', height=70, size_hint_y=None)
        self.leaf = leaf
        title  = title or f"{key_utils.format_key(leaf.key)}:"

        parent.add_widget(self)

        label = Label(text=title, valign='middle', halign="left", height = 70)
        label.bind(size=self.update_text_size)
        self.add_widget(label)

        self.spinner = Spinner(text=initial_value, values=values, size_hint=(0.8, None), height = 45,
                                       halign='center')
        self.add_widget(self.spinner)

        if on_change:
            self.spinner.bind(text=on_change)
        else:
            self.spinner.bind(text=self.on_change)

    def update_text_size(self, instance, size):
        instance.text_size = size

    def on_change(self, instance, text):
        self.leaf.set(new_value=text)

    def set_text(self, text):
        self.spinner.text = text
    
    def set_values(self, values):
        self.spinner.values = values

# Test Code
if __name__ == "__main__":
    pass
    