from kivy.core.window import Window
from kivy.properties import BooleanProperty, ObjectProperty, ListProperty
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle, Line

# This is a singleton FloatLayout so our tooltip can float freely
root_layout = None

class HoverBehavior(object):
    hovered = BooleanProperty(False)
    border_point = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._binded = False
        Window.bind(mouse_pos=self.on_mouse_pos)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return  # Not in a window yet
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            return
        self.hovered = inside
        self.border_point = pos
        if inside:
            self.on_hover()
        else:
            self.on_unhover()

    def on_hover(self):
        pass

    def on_unhover(self):
        pass



class Tooltip(Label):
    background_color = ListProperty([1, 1, 0, 0.9])  # Yellow with some transparency
    border_color = ListProperty([1, 1, 1, 1])        # White

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.text_size = (None, None)
        self.padding = (8, 5)
        self.color = (0, 0, 0, 1)  # Black text
        self.font_size = '12sp'
        self.opacity = 0
        self.height = 30

        self.bind(pos=self._update_canvas,
                  size=self._update_canvas,
                  background_color=self._update_canvas,
                  border_color=self._update_canvas)

        with self.canvas.before:
            self._bg_color = Color(*self.background_color)
            self._bg_rect = Rectangle(pos=self.pos, size=self.size)

            self._border_color = Color(*self.border_color)
            self._border_line = Line(rectangle=(*self.pos, *self.size), width=1)

    def _update_canvas(self, *args):
        self._bg_color.rgba = self.background_color
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size

        self._border_color.rgba = self.border_color
        self._border_line.rectangle = (*self.pos, *self.size)

class TooltipIcon(Label, HoverBehavior):
    tooltip = None

    def __init__(self, text, tooltip_text, **kwargs):
        text = text or "🛈:"
        super().__init__(text=text, **kwargs)
        self.tooltip = Tooltip(text=tooltip_text)
        Clock.schedule_once(self.add_tooltip)


    def add_tooltip(self, *args):
        global root_layout
        if root_layout:
            root_layout.add_widget(self.tooltip)

    def on_hover(self):
        if not self.tooltip:
            return

        x, y = self.border_point
        self.tooltip.pos = (x + 10, y - 10)
        self.tooltip.opacity = 1

    def on_unhover(self):
        if self.tooltip:
            self.tooltip.opacity = 0

# For testing only

from kivy.app import App
from kivy.uix.button import Button


class TooltipButton(Button, HoverBehavior):
    tooltip = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tooltip = Tooltip(text="I'm a tooltip!")
        Clock.schedule_once(self.add_tooltip)

    def add_tooltip(self, *args):
        if self.parent:
            self.parent.add_widget(self.tooltip)

    def on_hover(self):
        if not self.tooltip:
            return
        x, y = self.border_point
        self.tooltip.pos = (x + 10, y - 10)
        self.tooltip.opacity = 1

    def on_unhover(self):
        if self.tooltip:
            self.tooltip.opacity = 0

class TooltipApp(App):
    def build(self):
        global root_layout
        root_layout = FloatLayout()
        btn = TooltipButton(text="Hover me", size_hint=(None, None), size=(150, 50), pos=(200, 200))
        root_layout.add_widget(btn)
        return root_layout


if __name__ == '__main__':
    TooltipApp().run()