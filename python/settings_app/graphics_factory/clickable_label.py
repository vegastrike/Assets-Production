from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button


class ClickableLabel(Button):
    def __init__(self, text:str, section:str, on_click, font_size=15):
        super().__init__(text=text, size_hint=(0.25,0.125),background_normal='',
                         background_color=(0, 0, 0, 0),markup=True, font_size=font_size)
        self.normal_text = text
        self.on_hover_text = f"[u]{text}[/u]"
        self.hover = False
        self.key = section
        self.bind(on_press=on_click)

    def on_hover(self, pos):
        if self.collide_point(*self.to_widget(*pos)):
            self.hover = True
            self.text = self.on_hover_text
        else:
            self.hover = False
            self.text = self.normal_text

            