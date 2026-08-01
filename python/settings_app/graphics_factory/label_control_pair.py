import game_config as gc
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.button import Button

import key_utils

from graphics_factory.tooltip import TooltipIcon
from kivy.uix.widget import Widget
from kivy.core.window import Window


class AbstractLeafGui(BoxLayout):
    def __init__(self, parent: BoxLayout, leaf: gc.ConfigLeaf, title = None, tooltip_text = None):
        super().__init__(orientation='horizontal', height=70, size_hint_y=None)
        self.leaf = leaf
        if title is None:
            title = f"{key_utils.format_key(leaf.key)}:" if leaf else ""

        parent.add_widget(self)

        if tooltip_text:
            label = TooltipIcon(text=title, tooltip_text=tooltip_text, valign='middle', halign="left")
            label.bind(size=self.update_text_size)
            self.add_widget(label)
        else:
            label = Label(text=title, valign='middle', halign="left", height = 70)
            label.bind(size=self.update_text_size)
            self.add_widget(label)


    def update_text_size(self, instance, size):
        instance.text_size = size

    def on_change(self, instance, new_value):
        print(f"Control {instance} {new_value} replacing {self.leaf.value}")
        self.leaf.set(new_value=new_value)



class BoolLeafGui(AbstractLeafGui):
    def __init__(self, parent: BoxLayout, leaf: gc.ConfigLeaf, title = None, tooltip_text = None,
                 on_toggle = None):
        super().__init__(parent=parent, leaf=leaf, title=title, tooltip_text=tooltip_text)

        self.toggle_button = CheckBox(active=self.leaf.value, height=70)
        self.add_widget(self.toggle_button)

        if on_toggle:
            self.toggle_button.bind(active=on_toggle)
        else:
            self.toggle_button.bind(active=self.on_change)

        # Set background color to pink
        # with self.canvas.before:
        #     Color(0.2, 0.75, 0.8, 1)  # RGBA for pink
        #     self.rect = Rectangle(size=self.size, pos=self.pos)
        
        # Update rectangle size and position on layout changes
        # self.bind(size=self._update_rect, pos=self._update_rect)

    # def _update_rect(self, instance, value):
    #     self.rect.size = instance.size
    #     self.rect.pos = instance.pos

# TODO: figure out how to differentiate int from float
# isinstance(value, int) returns True only if value is an integer (e.g., 5, -3, 0).
# isinstance(value, float) returns True only if value is a floating-point number (e.g., 3.14, -2.5, 0.0).
# Floats that represent integers - 5.0 is not considered an integer by isinstance(value, int).
# This means config.json needs to be sanitised for this to work properly.
class TextLeafGui(AbstractLeafGui):
    def __init__(self, parent: BoxLayout, leaf: gc.ConfigLeaf, on_change = None, title = None, tooltip_text = None):
        super().__init__(parent=parent, leaf=leaf, title=title, tooltip_text=tooltip_text)

        self.text_field = TextInput(text=str(self.leaf.value), multiline=False, size_hint=(0.8, None), height = 45,
                                       halign='center')
        self.add_widget(self.text_field)

        if on_change:
            self.text_field.bind(text=on_change)
        else:
            self.text_field.bind(text=self.on_change)


        # Set background color to pink
        # with self.canvas.before:
        #     Color(0.2, 0.75, 0.8, 1)  # RGBA for pink
        #     self.rect = Rectangle(size=self.size, pos=self.pos)
        
        # Update rectangle size and position on layout changes
        # self.bind(size=self._update_rect, pos=self._update_rect)

    def on_change(self, instance, value):
        print(f"Text field changed from {self.leaf.value} to {value}")
        try:
            # Attempt to cast the value to the type of the leaf's original value
            if isinstance(self.leaf.value, int):
                self.leaf.set(int(value))
            elif isinstance(self.leaf.value, float):
                self.leaf.set(float(value))
            else:
                self.leaf.set(value)
        except ValueError:
            print(f"Invalid value: {value}. Could not cast to {type(self.leaf.value).__name__}.")

    def update_text_size(self, instance, size):
        instance.text_size = size
        
    # def _update_rect(self, instance, value):
    #     self.rect.size = instance.size
    #     self.rect.pos = instance.pos


class SpinnerLeafGui(AbstractLeafGui):
    def __init__(self, parent: BoxLayout, leaf: gc.ConfigLeaf, initial_value:str, values: list[str], on_change = None, 
                 title = None, tooltip_text = None):
        super().__init__(parent=parent, leaf=leaf, title=title, tooltip_text=tooltip_text)

        self.spinner = Spinner(text=initial_value, values=values, size_hint=(0.8, None), height = 45,
                                       halign='center')
        self.add_widget(self.spinner)

        if on_change:
            self.spinner.bind(text=on_change)
        else:
            self.spinner.bind(text=self.on_change)

    def set_text(self, text):
        self.spinner.text = text
    
    def set_values(self, values):
        self.spinner.values = values


class SpinnerMultiLeafGui(SpinnerLeafGui):
    def __init__(self, parent: BoxLayout, leaf: gc.ConfigLeaf, json:dict,  
                 title = None, tooltip_text = None):
        self.function_name = f"on_{title.lower()}_change"
        
        self.json = json
        keys = list(json.keys())
        if leaf:
            initial_value= leaf.value
        else:
            keys[0]
                                          
        
        super().__init__(parent=parent, leaf=leaf, initial_value=initial_value, values=keys,
                         title=title, tooltip_text=tooltip_text, on_change=self.on_change)


    def on_change(self, instance, new_text):
        print(f"{self.function_name}: {instance} {new_text}")

        # First change the main leaf so we can store the selected value in user config
        self.leaf.set(new_text)

        # Now edit the various values in JSON
        if new_text not in self.json:
            print(f"{self.function_name} error. {new_text} not in json.")
            return

        json_value = self.json[new_text]
        for key, value in json_value.items():
            print(f"Modifying {key} to {value}")
            key_list = key.split('/')
            leaf = gc.game_config.get_object(key=key_list)
            if not leaf:
                print(f"{self.function_name} error. {key} not in game_config.")
                continue
            leaf.set(value)

class CaptureKeyStrokePair(AbstractLeafGui):
        def __init__(self, parent: BoxLayout, key_leaf: gc.ConfigLeaf, modifier_leaf: gc.ConfigLeaf, 
                     title:str, tooltip_text = None):
            super().__init__(parent=parent, leaf=None, title=title, tooltip_text=tooltip_text)
            self.key_leaf = key_leaf
            self.modifier_leaf = modifier_leaf
            text = f"{key_leaf.value} ({modifier_leaf.value})"
            self.keystroke_label = Label(text=text, valign='middle', halign="left", height = 70)
            self.keystroke_label.bind(size=self.update_text_size)
            self.add_widget(self.keystroke_label)
            self._hovered = False
            Window.bind(mouse_pos=self.on_mouse_pos)

        def on_mouse_pos(self, window, pos):
            if self.get_root_window():
                inside = self.collide_point(*self.to_widget(*pos))
                if inside and not self._hovered:
                    self._hovered = True
                    Window.bind(on_key_down=self.on_key_down)
                elif not inside and self._hovered:
                    self._hovered = False
                    Window.unbind(on_key_down=self.on_key_down)

        def on_key_down(self, window, keycode, scancode, codepoint, modifiers):
            # Does not validate not in use.
            # Do we want to? If I want to switch two keys around, I'd need a temp value.
            # TODO: validate?
            modifier = modifiers[0]
            self.key_leaf.set(codepoint)
            self.modifier_leaf.set(modifier)
            text = f"{codepoint} ({modifier})"
            self.keystroke_label.text = text
            if isinstance(keycode, int):
                print(f"Key pressed: {keycode}, {scancode}, {codepoint}, Modifiers: {modifiers}")


class CaptureBindingButton(AbstractLeafGui):
    """A clickable binding entry (keyboard key, mouse button, or joystick button).

    Clicking it enters capture mode: the next matching input (key press, mouse
    click, or joystick button press, depending on device) replaces the binding.

    The binding is a dict from the config `actions` section, e.g.
    {"key": "space", "modifier": "none"} (keyboard),
    {"button": 2, "modifier": "none"} (mouse),
    {"joystick": 0, "button": 1, "modifier": "none"} (joystick).

    On capture, on_capture(binding_dict) is called so the caller can write
    the updated array back to the config leaf.
    """
    def __init__(self, parent: BoxLayout, binding: dict, device: str, title: str = None,
                 on_capture = None):
        # leaf=None: this widget does not own a ConfigLeaf; the caller does
        # (the per-device array leaf). We just show/capture a single entry.
        super().__init__(parent=parent, leaf=None, title=title)
        self.binding = binding
        self.device = device          # 'keyboard' | 'mouse' | 'joystick' | 'hat'
        self.on_capture = on_capture
        self._capturing = False

        self.button = Button(text=self.format_binding(), size_hint=(0.8, None), height=45)
        self.add_widget(self.button)
        self.button.bind(on_press=self.on_click)

    def format_binding(self):
        b = self.binding
        if self.device == 'keyboard':
            mod = b.get('modifier', 'none')
            return f"{b.get('key', '?')} ({mod})" if mod != 'none' else str(b.get('key', '?'))
        if self.device == 'mouse':
            return f"Mouse {b.get('button', '?')}"
        if self.device == 'joystick':
            return f"Joy {b.get('joystick', 0)} Btn {b.get('button', '?')}"
        if self.device == 'hat':
            return f"Hat {b.get('hatswitch', '?')} {b.get('direction', '')}".strip()
        return str(b)

    def on_click(self, instance):
        if self._capturing:
            # Already capturing; click again to cancel
            self._stop_capture()
            return
        self._start_capture()

    def _start_capture(self):
        self._capturing = True
        self.button.text = "Press..."
        if self.device == 'keyboard':
            Window.bind(on_key_down=self._on_key)
        elif self.device == 'mouse':
            Window.bind(on_touch_down=self._on_mouse)
        elif self.device in ('joystick', 'hat'):
            Window.bind(on_joy_button_down=self._on_joy)

    def _stop_capture(self):
        self._capturing = False
        self.button.text = self.format_binding()
        Window.unbind(on_key_down=self._on_key)
        Window.unbind(on_touch_down=self._on_mouse)
        Window.unbind(on_joy_button_down=self._on_joy)

    def _on_key(self, window, keycode, scancode, codepoint, modifiers):
        # Special keys (tab, arrows, F-keys...) have no codepoint; map the
        # SDL keycode to the engine's key name. Printable keys use codepoint.
        import key_utils
        engine_key = key_utils.keycode_to_engine_name(keycode, codepoint)
        if not engine_key:
            return
        new_binding = {"key": engine_key, "modifier": (modifiers[0] if modifiers else 'none')}
        self._finish(new_binding)

    def _on_mouse(self, window, touch):
        # touch.button is 'left'/'right'/'middle' or an int for extra buttons
        button = touch.button
        # Convert common names to the engine's numeric convention
        btn_map = {'left': 0, 'middle': 1, 'right': 2, 'scrollup': 3, 'scrolldown': 4}
        if isinstance(button, str) and button in btn_map:
            btn = btn_map[button]
        elif isinstance(button, int):
            btn = button
        else:
            return
        new_binding = {"button": btn, "modifier": "none"}
        self._finish(new_binding)

    def _on_joy(self, window, stickid, buttonid):
        if self.device == 'hat':
            new_binding = {"hatswitch": buttonid, "button": 0, "modifier": "none"}
        else:
            new_binding = {"joystick": stickid, "button": buttonid, "modifier": "none"}
        self._finish(new_binding)

    def _finish(self, new_binding):
        self._stop_capture()
        self.binding = new_binding
        if self.on_capture:
            self.on_capture(new_binding)
        self.button.text = self.format_binding()
            
class SliderLeafGui(AbstractLeafGui):
    def __init__(self, parent: BoxLayout, leaf: gc.ConfigLeaf, min=0, max=100, step=1, title=None, tooltip_text=None, on_change=None):
        super().__init__(parent=parent, leaf=leaf, title=title, tooltip_text=tooltip_text)

        self.add_widget(Label(text=str(min), size_hint_x=0.1))

        self.volume_slider = Slider(min=min, max=max, value=self.leaf.value, size_hint_x=0.7, step=step)
        self.add_widget(self.volume_slider)

        self.add_widget(Label(text=str(max), size_hint_x=0.1))

        if on_change:
            self.volume_slider.bind(value=on_change)
        else:
            self.volume_slider.bind(value=self.on_slider_change)

    def on_slider_change(self, instance, value):
        print(f"Slider changed from {self.leaf.value} to {value}")
        self.leaf.set(value)


class LiveAxisSlider(BoxLayout):
    """A live-updating slider for one physical joystick axis.

    Binds to the window's on_joy_axis events for (stickid, axisid) and
    reflects the current -1..1 value. Clicking it (in capture mode) selects
    it as the axis for the role being configured.
    """
    def __init__(self, stickid: int, axisid: int, label_text: str = None, on_select=None, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=40, **kwargs)
        self.stickid = stickid
        self.axisid = axisid
        self.on_select = on_select

        label_text = label_text or f"A{axisid}"
        self.label = Label(text=label_text, size_hint_x=0.2, halign='left')
        self.add_widget(self.label)

        self.slider = Slider(min=-1, max=1, value=0, size_hint_x=0.7)
        self.slider.disabled = True   # display-only; not user-draggable
        self.add_widget(self.slider)

        self.select_btn = Button(text="pick", size_hint_x=0.15, height=40, size_hint_y=None)
        self.select_btn.bind(on_press=lambda _: self.on_select(self.stickid, self.axisid) if self.on_select else None)
        self.add_widget(self.select_btn)

        # Live update from Kivy's SDL2 joystick provider
        from kivy.core.window import Window
        Window.bind(on_joy_axis=self.on_joy_axis)

    def on_joy_axis(self, window, stickid, axisid, value):
        if stickid == self.stickid and axisid == self.axisid:
            # SDL axis values are raw 16-bit (-32768..32767); normalize to -1..1
            self.slider.value = value / 32767.0

    def set_selected(self, selected: bool):
        self.select_btn.text = "*" if selected else "pick"
        self.select_btn.background_color = (0.2, 0.8, 0.2, 1) if selected else (0.5, 0.5, 0.5, 1)


class AxisCaptureRow(BoxLayout):
    """One row for one axis role (x/y/z/throttle).

    Shows live sliders for every joystick axis observed via on_joy_axis,
    plus a capture button that runs deflection detection over a window and
    picks the clearest-moving axis (or reverts if ambiguous).
    """
    DETECT_WINDOW = 2.0     # seconds
    WINNER_RATIO = 1.8      # winner deflection must exceed 2nd by this ratio
    WINNER_FLOOR = 0.15     # and exceed this absolute deflection to count

    def __init__(self, parent: BoxLayout, role: str, role_leaf: gc.ConfigBranch, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, height=160, **kwargs)
        parent.add_widget(self)

        self.role = role
        self.role_leaf = role_leaf
        self.live_sliders = {}      # (stickid, axisid) -> LiveAxisSlider
        self._detecting = False
        self._deflection = {}       # (stickid, axisid) -> (min, max)

        # Header: role name + source + current axis
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.add_widget(header)
        header.add_widget(Label(text=role, size_hint_x=0.15, halign='left', bold=True))

        # Source spinner (joystick/mouse)
        if role_leaf.has_key(["source"]):
            self.source_leaf = role_leaf.get_object(["source"])
            self.source_spinner = Spinner(text=self.source_leaf.value, values=["joystick", "mouse"],
                                          size_hint_x=0.2)
            self.source_spinner.bind(text=self._on_source_change)
            header.add_widget(self.source_spinner)
        else:
            self.source_leaf = None
            self.source_spinner = None

        # Current axis display
        self.axis_leaf = role_leaf.get_object(["axis"]) if role_leaf.has_key(["axis"]) else None
        self.current_axis_label = Label(text=f"axis: {self.axis_leaf.value if self.axis_leaf else '?'}",
                                        size_hint_x=0.2)
        header.add_widget(self.current_axis_label)

        # Detect button
        detect_btn = Button(text="wiggle to detect", size_hint_x=0.25, height=40, size_hint_y=None)
        detect_btn.bind(on_press=lambda _: self._start_detect())
        header.add_widget(detect_btn)

        # Inverse toggle
        if role_leaf.has_key(["inverse"]):
            self.inverse_leaf = role_leaf.get_object(["inverse"])
            inv_gui = BoolLeafGui(parent=header, leaf=self.inverse_leaf, title="inverse")
            inv_gui.size_hint_x = 0.15
            inv_gui.height = 40
        else:
            self.inverse_leaf = None

        # Live sliders area (populated as axes produce events)
        self.sliders_area = BoxLayout(orientation='vertical', size_hint_y=None)
        self.sliders_area.bind(minimum_height=self.sliders_area.setter('height'))
        self.add_widget(self.sliders_area)

        # Watch for all axes to populate live sliders
        from kivy.core.window import Window
        Window.bind(on_joy_axis=self._watch_axes)

    def _watch_axes(self, window, stickid, axisid, value):
        # Populate a live slider the first time an axis is seen
        key = (stickid, axisid)
        if key not in self.live_sliders:
            slider = LiveAxisSlider(stickid=stickid, axisid=axisid,
                                    label_text=f"Joy{stickid} A{axisid}",
                                    on_select=self._on_slider_select)
            self.live_sliders[key] = slider
            self.sliders_area.add_widget(slider)
            # Mark selected if it matches the configured axis
            self._update_selected()
        # Track deflection during detection (normalize raw SDL to -1..1)
        if self._detecting:
            v = value / 32767.0
            if key not in self._deflection:
                self._deflection[key] = [v, v]
            else:
                lo, hi = self._deflection[key]
                self._deflection[key] = [min(lo, v), max(hi, v)]

    def _on_slider_select(self, stickid, axisid):
        # Direct click: assign immediately
        self._assign_axis(stickid, axisid)

    def _start_detect(self):
        if self._detecting:
            return
        self._detecting = True
        self._deflection = {}
        # Seed the baseline with current slider values so a wiggle already in
        # progress (or a slow single movement) still registers.
        for (stickid, axisid), slider in self.live_sliders.items():
            v = slider.slider.value
            self._deflection[(stickid, axisid)] = [v, v]
        from kivy.clock import Clock
        Clock.schedule_once(self._finish_detect, self.DETECT_WINDOW)

    def _finish_detect(self, dt):
        self._detecting = False
        if not self._deflection:
            print(f"[{self.role}] No axis movement detected during window.")
            return

        # Compute deflection per axis and rank
        deflections = {key: (hi - lo) for key, (lo, hi) in self._deflection.items()}
        ranked = sorted(deflections.items(), key=lambda kv: kv[1], reverse=True)
        winner_key, winner_def = ranked[0]
        runner_up_def = ranked[1][1] if len(ranked) > 1 else 0.0

        print(f"[{self.role}] detect: {deflections}")

        if winner_def < self.WINNER_FLOOR:
            print(f"[{self.role}] No clear winner (deflection {winner_def} < floor {self.WINNER_FLOOR}). Reverting.")
            return
        if len(ranked) > 1 and runner_up_def > 0 and (winner_def / runner_up_def) < self.WINNER_RATIO:
            print(f"[{self.role}] Ambiguous (winner {winner_def} vs runner-up {runner_up_def}). Reverting.")
            return

        self._assign_axis(*winner_key)

    def _assign_axis(self, stickid, axisid):
        print(f"[{self.role}] Assigning axis: stick={stickid} axis={axisid}")
        if self.axis_leaf:
            self.axis_leaf.set(axisid)
            self.current_axis_label.text = f"axis: {axisid}"
        # Also record which joystick this axis is on (stickid)
        if self.role_leaf.has_key(["joystick"]):
            self.role_leaf.get_object(["joystick"]).set(stickid)
        self._update_selected()

    def _update_selected(self):
        cur = (0, self.axis_leaf.value) if self.axis_leaf else None
        for key, slider in self.live_sliders.items():
            slider.set_selected(cur is not None and key == cur)

    def _on_source_change(self, instance, text):
        if self.source_leaf:
            self.source_leaf.set(text)

        



# Test Code
if __name__ == "__main__":
    pass
    