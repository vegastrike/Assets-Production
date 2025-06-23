from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

import game_config as gc
from graphics_factory.label_control_pair import BoolLeafGui, SpinnerLeafGui
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
        self.game_accel = ac.app_schema["physics"]
        game_accel_keys = list(self.game_accel.keys())
        self.game_accel_leaf = gc.game_config.get_object(["physics", "game_accel"])
        game_accel_layout = SpinnerLeafGui(parent=self, leaf=self.game_accel_leaf, 
                                           initial_value=self.get_accel_key_for_value(self.game_accel_leaf) or game_accel_keys[0],
                                           values=game_accel_keys, on_change=self.on_change)
        
        spacer = BoxLayout(size_hint_y=1)
        self.add_widget(spacer)
        
    def get_accel_key_for_value(self, leaf):
        for key, value in self.game_accel.items():
            if value == leaf.value:
                return key
        return None
    
    def on_change(self, instance, new_text):
        if new_text in self.game_accel:
            new_value = self.game_accel[new_text]
        else:
            print(f"Error in PerformanceTab:game_accel_layout. {instance} {new_text} not found in game_accel_options.")    
            return
        
        print(f"Control {instance} {new_text} {new_value} replacing {self.game_accel_leaf.value}")
        self.game_accel_leaf.set(new_value=new_value)