from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle

class DividerLine(Widget):
    def __init__(self, color=(0.6, 0.6, 0.6, 1), height=1, **kwargs):
        super().__init__(size_hint_y=None, height=height, **kwargs)
        with self.canvas:
            Color(*color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

# layout.add_widget(DividerLine())

class VerticalDivider(Widget):
    def __init__(self, color=(0.6, 0.6, 0.6, 1), width=1, **kwargs):
        super().__init__(size_hint_x=None, width=width, **kwargs)
        with self.canvas:
            Color(*color)
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, *args):
        self.rect.size = self.size
        self.rect.pos = self.pos

# row = BoxLayout(orientation='horizontal')
# row.add_widget(Label(text="Left"))
# row.add_widget(VerticalDivider())
# row.add_widget(Label(text="Right"))