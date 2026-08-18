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

        # Title
        title_label = Label(text="Controls".upper(), font_size=24, size_hint=(0.8, None), height=80,
                            halign='center')
        self.add_widget(title_label)

        # Divider
        self.add_widget(DividerLine())

        # Scrollable configuration area. Content is top-anchored: the inner
        # BoxLayout grows downward (minimum_height -> height), so extra text
        # flows to the bottom and can be scrolled to, instead of overflowing
        # upward over the title/buttons above.
        scroll_view = ScrollView(size_hint=(1, 1))
        config_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        config_layout.bind(minimum_height=config_layout.setter('height'))
        scroll_view.add_widget(config_layout)
        self.add_widget(scroll_view)

        # -- Keyboard section (placeholder header; actual key bindings are in
        #    the Keys/Bindings tab) --
        config_layout.add_widget(Label(text="Keyboard".upper(), font_size=18, size_hint=(0.8, None), height=80,
                                       halign='center'))

        config_layout.add_widget(Label(text="Mouse".upper(), font_size=18, size_hint=(0.8, None), height=80,
                                       halign='center'))

        mouse_enabled_leaf = gc.game_config.get_object(["input", "mouse", "enabled"])
        BoolLeafGui(parent=config_layout, leaf=mouse_enabled_leaf)

        mouse_inverse_x_leaf = gc.game_config.get_object(["input", "mouse", "inverse_x"])
        BoolLeafGui(parent=config_layout, leaf=mouse_inverse_x_leaf)

        mouse_inverse_y_leaf = gc.game_config.get_object(["input", "mouse", "inverse_y"])
        BoolLeafGui(parent=config_layout, leaf=mouse_inverse_y_leaf)

        mouse_warp_leaf = gc.game_config.get_object(["input", "joystick", "warp_mouse"])
        BoolLeafGui(parent=config_layout, leaf=mouse_warp_leaf)

        mouse_sensitivity_leaf = gc.game_config.get_object(["input", "joystick", "mouse_sensitivity"])
        SliderLeafGui(parent=config_layout, leaf=mouse_sensitivity_leaf, min=20, max=200, step=10)

        config_layout.add_widget(Label(text="Joystick".upper(), font_size=18, size_hint=(0.8, None), height=80,
                                       halign='center'))

        joystick_enabled_leaf = gc.game_config.get_object(["input", "joystick", "enabled"])
        BoolLeafGui(parent=config_layout, leaf=joystick_enabled_leaf)

        joystick_throttle_leaf = gc.game_config.get_object(["input", "joystick", "throttle"])
        BoolLeafGui(parent=config_layout, leaf=joystick_throttle_leaf)

        joystick_hat_leaf = gc.game_config.get_object(["input", "joystick", "hat_enabled"])
        BoolLeafGui(parent=config_layout, leaf=joystick_hat_leaf)
