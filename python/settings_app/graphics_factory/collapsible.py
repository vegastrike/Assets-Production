from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.animation import Animation

from graphics_factory.clickable_label import ClickableLabel

class CollapsibleBox(BoxLayout):
    def __init__(self, title: str, content:BoxLayout, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.collapsed = False

        self.content = content

        # Toggle button
        self.clickable_label = ClickableLabel(text=title.upper(), section=None, font_size=18, on_click=self.toggle)

        # Layout setup
        self.add_widget(self.clickable_label)
        self.add_widget(self.content)

        self.update_height()

    def update_height(self):
        self.height = self.clickable_label.height + (self.content.height if not self.collapsed else 0)

    def toggle(self, *args):
        if self.collapsed:
            # Expand
            anim = Animation(height=100, opacity=1, duration=0.3)
            anim.bind(on_progress=lambda a, w, p: self.update_height())
            anim.start(self.content)
        else:
            # Collapse
            anim = Animation(height=0, opacity=0, duration=0.3)
            anim.bind(on_progress=lambda a, w, p: self.update_height())
            anim.start(self.content)

        self.collapsed = not self.collapsed

class TestApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        root.add_widget(CollapsibleBox())
        return root

if __name__ == '__main__':
    TestApp().run()
