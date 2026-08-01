import game_config as gc
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView

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

        if title:
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

class CaptureBindingButton(AbstractLeafGui):
    """A clickable binding entry. Clicking it opens a modal capture dialog;
    the next input (key press, mouse click, or joystick button) is detected
    there with Accept/Retry/Cancel controls.

    The binding is a dict from the config `actions` section, e.g.
    {"key": "space", "modifier": "none"} (keyboard),
    {"button": 2, "modifier": "none"} (mouse),
    {"joystick": 0, "button": 1, "modifier": "none"} (joystick).

    On capture, on_capture(device, binding_dict) is called.
    """
    def __init__(self, parent: BoxLayout, binding: dict, device: str, title: str = None,
                 on_capture = None):
        super().__init__(parent=parent, leaf=None, title=title)
        # AbstractLeafGui defaults to a fixed 70px height; fill the row
        # instead so the centered button aligns with sibling rows.
        self.size_hint_y = 1.0
        self.binding = binding
        self.device = device
        self.on_capture = on_capture

        self.button = Button(text=self.format_binding(), size_hint=(0.8, None), height=35,
                             pos_hint={'center_y': 0.5})
        self.add_widget(self.button)
        self.button.bind(on_press=self.on_click)

    @staticmethod
    def device_from_binding(binding: dict) -> str:
        if 'key' in binding:
            return 'keyboard'
        if 'hatswitch' in binding:
            return 'hat'
        if 'joystick' in binding:
            return 'joystick'
        if 'button' in binding:
            return 'mouse'
        return 'keyboard'

    def format_binding(self):
        return CaptureBindingButton.format_binding_for(self.device, self.binding)

    @staticmethod
    def format_binding_for(device, binding):
        b = binding
        if device == 'keyboard':
            import key_utils
            mod = b.get('modifier', 'none')
            key = key_utils.format_key_display(b.get('key', '?'))
            return f"{key} ({mod})" if mod != 'none' else key
        if device == 'mouse':
            return f"Mouse {b.get('button', '?')}"
        if device == 'joystick':
            return f"Joy {b.get('joystick', 0)} Btn {b.get('button', '?')}"
        if device == 'hat':
            b = binding
            if 'direction' in b and 'axis' in b:
                return f"HatAxis{b.get('axis')} {b.get('direction')}"
            if 'direction' in b:
                return f"Hat {b.get('hatswitch', '?')} {b.get('direction', '')}".strip()
            return f"Hat {b.get('hatswitch', '?')} btn {b.get('button', '?')}"
        return str(b)

    def on_click(self, instance):
        # Open a modal capture dialog; the overlay makes the whole app inert
        # while waiting for input, so nothing else can steal the click.
        dialog = BindingCaptureDialog(
            on_capture=lambda device, new_binding: self._accept(device, new_binding))
        dialog.open()

    def _accept(self, device, new_binding):
        if new_binding is None:
            return  # cancelled; keep the old binding
        self.binding = new_binding
        self.device = device
        self.button.text = self.format_binding()
        if self.on_capture:
            self.on_capture(device, new_binding)


class BindingCaptureDialog(ModalView):
    """Modal capture dialog. While open, the overlay swallows every touch,
    so the rest of the app is inert. Any key press (including Esc), mouse
    click, or joystick button is captured and shown; the user then chooses
    Accept / Retry / Cancel. On accept, on_capture(device, binding_dict) is
    called; on cancel, on_capture(None, None) is called.
    """
    auto_dismiss = False  # only close via Accept/Retry/Cancel/Esc

    def __init__(self, on_capture, **kwargs):
        super().__init__(size_hint=(0.5, None), height=250, **kwargs)
        self.on_capture = on_capture
        self._binding = None

        layout = BoxLayout(orientation='vertical', padding=20, spacing=12)
        self.add_widget(layout)

        self._status = Label(
            text="Press any key / click a mouse button / press a joystick button...",
            size_hint_y=0.4, halign='center', valign='middle')
        self._status.bind(size=lambda inst, sz: setattr(inst, 'text_size', sz))
        layout.add_widget(self._status)

        self._captured = Label(text="", size_hint_y=0.3, halign='center', valign='middle',
                               font_size=20, bold=True)
        self._captured.bind(size=lambda inst, sz: setattr(inst, 'text_size', sz))
        layout.add_widget(self._captured)

        buttons = BoxLayout(orientation='horizontal', spacing=12, size_hint_y=0.3)
        layout.add_widget(buttons)

        accept = Button(text="Accept", disabled=True)
        accept.bind(on_press=lambda _: self._accept())
        buttons.add_widget(accept)
        self._accept_btn = accept

        retry = Button(text="Retry")
        retry.bind(on_press=lambda _: self._retry())
        buttons.add_widget(retry)

        cancel = Button(text="Cancel")
        cancel.bind(on_press=lambda _: self._cancel())
        buttons.add_widget(cancel)

        # Clicks on the dialog's own buttons are controls, not bindings.
        self._own_buttons = [accept, retry, cancel]

        # Capture input while open (device auto-detect: first to fire wins)
        Window.bind(on_key_down=self._on_key)
        Window.bind(on_touch_down=self._on_mouse)
        Window.bind(on_joy_button_down=self._on_joy_button)
        Window.bind(on_joy_hat=self._on_joy_hat)

    # --- input handlers ---

    def _on_key(self, window, keycode, scancode, codepoint, modifiers):
        # Return True to consume the event: window_sdl2 dispatches on_keyboard
        # (which quits the app on Esc via exit_on_escape) only when on_key_down
        # returns falsy. Consuming every key here keeps the app alive while
        # the capture dialog is open.
        import key_utils
        if keycode in key_utils.MODIFIER_KEYCODES:
            return True
        engine_key = key_utils.keycode_to_engine_name(keycode, codepoint)
        if not engine_key:
            return True
        # Shift is not stored as a modifier (the engine encodes it in the
        # codepoint: Shift+= -> '+'); apply it to printable characters.
        if 'shift' in modifiers:
            engine_key = key_utils.shift_apply(engine_key)
        engine_mod = next((m for m in ('ctrl', 'alt') if m in modifiers), 'none')
        self._set_binding({'key': engine_key, 'modifier': engine_mod})
        return True

    def _on_mouse(self, window, touch):
        # Ignore clicks on our own buttons (Accept/Retry/Cancel) - those are
        # the dialog controls, not the binding being captured.
        if any(btn.collide_point(touch.x, touch.y) for btn in self._own_buttons):
            return
        button = touch.button
        btn_map = {'left': 0, 'middle': 1, 'right': 2, 'scrollup': 3, 'scrolldown': 4}
        if isinstance(button, str) and button in btn_map:
            btn = btn_map[button]
        elif isinstance(button, int):
            btn = button
        else:
            return
        self._set_binding({'button': btn, 'modifier': 'none'})

    def _on_joy_button(self, window, stickid, buttonid):
        self._set_binding({'joystick': stickid, 'button': buttonid, 'modifier': 'none'})

    def _on_joy_hat(self, window, stickid, hatid, direction):
        # A real HAT (e.g. Switch D-pad): direction is an (dx, dy) tuple of
        # -1/0/1. Map to the engine's VS_HAT_* names.
        dx, dy = direction
        name = None
        if dx == 0 and dy == 0:
            name = 'center'
        elif dx == 0 and dy == 1:
            name = 'up'
        elif dx == 0 and dy == -1:
            name = 'down'
        elif dx == 1 and dy == 0:
            name = 'right'
        elif dx == -1 and dy == 0:
            name = 'left'
        elif dx == 1 and dy == 1:
            name = 'rightup'
        elif dx == 1 and dy == -1:
            name = 'rightdown'
        elif dx == -1 and dy == 1:
            name = 'leftup'
        elif dx == -1 and dy == -1:
            name = 'leftdown'
        if name is None:
            return
        self._set_binding({'joystick': stickid, 'hatswitch': hatid, 'direction': name})

    # --- flow ---

    def _set_binding(self, binding):
        self._binding = binding
        self._captured.text = CaptureBindingButton.format_binding_for(
            CaptureBindingButton.device_from_binding(binding), binding)
        self._accept_btn.disabled = False

    def _retry(self):
        self._binding = None
        self._captured.text = ""
        self._accept_btn.disabled = True

    def _accept(self):
        if self._binding is None:
            return
        self._cleanup()
        self.dismiss()
        self.on_capture(CaptureBindingButton.device_from_binding(self._binding), self._binding)

    def _cancel(self):
        self._cleanup()
        self.dismiss()
        self.on_capture(None, None)

    def _cleanup(self):
        Window.unbind(on_key_down=self._on_key)
        Window.unbind(on_touch_down=self._on_mouse)
        Window.unbind(on_joy_button_down=self._on_joy_button)
        Window.unbind(on_joy_hat=self._on_joy_hat)


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


class AxisExplorer(BoxLayout):
    """One shared live display of every joystick axis observed via on_joy_axis.

    A single set of live sliders (no duplication across role rows). A role
    selector says which role a 'pick' assigns to.
    """
    def __init__(self, parent: BoxLayout, roles: dict, **kwargs):
        # roles: {role_name: role_leaf}
        super().__init__(orientation='vertical', size_hint_y=None, height=300, **kwargs)
        parent.add_widget(self)

        self.roles = roles
        self.live_sliders = {}      # (stickid, axisid) -> LiveAxisSlider
        self._pick_target = None    # HatAxisRow in pick mode, else None

        # Header: role selector + hint
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.add_widget(header)
        header.add_widget(Label(text="Assign to role:", size_hint_x=0.3))
        self.role_spinner = Spinner(text=sorted(roles.keys())[0], values=sorted(roles.keys()),
                                    size_hint_x=0.3)
        header.add_widget(self.role_spinner)

        # Live sliders area
        self.sliders_area = BoxLayout(orientation='vertical', size_hint_y=None)
        self.sliders_area.bind(minimum_height=self.sliders_area.setter('height'))
        self.add_widget(self.sliders_area)

        from kivy.core.window import Window
        Window.bind(on_joy_axis=self._watch_axes)

    def _watch_axes(self, window, stickid, axisid, value):
        key = (stickid, axisid)
        if key not in self.live_sliders:
            slider = LiveAxisSlider(stickid=stickid, axisid=axisid,
                                    label_text=f"Joy{stickid} A{axisid}",
                                    on_select=self._on_pick)
            self.live_sliders[key] = slider
            self.sliders_area.add_widget(slider)
            self._update_selected()

    def set_pick_target(self, hat_row):
        self._pick_target = hat_row
        self._update_selected()

    def _on_pick(self, stickid, axisid):
        # If a hat row is in pick mode, assign there; otherwise to a role.
        if self._pick_target is not None:
            self._pick_target.accept_pick(stickid, axisid)
            self._pick_target = None
            return
        role = self.role_spinner.text
        role_leaf = self.roles.get(role)
        if role_leaf is None:
            return
        if role_leaf.has_key(["axis"]):
            role_leaf.get_object(["axis"]).set(axisid)
        if role_leaf.has_key(["joystick"]):
            role_leaf.get_object(["joystick"]).set(stickid)
        print(f"Assigned axis {stickid}/{axisid} to role '{role}'")
        self._update_selected()

    def _update_selected(self):
        # Highlight sliders that match any role's assigned axis
        assigned = set()
        for role, role_leaf in self.roles.items():
            if role_leaf.has_key(["axis"]):
                a = role_leaf.get_object(["axis"]).value
                j = role_leaf.get_object(["joystick"]).value if role_leaf.has_key(["joystick"]) else 0
                assigned.add((j, a))
        for key, slider in self.live_sliders.items():
            slider.set_selected(key in assigned)


class RoleAxisRow(BoxLayout):
    """One compact row per axis role: role name, assigned axis, detect button."""
    DETECT_WINDOW = 2.0
    WINNER_RATIO = 1.8
    WINNER_FLOOR = 0.15

    def __init__(self, parent: BoxLayout, role: str, role_leaf: gc.ConfigBranch,
                 explorer: AxisExplorer, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=50, **kwargs)
        parent.add_widget(self)

        self.role = role
        self.role_leaf = role_leaf
        self.explorer = explorer
        self._detecting = False
        self._deflection = {}

        self.add_widget(Label(text=role, size_hint_x=0.15, halign='left', bold=True))

        # Source spinner
        if role_leaf.has_key(["source"]):
            self.source_leaf = role_leaf.get_object(["source"])
            src = Spinner(text=self.source_leaf.value, values=["joystick", "mouse"], size_hint_x=0.2)
            src.bind(text=self._on_source_change)
            self.add_widget(src)

        # Current axis label
        self.axis_leaf = role_leaf.get_object(["axis"]) if role_leaf.has_key(["axis"]) else None
        self.axis_label = Label(text=f"axis: {self.axis_leaf.value if self.axis_leaf else '?'}",
                                size_hint_x=0.2)
        self.add_widget(self.axis_label)

        # Detect button
        detect_btn = Button(text="wiggle to detect", size_hint_x=0.3, height=40, size_hint_y=None)
        detect_btn.bind(on_press=lambda _: self._start_detect())
        self.add_widget(detect_btn)

        # Inverse toggle
        if role_leaf.has_key(["inverse"]):
            self.inverse_leaf = role_leaf.get_object(["inverse"])
            inv = BoolLeafGui(parent=self, leaf=self.inverse_leaf, title="inverse")
            inv.size_hint_x = 0.15
            inv.height = 40

    def _on_source_change(self, instance, text):
        if self.source_leaf:
            self.source_leaf.set(text)

    def _start_detect(self):
        if self._detecting:
            return
        self._detecting = True
        self._deflection = {}
        for (stickid, axisid), slider in self.explorer.live_sliders.items():
            v = slider.slider.value
            self._deflection[(stickid, axisid)] = [v, v]
        from kivy.clock import Clock
        Clock.schedule_once(self._finish_detect, self.DETECT_WINDOW)

    def _finish_detect(self, dt):
        self._detecting = False
        if not self._deflection:
            return
        deflections = {k: (hi - lo) for k, (lo, hi) in self._deflection.items()}
        ranked = sorted(deflections.items(), key=lambda kv: kv[1], reverse=True)
        winner_key, winner_def = ranked[0]
        runner_up_def = ranked[1][1] if len(ranked) > 1 else 0.0
        if winner_def < self.WINNER_FLOOR:
            return
        if len(ranked) > 1 and runner_up_def > 0 and (winner_def / runner_up_def) < self.WINNER_RATIO:
            return
        self._assign(winner_key)

    def _assign(self, key):
        stickid, axisid = key
        if self.axis_leaf:
            self.axis_leaf.set(axisid)
            self.axis_label.text = f"axis: {axisid}"
        if self.role_leaf.has_key(["joystick"]):
            self.role_leaf.get_object(["joystick"]).set(stickid)
        self.explorer._update_selected()
        print(f"[{self.role}] detect assigned axis {stickid}/{axisid}")


class HatAxisRow(BoxLayout):
    """One compact row per analogue hatswitch: hat index, assigned axis,
    margin, and the threshold values (the engine's analogue-hatswitch:
    an axis with threshold bands that act as buttons).
    """
    def __init__(self, parent: BoxLayout, hat: str, hat_leaf: gc.ConfigBranch,
                 explorer: AxisExplorer, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=50, **kwargs)
        parent.add_widget(self)

        self.hat = hat
        self.hat_leaf = hat_leaf
        self.explorer = explorer

        self.add_widget(Label(text=f"Hat {hat}", size_hint_x=0.15, halign='left', bold=True))

        # Joystick number (text entry; defaults to 0)
        self.joy_leaf = hat_leaf.get_object(["joystick"]) if hat_leaf.has_key(["joystick"]) else None
        joy = TextInput(text=str(self.joy_leaf.value) if self.joy_leaf else "0",
                        size_hint_x=0.1, multiline=False)
        joy.bind(text=self._on_joy_change)
        self.add_widget(joy)

        # Assigned axis label + pick from explorer
        self.axis_leaf = hat_leaf.get_object(["axis"]) if hat_leaf.has_key(["axis"]) else None
        self.axis_label = Label(text=f"axis: {self.axis_leaf.value if self.axis_leaf else '?'}",
                                size_hint_x=0.15)
        self.add_widget(self.axis_label)
        pick_btn = Button(text="pick from explorer", size_hint_x=0.2, height=40, size_hint_y=None)
        pick_btn.bind(on_press=lambda _: self._start_pick())
        self.add_widget(pick_btn)

        # Margin
        self.margin_leaf = hat_leaf.get_object(["margin"]) if hat_leaf.has_key(["margin"]) else None
        if self.margin_leaf:
            margin = TextInput(text=str(self.margin_leaf.value), size_hint_x=0.1, multiline=False)
            margin.bind(text=self._on_margin_change)
            self.add_widget(margin)

        # Threshold values (comma-separated)
        self.values_leaf = hat_leaf.get_object(["values"]) if hat_leaf.has_key(["values"]) else None
        if self.values_leaf:
            values = TextInput(text=", ".join(str(v) for v in self.values_leaf.value),
                               size_hint_x=0.3, multiline=False)
            values.bind(text=self._on_values_change)
            self.add_widget(values)

        # Explorer pick mode: next pick assigns this hat's axis
        self._picking = False

    def _on_joy_change(self, instance, text):
        if self.joy_leaf:
            try:
                self.joy_leaf.set(int(text))
            except ValueError:
                pass

    def _on_margin_change(self, instance, text):
        if self.margin_leaf:
            try:
                self.margin_leaf.set(float(text))
            except ValueError:
                pass

    def _on_values_change(self, instance, text):
        if self.values_leaf:
            try:
                values = [float(v.strip()) for v in text.split(',') if v.strip()]
                self.values_leaf.set(values)
            except ValueError:
                pass

    def _start_pick(self):
        self._picking = not self._picking
        self.explorer.set_pick_target(self if self._picking else None)
        print(f"Hat {self.hat}: pick mode {'ON' if self._picking else 'OFF'}")

    def accept_pick(self, stickid, axisid):
        if self.axis_leaf:
            self.axis_leaf.set(axisid)
            self.axis_label.text = f"axis: {axisid}"
        if self.joy_leaf:
            self.joy_leaf.set(stickid)
        self._picking = False
        self.explorer._update_selected()


# Test Code
if __name__ == "__main__":
    pass
    