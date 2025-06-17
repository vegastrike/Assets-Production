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

import key_utils

class AbstractLabelControlPair:
    # An abstract class to hold shared code for below pairs

    def __init__(self, parent: tk.Frame, key:list[str], text: str):
        self.parent = parent
        self.key: list[str] = key
        self.text: str = text
    
class LabelCheckboxPair(AbstractLabelControlPair):
    def __init__(self, parent: tk.Frame, key:list[str], text: str,  
                 attributes: GraphicAttributes, initial_value: bool = False):
        super().__init__(parent, key, text)
        frame_row = ttk.Frame(parent)
        frame_row.pack(pady=attributes.padding_y)

        label = ttk.Label(frame_row, text=f"{text}:", font=attributes.font)
        label.pack(side=attributes.alignment, padx=attributes.padding_x)

        self.toggle_var = tk.BooleanVar(value=initial_value)
        toggle_button = ttk.Checkbutton(frame_row, variable=self.toggle_var)
        toggle_button.pack(side=attributes.alignment, padx=attributes.padding_x)

        self.toggle_var.trace_add("write", lambda *args: self._on_change())

    def _on_change(self):
        # This method is called when the combobox value changes
        # It updates the config with the new value
        if self.key:
            self.config.set(self.key, self.toggle_var.get())
        else:
            print("No key set for this control pair, cannot update config.")

class BoolLeafGui(BoxLayout):
    def __init__(self, parent: BoxLayout, leaf: gc.ConfigLeaf, on_toggle = None):
        super().__init__(orientation='horizontal')
        self.leaf = leaf

        parent.add_widget(self)

        label = Label(text=f"{key_utils.format_key(leaf.key)}:", halign="left")
        label.bind(size=self.update_text_size)
        self.add_widget(label)

        self.toggle_button = CheckBox(active=self.leaf.value)
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
    def __init__(self, parent: BoxLayout, leaf: gc.ConfigLeaf, on_change = None):
        super().__init__(orientation='horizontal')
        self.leaf = leaf

        parent.add_widget(self)

        label = Label(text=f"{key_utils.format_key(leaf.key)}:", halign="left")
        label.bind(size=self.update_text_size)
        self.add_widget(label)

        self.text_field = TextInput(text=str(self.leaf.value), multiline=False)
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
    # 



class LabelComboboxPair(AbstractLabelControlPair):
    def __init__(self, parent: tk.Frame, key:str, text: str, attributes: GraphicAttributes, 
                    options: list, initial_value: str = None, on_change=None):
        super().__init__(parent, key, text)
        frame_row = tk.Frame(parent, bg=attributes.background)
        frame_row.pack(pady=attributes.padding_y)

        label = tk.Label(frame_row, text=f"{text}:", fg=attributes.foreground, 
                            bg=attributes.background, font=attributes.font)
        label.pack(side=attributes.alignment, padx=attributes.padding_x)

        combobox_var = tk.StringVar(value=initial_value)
        combobox = tk.OptionMenu(frame_row, combobox_var, *options)
        combobox.config(bg=attributes.background, fg=attributes.foreground, 
                        font=attributes.font, activebackground=attributes.background)
        combobox.pack(side=attributes.alignment, padx=attributes.padding_x)

        if on_change:
            # Call the callback function to effect other controls
            # Used to change the resolution control when selecting a different screen
            combobox_var.trace_add("write", lambda *args: on_change(combobox_var.get()))


# A special case for resolution combo box, which has two keys
class ResolutionPair(AbstractLabelControlPair):
    def __init__(self, parent: tk.Frame, first_key:list[str], 
                 second_key:list[str], text: str, attributes: GraphicAttributes, 
                    resolutions: dict[str, (int,int)], initial_value: str):
        super().__init__(parent=parent, key=None, text=text)
        self.first_key = first_key
        self.second_key = second_key
        self.resolutions = resolutions

        frame_row = tk.Frame(parent, bg=attributes.background)
        frame_row.pack(pady=attributes.padding_y)

        label = tk.Label(frame_row, text=f"{text}:", fg=attributes.foreground, 
                            bg=attributes.background, font=attributes.font)
        label.pack(side=attributes.alignment, padx=attributes.padding_x)

        self.combobox_var = tk.StringVar(value=initial_value)
        combobox = tk.OptionMenu(frame_row, self.combobox_var, *resolutions.keys())
        combobox.config(bg=attributes.background, fg=attributes.foreground, 
                        font=attributes.font, activebackground=attributes.background)
        combobox.pack(side=attributes.alignment, padx=attributes.padding_x)

        self.combobox_var.trace_add("write", lambda *args: self._on_change())
            

    def _on_change(self):
        key = self.combobox_var.get()
        gc.game_config.set(self.first_key, self.resolutions[key][0]) 
        gc.game_config.set(self.second_key, self.resolutions[key][1]) 


# Test Code
if __name__ == "__main__":

    # Define some example attributes
    attributes = GraphicAttributes(
        background="#333333",
        foreground="#FFFFFF",
        font="Arial", 
        font_size=12,
        padding_x=10,
        padding_y=5,
        alignment=tk.LEFT
    )

    # Create the main application window
    root = tk.Tk()
    root.title("LabelCheckboxPair Example")
    root.configure(bg=attributes.background)

    # Create a frame to hold the widget
    main_frame = tk.Frame(root, bg=attributes.background)
    main_frame.pack(padx=20, pady=20)

    # Create and display the LabelCheckboxPair
    label_checkbox = LabelCheckboxPair(
        parent=main_frame,
        text="Enable Feature",
        attributes=attributes,
        initial_value=True
    )

    label_combo = LabelComboboxPair(
        parent=main_frame,
        text="Select Option",
        attributes=attributes,
        options=["Option 1", "Option 2", "Option 3"],
        initial_value="Option 1"
    )

    # Start the Tkinter event loop
    root.mainloop()