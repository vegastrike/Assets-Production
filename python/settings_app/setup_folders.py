import os
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.graphics import Color, Rectangle

import app_config as ac
import game_config as gc

from graphics_factory.file_dialog import FileChooserPopup

CONFIG_FILE_NAME = "config.json"

def check_config_file_paths():
    success = True
    # Check if we have the paths to the assets and user folders
    if not ac.app_config.app_configured():
        app = FolderSetupWindow()
        app.run()
        success = app.success
    else:
        print("App already configured.")
    return success

class LabelTextButtonRow(BoxLayout):
    label_texts = ['Assets Folder:', 'User Folder:']
    def __init__(self, parent_layout:BoxLayout, assets:bool, validation_function):
        super().__init__(orientation='horizontal', spacing=10, padding=10, size_hint=(1, 0.3))

        # Can't raise exceptions or debugger will hang
        if not validation_function:
            print(f"Error: validation_function is None")
        

        self.assets = assets
        self.validation_function = validation_function
        

        if(assets):
            index = 0
            folder_path = ac.app_config.assets_folder or ac.home_dir
                    
        else:
            index = 1
            folder_path = ac.app_config.user_folder or ac.home_dir

        label_text = self.label_texts[index]
        
        # with self.canvas.before:
        #     Color(0.2, 0.6, 0.8, 1)  # RGBA: light blue
        #     self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        # Keep rectangle in sync with layout size/pos
        # self.bind(pos=self.update_bg, size=self.update_bg)
        
        self.add_widget(Label(text=label_text, size_hint=(1, None), height=30, halign="left"))
        self.input = TextInput(text=folder_path, multiline=False, size_hint=(4.3, None), height=30)
        self.input.bind(text=self.validate_live)
        self.add_widget(self.input)
        button = Button(text="Browse...", size_hint=(0.7, None), height=30)
        button.bind(on_press=self.browse_for_folder)
        self.add_widget(button)
        parent_layout.add_widget(self)
        
    # def update_bg(self, *args):
    #     self.bg_rect.pos = self.pos
    #     self.bg_rect.size = self.size
    
    def browse_for_folder(self, instance):
        file_chooser_popup = FileChooserPopup(on_selection=self.on_popup_select)
        popup = Popup(title="Select", content=file_chooser_popup, size_hint=(0.9, 0.9))
        file_chooser_popup.parent_popup = popup  # Allow popup to be dismissed from within
        popup.open()

    def validate_live(self, instance, value):
        print(value)

    def on_popup_select(self, selected_folder):
        print(f"on_popup_select {selected_folder}")
        self.user_folder = selected_folder
        self.input.text = selected_folder
        if self.assets:
            ac.app_config.assets_folder = selected_folder
        else:
            ac.app_config.user_folder = selected_folder
        self.validation_function()



class FolderSetupWindow(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Add a simple label at the top of the window
        layout.add_widget(Label(text="Folders Setup", font_size=24, size_hint=(1, 0.2)))

        self.success = False

        LabelTextButtonRow(layout, assets = True, validation_function=self.validate)
        LabelTextButtonRow(layout, assets = False, validation_function=self.validate)

        # OK and Cancel buttons
        bottom_buttons_row = BoxLayout(orientation='horizontal', spacing=10, padding=10, size_hint=(0.7, 0.2))
        bottom_buttons_row.add_widget(BoxLayout(size_hint=(1, 1)))  # Spacer to align buttons to the right

        self.ok_button = Button(text="OK", disabled=True, height=30)
        self.ok_button.bind(on_press=self.on_ok)
        bottom_buttons_row.add_widget(self.ok_button)

        self.cancel_button = Button(text="Cancel", height=30)
        self.cancel_button.bind(on_press=self.on_cancel)
        bottom_buttons_row.add_widget(self.cancel_button)
        layout.add_widget(bottom_buttons_row)

        layout.add_widget(BoxLayout(size_hint=(1, 1)))  # Bottom spacer

        self.validate()

        return layout

    
    def validate(self):
        print("Validating folders...")
        if not ac.app_config.assets_folder or not ac.app_config.user_folder:
            print(f"None for {ac.app_config.assets_folder} or {ac.app_config.user_folder}")
            self.ok_button.disabled = True
            self.success = False
            return

        assets_config_found = os.path.exists(os.path.join(ac.app_config.assets_folder, CONFIG_FILE_NAME))
        user_folder_exists = os.path.exists(ac.app_config.user_folder)
        if (not assets_config_found or not user_folder_exists):
            print(f"Found config in assets folder: {assets_config_found}")
            print(f"User folder exists: {user_folder_exists}")
            self.ok_button.disabled = True
            self.success = False
            return

        print("Success validating. Enabling OK button.")
        self.ok_button.disabled = False
        self.success = True

    def on_ok(self, instance):
        ac.app_config.settings_app_config_filename = os.path.join(ac.app_config.user_folder, ac.SETTINGS_APP_CONFIG_FILE_SUFFIX)
        ac.app_config.serialize()
        gc.load_game_config()
        self.stop()
        #self.result = True

    def on_cancel(self, instance):
        self.success = False
        print("Could not set up the folders correctly. Exiting.")
        self.stop()
        #self.result = False



if __name__ == "__main__":
    FolderSetupWindow().run()
