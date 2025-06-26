from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

import game_config as gc

from graphics_factory.divider import DividerLine
from graphics_factory.label_control_pair import BoolLeafGui, SliderLeafGui


class ControlsTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.padding = 10

        self.tab_name = "Controls"

        # Start adding widgets
        # Title
        title_label = Label(text="Controls".upper(), font_size=24, size_hint=(0.8, None), height = 80,
                            halign='center')
        self.add_widget(title_label)

        # Divider
        self.add_widget(DividerLine())

        
        
        self.add_widget(Label(text="Keyboard".upper(), font_size=18, size_hint=(0.8, None), height = 80,
                              halign='center'))

        self.add_widget(Label(text="Mouse".upper(), font_size=18, size_hint=(0.8, None), height = 80,
                              halign='center'))
        
        mouse_enabled_leaf = gc.game_config.get_object(["mouse","enabled"])
        BoolLeafGui(parent=self, leaf=mouse_enabled_leaf)

        mouse_inverse_x_leaf = gc.game_config.get_object(["mouse","inverse_x"])
        BoolLeafGui(parent=self, leaf=mouse_inverse_x_leaf)

        mouse_inverse_y_leaf = gc.game_config.get_object(["mouse","inverse_y"])
        BoolLeafGui(parent=self, leaf=mouse_inverse_y_leaf)

        mouse_warp_leaf = gc.game_config.get_object(["joystick","warp_mouse"])
        BoolLeafGui(parent=self, leaf=mouse_warp_leaf)

        mouse_sensitivity_leaf = gc.game_config.get_object(["joystick", "mouse_sensitivity"])
        SliderLeafGui(parent=self, leaf=mouse_sensitivity_leaf, min=20, max=200, step=10)
    
        self.add_widget(Label(text="Joystick".upper(), font_size=18, size_hint=(0.8, None), height = 80,
                              halign='center'))
        
        joystick_enabled_leaf = gc.game_config.get_object(["joystick","enabled"])
        BoolLeafGui(parent=self, leaf=joystick_enabled_leaf)

        joystick_throttle_leaf = gc.game_config.get_object(["joystick","throttle"])
        BoolLeafGui(parent=self, leaf=joystick_throttle_leaf)

        joystick_hat_leaf = gc.game_config.get_object(["joystick","hat_enabled"])
        BoolLeafGui(parent=self, leaf=joystick_hat_leaf)


    

