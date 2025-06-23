from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App

import game_config as gc
from graphics_factory.label_control_pair import SpinnerMultiLeafGui
from graphics_factory.divider import DividerLine

import app_config as ac
from kivy.uix.slider import Slider


class AudioTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.padding = 10

        self.tab_name = "Audio"

        # Start adding widgets
        # Title
        title_label = Label(text="Audio".upper(), font_size=24, size_hint=(0.8, None), height = 80,
                            halign='center')
        self.add_widget(title_label)

        # Divider
        self.add_widget(DividerLine())

        # Sound selection
        SpinnerMultiLeafGui(parent=self, leaf=gc.game_config.get_object(["settings_app", "audio"]),
                            json=ac.app_schema["audio"], title="Sound:", 
                            tooltip_text="This changes multiple configuration items.")

        # Volume Control

        volume_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=(0, 10))
        volume_label = Label(text="Volume (this does nothing for now)", size_hint_x=0.3, halign='left', valign='middle')
        volume_label.bind(size=volume_label.setter('text_size'))

        self.volume_slider = Slider(min=0, max=100, value=50, size_hint_x=0.7)
        volume_layout.add_widget(volume_label)
        volume_layout.add_widget(self.volume_slider)
        self.add_widget(volume_layout)
        
        spacer = BoxLayout(size_hint_y=1)
        self.add_widget(spacer)