from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView

import game_config as gc
from graphics_factory.label_control_pair import CaptureKeyStrokePair
from graphics_factory.divider import DividerLine




class BindingsTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.padding = 10

        self.tab_name = "Keys"

        # Start adding widgets
        # Title
        title_label = Label(text="Keyboard Bindings".upper(), font_size=24, size_hint=(0.8, None), height = 80,
                            halign='center')
        self.add_widget(title_label)

        # Divider
        self.add_widget(DividerLine())

        bindings = gc.game_config.get_object(["controls"])

        # Scrollable configuration area
        scroll_view = ScrollView(size_hint=(1, 0.8))
        config_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        config_layout.bind(minimum_height=config_layout.setter('height'))
        scroll_view.add_widget(config_layout)
        self.add_widget(scroll_view)
        
        for key, value in bindings.value.items():
            CaptureKeyStrokePair(parent=config_layout, key_leaf=value.value["key"], modifier_leaf=value.value["modifier"],
                                 title=key)
            