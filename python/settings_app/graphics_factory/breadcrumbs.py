from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock

import game_config as gc

class Breadcrumbs(BoxLayout):
    def __init__(self, branch:gc.ConfigBranch, navigate):
        super().__init__(orientation='horizontal', spacing=5, padding=5)

        self.branch = branch
        self.navigate = navigate
        self.path = branch.get_path()
        self.path.insert(0, 'Home')
        self.links = []

        for i, folder in enumerate(self.path):
            btn = Button(
                text=f"{folder}",
                size_hint_x=None,
                width=100,
                background_normal='',
                background_color=(0, 0, 0, 0),
                markup=True
            )
            btn.bind(on_press=self.navigate)
            self.links.append(btn)
            self.add_widget(btn)

            # Add separator if not last
            if i < len(self.path) - 1:
                separator = Label(text='>', size_hint_x=None, width=30)
                self.add_widget(separator)

        # Bind mouse position after layout is on screen
        Clock.schedule_once(lambda dt: Window.bind(mouse_pos=self.on_mouse_move), 0)

    def on_mouse_move(self, window, pos):
        for btn in self.links:
            if btn.collide_point(*btn.to_widget(*pos)):
                if not btn.text.startswith("[u]"):
                    btn.text = f"[u]{btn.text}[/u]"
            else:
                if btn.text.startswith("[u]"):
                    btn.text = btn.text.replace("[u]", "").replace("[/u]", "")




# Test code
class MyApp(App):
    def build(self):
        return Breadcrumbs()

if __name__ == '__main__':
    MyApp().run()