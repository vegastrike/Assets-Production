from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button

import game_config as gc

from graphics_factory.divider import DividerLine
from graphics_factory.label_control_pair import (BoolLeafGui, SliderLeafGui, TextLeafGui,
                                                 AxisExplorer)


def _set_leaf(gc_obj, path, value):
    leaf = gc_obj.get_object(path)
    if leaf is not None:
        leaf.set(value)


class FlightControlSelector(BoxLayout):
    """A single mutually-exclusive selector for the flight-control device.

    Keyboard is always active; this picks whether the mouse, the joystick, or
    neither additionally drives flight. Selecting one disables the others and
    swaps the visible option box inside a fixed options container. Writes the
    coherent set:
      Keyboard -> mouse.enabled=false, joystick.enabled=false
      Mouse    -> mouse.enabled=true,  joystick.enabled=false, x/y source=mouse
      Joystick -> mouse.enabled=false, joystick.enabled=true,  x/y source=joystick
    """
    def __init__(self, parent, options_container, mode_boxes=None, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=50, **kwargs)
        parent.add_widget(self)
        # options_container: a single BoxLayout that stays fixed in the layout;
        # _apply_mode clears it and re-adds only the selected mode's boxes.
        self.options_container = options_container
        self.mode_boxes = mode_boxes or {}
        self.add_widget(Label(text="Flight control device:", size_hint_x=0.4, halign='left'))
        self.spinner = Spinner(values=["Keyboard", "Mouse", "Joystick"], size_hint_x=0.3)
        self.spinner.text = self._current_mode()
        self.spinner.bind(text=self._on_change)
        self.add_widget(self.spinner)
        self.add_widget(Label(text="(keyboard is always enabled)", size_hint_x=0.3, halign='left',
                              font_size='12sp', color=(0.7, 0.7, 0.7, 1)))
        self._apply_mode(self.spinner.text)

    def _current_mode(self):
        mouse = gc.game_config.get_object(["mouse", "enabled"])
        joy = gc.game_config.get_object(["joystick", "enabled"])
        mouse_on = bool(mouse.value) if mouse else False
        joy_on = bool(joy.value) if joy else False
        if mouse_on and not joy_on:
            return "Mouse"
        if joy_on and not mouse_on:
            return "Joystick"
        return "Keyboard"

    def _apply_mode(self, mode):
        """Clear the options container, then add only this mode's boxes.

        The options container is a fixed child of the parent, so ordering is
        always correct and no hidden widgets can overlay the selector.
        """
        self.options_container.clear_widgets()
        for box in self.mode_boxes.get(mode, []):
            self.options_container.add_widget(box)

    def _on_change(self, instance, text):
        axes = gc.game_config.get_object(["axes"])
        if text == "Mouse":
            _set_leaf(gc.game_config, ["mouse", "enabled"], True)
            _set_leaf(gc.game_config, ["joystick", "enabled"], False)
            if axes is not None:
                for role in ("x", "y"):
                    role_leaf = axes.get_object([role])
                    if role_leaf is not None and role_leaf.has_key(["source"]):
                        role_leaf.get_object(["source"]).set("mouse")
        elif text == "Joystick":
            _set_leaf(gc.game_config, ["mouse", "enabled"], False)
            _set_leaf(gc.game_config, ["joystick", "enabled"], True)
            if axes is not None:
                for role in ("x", "y"):
                    role_leaf = axes.get_object([role])
                    if role_leaf is not None and role_leaf.has_key(["source"]):
                        role_leaf.get_object(["source"]).set("joystick")
        else:  # Keyboard
            _set_leaf(gc.game_config, ["mouse", "enabled"], False)
            _set_leaf(gc.game_config, ["joystick", "enabled"], False)
        self._apply_mode(text)
        print(f"Flight control device set to: {text}")


class ControlsTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.padding = 10

        self.tab_name = "Controls"

        # Scrollable content area (same pattern as the Bindings tab): the
        # ScrollView fills the tab, the inner layout sizes to its content and
        # sits at the top.
        scroll_view = ScrollView(size_hint=(1, 1))
        content = BoxLayout(orientation='vertical', size_hint_y=None)
        content.bind(minimum_height=content.setter('height'))
        scroll_view.add_widget(content)
        self.add_widget(scroll_view)

        # Title
        title_label = Label(text="Controls".upper(), font_size=24, size_hint=(0.8, None), height=80,
                            halign='center')
        content.add_widget(title_label)
        content.add_widget(DividerLine())

        # Flight-control device selector (swaps which option box is shown).
        # Each box has a fixed height; the outer ScrollView handles overflow.
        self.mouse_box = BoxLayout(orientation="vertical", size_hint_y=None, height=280,
                                   padding=(0, 12, 0, 0))
        self.axes_box = BoxLayout(orientation="vertical", size_hint_y=None, height=560,
                                  padding=(0, 12, 0, 0))
        # A container the selector fills with the current mode's box(es).
        # It sizes to its contents via minimum_height (so Joystick mode with
        # both boxes never overflows/overlaps the selector above); the outer
        # ScrollView handles any overflow.
        self.options_container = BoxLayout(orientation="vertical", size_hint_y=None,
                                           height=0)
        self.options_container.bind(
            minimum_height=self.options_container.setter('height'))
        mode_boxes = {"Keyboard": [], "Mouse": [self.mouse_box],
                      "Joystick": [self.axes_box]}
        FlightControlSelector(parent=content, options_container=self.options_container,
                              mode_boxes=mode_boxes)

        # Keyboard is always enabled - informational only.
        content.add_widget(Label(text="Keyboard is always enabled.", font_size=14,
                                 size_hint=(0.9, None), height=30, halign='left'))

        # The option boxes live here, populated by the selector per mode.
        content.add_widget(self.options_container)

        # ---- Mouse options (shown only in Mouse mode) ----
        self.mouse_box.add_widget(Label(text="Mouse".upper(), font_size=18,
                                        size_hint=(0.8, None), height=60, halign='center'))
        for path, kwargs in [
            (["mouse", "inverse_x"], {}),
            (["mouse", "inverse_y"], {}),
        ]:
            leaf = gc.game_config.get_object(path)
            if leaf is not None:
                BoolLeafGui(parent=self.mouse_box, leaf=leaf, title=path[-1])
        warp_leaf = gc.game_config.get_object(["joystick", "warp_mouse"])
        if warp_leaf is not None:
            BoolLeafGui(parent=self.mouse_box, leaf=warp_leaf, title="warp mouse")
        for path, minv, maxv, step in [
            (["joystick", "mouse_sensitivity"], 20, 200, 10),
        ]:
            leaf = gc.game_config.get_object(path)
            if leaf is not None:
                SliderLeafGui(parent=self.mouse_box, leaf=leaf, min=minv, max=maxv, step=step,
                              title="mouse sensitivity")

        # ---- Joystick (shown only in Joystick mode) ----
        self.axes_box.add_widget(Label(text="Joystick".upper(), font_size=18,
                                       size_hint=(0.8, None), height=50, halign='center'))

        # Deadband is a single global setting applied to all joystick axes, so
        # it lives above the sliders (not per axis): a type-in number box plus
        # an 'Auto deadband' button that sets it from the current stick.
        self.deadband_leaf = gc.game_config.get_object(["joystick", "deadband"])
        deadband_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.axes_box.add_widget(deadband_row)
        self.deadband_input = None
        if self.deadband_leaf is not None:
            self.deadband_input = TextLeafGui(parent=deadband_row, leaf=self.deadband_leaf,
                                              title="deadband")
        auto_btn = Button(text="Auto deadband", size_hint_x=0.3, height=40, size_hint_y=None)
        auto_btn.bind(on_press=lambda _: self._auto_deadband())
        deadband_row.add_widget(auto_btn)

        self.axes_box.add_widget(Label(text="The sliders show the live joystick axis positions.",
                                       size_hint=(0.9, None), height=30, halign='center'))
        axes = gc.game_config.get_object(["axes"])
        if axes is not None:
            roles = {role: axes.get_object([role]) for role in sorted(axes.value.keys())}
            explorer = AxisExplorer(parent=self.axes_box, roles=roles)
            self.axes_explorer = explorer
        else:
            self.axes_explorer = None
            self.axes_box.add_widget(Label(text="No 'axes' section found in config.json",
                                           height=40, size_hint_y=None))

    def _auto_deadband(self, _dt=None):
        """Set the deadband to cover the worst resting deflection of the bound
        axes (the engine's deadzone is symmetric around 0, so it must exceed the
        stick's resting offset or the ship drifts).

        Samples the bound axes for about a second, tracking the maximum
        |deflection| seen, then sets deadband = max + jitter headroom.
        """
        if self.deadband_leaf is None:
            return
        explorer = getattr(self, 'axes_explorer', None)
        if explorer is None:
            return
        if getattr(self, '_db_sampling', False):
            return
        self._db_sampling = True
        self._db_max = 0.0
        self._db_samples = 0
        from kivy.clock import Clock
        Clock.schedule_interval(self._db_sample, 0.1)

    def _db_sample(self, dt):
        """One sampling tick: track max bound-axis deflection; finish after ~1s."""
        explorer = getattr(self, 'axes_explorer', None)
        if explorer is not None:
            self._db_max = max(self._db_max, explorer.max_deflection())
        self._db_samples += 1
        if self._db_samples >= 10:   # ~1s at 0.1s ticks
            self._finish_auto_deadband()

    def _finish_auto_deadband(self):
        from kivy.clock import Clock
        Clock.unschedule(self._db_sample)
        self._db_sampling = False
        deadband = max(0.0, min(0.5, self._db_max + 0.05))
        self.deadband_leaf.set(deadband)
        # Refresh the number box so the new value is visible (TextLeafGui only
        # updates its text from typing, not from a programmatic leaf change).
        if self.deadband_input is not None:
            self.deadband_input.text_field.text = f"{deadband:.3f}"
        print(f"Auto deadband set to {deadband:.3f} (max resting deflection {self._db_max:.3f})")



    

