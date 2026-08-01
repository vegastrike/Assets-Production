from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

import game_config as gc

from graphics_factory.divider import DividerLine
from graphics_factory.label_control_pair import BoolLeafGui, SliderLeafGui, SpinnerLeafGui, TextLeafGui


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

        # ---- Axes (continuous flight inputs: x/y/z/throttle roles) ----
        self.add_widget(Label(text="Axes".upper(), font_size=18, size_hint=(0.8, None), height=80,
                              halign='center'))

        axes = gc.game_config.get_object(["axes"])
        if axes is not None:
            for role in sorted(axes.value.keys()):
                role_leaf = axes.get_object([role])
                # role -> {source, joystick/mouse, axis, inverse}
                title = Label(text=role, valign='middle', halign='left', height=40, size_hint_y=None)
                self.add_widget(title)
                if role_leaf.has_key(["source"]):
                    source_leaf = role_leaf.get_object(["source"])
                    SpinnerLeafGui(parent=self, leaf=source_leaf, initial_value=source_leaf.value,
                                   values=["joystick", "mouse"], title="source")
                if role_leaf.has_key(["joystick"]):
                    joy_leaf = role_leaf.get_object(["joystick"])
                    TextLeafGui(parent=self, leaf=joy_leaf, title="joystick")
                if role_leaf.has_key(["mouse"]):
                    mouse_leaf = role_leaf.get_object(["mouse"])
                    TextLeafGui(parent=self, leaf=mouse_leaf, title="mouse")
                if role_leaf.has_key(["axis"]):
                    axis_leaf = role_leaf.get_object(["axis"])
                    TextLeafGui(parent=self, leaf=axis_leaf, title="axis")
                if role_leaf.has_key(["inverse"]):
                    inv_leaf = role_leaf.get_object(["inverse"])
                    BoolLeafGui(parent=self, leaf=inv_leaf, title="inverse")
        else:
            self.add_widget(Label(text="No 'axes' section found in config.json", height=40, size_hint_y=None))


    

