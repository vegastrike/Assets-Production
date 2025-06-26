from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

import game_config as gc
from graphics_factory.label_control_pair import SpinnerMultiLeafGui
from graphics_factory.divider import DividerLine

import app_config as ac

class PerformanceTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.padding = 10

        self.tab_name = "Performance"

        # Start adding widgets
        # Title
        title_label = Label(text="Performance".upper(), font_size=24, size_hint=(0.8, None), height = 80,
                            halign='center')
        self.add_widget(title_label)

        # Divider
        self.add_widget(DividerLine())

        # Acceleration
        SpinnerMultiLeafGui(parent=self, leaf=gc.game_config.get_object(["settings_app", "physics"]),
                            json=ac.app_schema["physics"], title="Physics:", 
                            tooltip_text="???")
        
        spacer = BoxLayout(size_hint_y=1)
        self.add_widget(spacer)
