from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.tabbedpanel import TabbedPanelItem

import tabs.graphics
import tabs.advanced

import game_config as gc
import graphics_factory.tooltip as tooltip


class MainWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        # Create a TabbedPanel for tabbed panes
        self.notebook = TabbedPanel()
        self.notebook.do_default_tab = False
        self.add_widget(self.notebook)

        # Add graphics tab
        graphics_tab = tabs.graphics.GraphicsTab()
        graphics_tab_item = TabbedPanelItem(text=graphics_tab.tab_name)
        graphics_tab_item.add_widget(graphics_tab)
        self.notebook.add_widget(graphics_tab_item)
        # Set the default tab to display graphics_tab
        self.notebook.default_tab = graphics_tab_item

        # Add advanced tab
        advanced_tab = tabs.advanced.AdvancedTab()
        advanced_tab_item = TabbedPanelItem(text=advanced_tab.tab_name)
        advanced_tab_item.add_widget(advanced_tab)
        self.notebook.add_widget(advanced_tab_item)

        # Bottom buttons row
        bottom_buttons_row = BoxLayout(size_hint_y=None, height=50)
        self.add_widget(bottom_buttons_row)

        save_and_exit_button = Button(text="Save and Exit", on_press=lambda _: self.do_save_and_exit())
        bottom_buttons_row.add_widget(save_and_exit_button)

        exit_button = Button(text="Exit", on_press=lambda _: self.do_exit())
        bottom_buttons_row.add_widget(exit_button)

        print("Main window initialized.")

    def do_save_and_exit(self):
        gc.game_config.save_user_config()
        App.get_running_app().stop()

    def do_exit(self):
        App.get_running_app().stop()



class MainApp(App):
    def build(self):
        tooltip.root_layout = FloatLayout()
        main_layout = MainWindow()
        tooltip.root_layout.add_widget(main_layout)
        return tooltip.root_layout


if __name__ == "__main__":
    MainApp().run()
