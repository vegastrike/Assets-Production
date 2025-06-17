from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.relativelayout import RelativeLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

import graphics_factory.label_control_pair as label_control_pair
import graphics_factory.graphic_attributes as graphic_attributes
import graphics_factory.config_pane as config_pane

import game_config as gc

from config_to_gui import generate_first_level_section

import key_utils

class AdvancedTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.tab_name = "Advanced"
        self.size_hint=(1.0,1.0)

        # Set background color to pink
        # with self.canvas.before:
        #     Color(1, 0.75, 0.2, 1)  # RGBA for pink
        #     self.rect = Rectangle(size=self.size, pos=self.pos)
        
        # Update rectangle size and position on layout changes
        # self.bind(size=self._update_rect, pos=self._update_rect)

        # Wrap in a ScrollView so layout can expand properly
        #self.scroll = ScrollView(size_hint=(1, 1))

        # ConfigPane
        self.config_pane = None

        # Create the main navigation frame - displays config sections in a grid
        self.main_frame = GridLayout(cols=4, size_hint=(1.0,1.0))
        #self.main_frame.bind(minimum_height=self.main_frame.setter('height'))

        self.links = []

        # Populate the left frame with config data
        for section, values in gc.game_config.value.items():
            btn = Button(
                text=key_utils.format_key(section),
                size_hint=(0.25,0.125),
                background_normal='',
                background_color=(0, 0, 0, 0),
                markup=True
            )
            btn.bind(on_press=self.on_label_click)
            self.links.append(btn)
            self.main_frame.add_widget(btn)

        #self.scroll.add_widget(self.main_frame)
        self.add_widget(self.main_frame)

        # Bind mouse position after layout is on screen
        Clock.schedule_once(lambda dt: Window.bind(mouse_pos=self.on_mouse_move), 0)

    # def _update_rect(self, instance, value):
    #     self.rect.size = instance.size
    #     self.rect.pos = instance.pos

    def on_mouse_move(self, window, pos):
        for btn in self.links:
            if btn.collide_point(*btn.to_widget(*pos)):
                if not btn.text.startswith("[u]"):
                    btn.text = f"[u]{btn.text}[/u]"
            else:
                if btn.text.startswith("[u]"):
                    btn.text = btn.text.replace("[u]", "").replace("[/u]", "")

    def on_label_click(self, instance):
        section_name = instance.text.replace("[u]", "").replace("[/u]", "")
        print(f"Clicked on section: {section_name}")

        branch = gc.game_config.get_object([section_name])
        if not branch:
            print(f"Branch {branch} not found.")
            return
        
        self.config_pane = config_pane.ConfigPane(branch=branch, navigate=self.navigate)

        self.remove_widget(self.main_frame)
        self.add_widget(self.config_pane)

    def navigate(self, instance):
        section_name = instance.text.replace("[u]", "").replace("[/u]", "")
        print(f"Clicked on section: {section_name}")

        if section_name == 'Home':
            self.remove_widget(self.config_pane)
            self.add_widget(self.main_frame)
            return

        branch = gc.game_config.get_object([section_name])
        if not branch:
            print(f"Branch {branch} not found.")
            return
        
        self.remove_widget(self.config_pane)
        self.config_pane = config_pane.ConfigPane(branch=branch, navigate=self.navigate)
        self.add_widget(self.config_pane)