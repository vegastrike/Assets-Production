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


def _load_sdl():
    """Load the system SDL2 library and set up the joystick ctypes signatures.

    Also ensures the SDL joystick subsystem is initialized (SDL_INIT_JOYSTICK,
    0x200, which implies SDL_INIT_EVENTS) - Kivy's window provider does NOT
    initialize the joystick subsystem, so without this SDL_NumJoysticks always
    returns 0 and no axes can be enumerated. Shared by the joystick
    enumeration and hat-polling paths. Returns the ctypes handle, or None if
    SDL2 can't be loaded.
    """
    import ctypes
    import ctypes.util
    try:
        sdl = ctypes.CDLL(ctypes.util.find_library("SDL2") or "libSDL2-2.0.so.0")
    except (OSError, AttributeError):
        return None
    sdl.SDL_Init.argtypes = [ctypes.c_uint]
    sdl.SDL_Init.restype = ctypes.c_int
    sdl.SDL_Init(0x200)   # SDL_INIT_JOYSTICK (implies SDL_INIT_EVENTS)
    sdl.SDL_NumJoysticks.restype = ctypes.c_int
    sdl.SDL_JoystickOpen.argtypes = [ctypes.c_int]
    sdl.SDL_JoystickOpen.restype = ctypes.c_void_p
    sdl.SDL_JoystickGetHat.argtypes = [ctypes.c_void_p, ctypes.c_int]
    sdl.SDL_JoystickGetHat.restype = ctypes.c_uint8
    sdl.SDL_JoystickNumHats.argtypes = [ctypes.c_void_p]
    sdl.SDL_JoystickNumHats.restype = ctypes.c_int
    sdl.SDL_JoystickNumAxes.argtypes = [ctypes.c_void_p]
    sdl.SDL_JoystickNumAxes.restype = ctypes.c_int
    return sdl


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

        # Kivy's on_joy_hat event is unreliable (the SDL2 provider often
        # drops SDL_JOYHATMOTION), so also poll SDL_JoystickGetHat directly.
        from kivy.clock import Clock
        self._hat_poll = Clock.schedule_interval(self._poll_hats, 1 / 20)
        self._hat_state = {}
        self._hat_poll_active = True

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

    def _poll_hats(self, dt):
        """Poll SDL_JoystickGetHat for every joystick/hat and detect state
        changes (the reliable way to catch D-pad presses; Kivy's on_joy_hat
        event is often not delivered).
        """
        sdl = _load_sdl()
        if sdl is None:
            return
        n = sdl.SDL_NumJoysticks()
        for i in range(n):
            joy = sdl.SDL_JoystickOpen(i)
            if not joy:
                continue
            nhats = sdl.SDL_JoystickNumHats(joy)
            for h in range(nhats):
                v = sdl.SDL_JoystickGetHat(joy, h)
                key = (i, h)
                if key in self._hat_state and self._hat_state[key] != v:
                    # Convert the SDL bitmask to the (vx, vy) tuple the
                    # Kivy event path uses (matching _window_sdl2.pyx).
                    vx = vy = 0
                    if v & 1:   # SDL_HAT_UP
                        vy = 1
                    elif v & 4:  # SDL_HAT_DOWN
                        vy = -1
                    if v & 2:   # SDL_HAT_RIGHT
                        vx = 1
                    elif v & 8:  # SDL_HAT_LEFT
                        vx = -1
                    self._on_hat_value(i, h, (vx, vy))
                self._hat_state[key] = v

    def _on_hat_value(self, stickid, hatid, value):
        # Kivy converts the SDL hat bitmask to a (vx, vy) tuple
        # (_window_sdl2.pyx:691-703): UP=(0,1) DOWN=(0,-1) RIGHT=(1,0)
        # LEFT=(-1,0), diagonals are sums, CENTER=(0,0).
        if not isinstance(value, tuple) or len(value) != 2:
            return
        vx, vy = value
        name = None
        if vx == 0 and vy == 0:
            name = 'center'
        elif vx == 0 and vy == 1:
            name = 'up'
        elif vx == 0 and vy == -1:
            name = 'down'
        elif vx == 1 and vy == 0:
            name = 'right'
        elif vx == -1 and vy == 0:
            name = 'left'
        elif vx == 1 and vy == 1:
            name = 'rightup'
        elif vx == 1 and vy == -1:
            name = 'rightdown'
        elif vx == -1 and vy == 1:
            name = 'leftup'
        elif vx == -1 and vy == -1:
            name = 'leftdown'
        if name is None or name == 'center':
            return  # ignore release to center
        self._set_binding({'joystick': stickid, 'hatswitch': hatid, 'direction': name})

    def _on_joy_hat(self, window, stickid, hatid, value):
        # Kivy event path (may not fire); same decoding as the poll.
        self._on_hat_value(stickid, hatid, value)

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
        if getattr(self, '_hat_poll', None):
            self._hat_poll.cancel()


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
    """A live-updating slider for one physical joystick axis, with a bind
    dropdown (none/x/y/z/throttle) and an Invert checkbox (per-role).
    """
    ROLES = ["none", "x", "y", "z", "throttle"]

    def __init__(self, stickid: int, axisid: int, label_text: str = None,
                 on_bind=None, on_invert=None, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=40, **kwargs)
        self.stickid = stickid
        self.axisid = axisid
        self.on_bind = on_bind
        self.on_invert = on_invert
        self._updating = False

        label_text = label_text or f"A{axisid}"
        self.label = Label(text=label_text, size_hint_x=0.16, halign='left',
                           font_size='12sp')
        self.add_widget(self.label)

        self.slider = Slider(min=-1, max=1, value=0, size_hint_x=0.46)
        self.slider.disabled = True   # display-only; not user-draggable
        self.add_widget(self.slider)

        self.bind_spinner = Spinner(values=self.ROLES, size_hint_x=0.24,
                                    text="none", font_size='12sp')
        self.bind_spinner.bind(text=self._on_bind)
        self.add_widget(self.bind_spinner)

        self.invert_cb = CheckBox(active=False, size_hint_x=0.14)
        self.invert_cb.bind(active=self._on_invert)
        self.add_widget(self.invert_cb)
        self.invert_label = Label(text="Inv", size_hint_x=None, width=28,
                                  font_size='10sp')
        self.add_widget(self.invert_label)

        # Live update from Kivy's SDL2 joystick provider
        from kivy.core.window import Window
        Window.bind(on_joy_axis=self.on_joy_axis)

    def on_joy_axis(self, window, stickid, axisid, value):
        if stickid == self.stickid and axisid == self.axisid:
            # SDL axis values are raw 16-bit (-32768..32767); normalize to -1..1
            self.slider.value = value / 32767.0

    def _on_bind(self, instance, text):
        if self._updating or self.on_bind is None:
            return
        self.on_bind(self.stickid, self.axisid, text)

    def _on_invert(self, instance, active):
        if self._updating or self.on_invert is None:
            return
        self.on_invert(self.stickid, self.axisid, bool(active))

    def set_bound_role(self, role):
        """Set the dropdown text without re-firing the bind handler."""
        self._updating = True
        self.bind_spinner.text = role if role else "none"
        self._updating = False

    def set_inverted(self, inverted):
        """Set the checkbox state without re-firing the invert handler."""
        self._updating = True
        self.invert_cb.active = bool(inverted)
        self._updating = False


class AxisExplorer(BoxLayout):
    """One shared live display of every joystick axis observed via on_joy_axis.

    Each slider carries its own bind dropdown (none/x/y/z/throttle), so there
    are no separate role rows - the whole block stays compact.
    """
    def __init__(self, parent: BoxLayout, roles: dict, **kwargs):
        # roles: {role_name: role_leaf}
        super().__init__(orientation='vertical', size_hint_y=None, height=300, **kwargs)
        parent.add_widget(self)

        self.roles = roles
        self.live_sliders = {}      # (stickid, axisid) -> LiveAxisSlider
        # Start as if a joystick were present so the first no-joystick poll
        # actually hides the (initially visible) sliders.
        self._have_joystick = True

        # "No joystick detected" placeholder, shown until a device appears.
        # Hidden initially (sliders are the default state when present).
        self.no_joy_label = Label(text="No Joystick Detected", halign='center',
                                  size_hint=(1, None), height=40, opacity=0.0)
        self.add_widget(self.no_joy_label)

        # Live sliders area
        self.sliders_area = BoxLayout(orientation='vertical', size_hint_y=None)
        self.sliders_area.bind(minimum_height=self.sliders_area.setter('height'))
        self.add_widget(self.sliders_area)

        from kivy.core.window import Window
        Window.bind(on_joy_axis=self._watch_axes)

        # Poll every second: pick up a joystick whenever one appears (and
        # show the placeholder while none is connected).
        from kivy.clock import Clock
        self._enumerate_joysticks()
        Clock.schedule_interval(lambda dt: self._enumerate_joysticks(), 1.0)

    def _set_joystick_visible(self, present):
        """Show either the 'No Joystick Detected' placeholder or the sliders."""
        if present == self._have_joystick:
            return
        self._have_joystick = present
        self.no_joy_label.opacity = 0.0 if present else 1.0
        self.sliders_area.opacity = 1.0 if present else 0.0

    def _enumerate_joysticks(self):
        """Create a slider for every axis of every connected joystick right away.

        Kivy only creates on_joy_axis sliders after the user moves the stick,
        so without this the axis list is empty at startup. Uses the shared
        _load_sdl() helper (same SDL2 ctypes approach as _poll_hats). Polls
        every second so a late-plugged joystick is picked up.
        """
        sdl = _load_sdl()
        if sdl is None:
            self._set_joystick_visible(False)
            return
        n = sdl.SDL_NumJoysticks()
        found_any = False
        for i in range(n):
            joy = sdl.SDL_JoystickOpen(i)
            if not joy:
                continue
            found_any = True
            naxes = sdl.SDL_JoystickNumAxes(joy)
            for a in range(naxes):
                key = (i, a)
                if key not in self.live_sliders:
                    slider = LiveAxisSlider(stickid=i, axisid=a,
                                            label_text=f"Joy{i} A{a}",
                                            on_bind=self._on_bind_axis,
                                            on_invert=self._on_invert_axis)
                    self.live_sliders[key] = slider
                    self.sliders_area.add_widget(slider)
        self._set_joystick_visible(found_any)
        if found_any:
            self._refresh_slider_binds()

    def _watch_axes(self, window, stickid, axisid, value):
        key = (stickid, axisid)
        if key not in self.live_sliders:
            slider = LiveAxisSlider(stickid=stickid, axisid=axisid,
                                    label_text=f"Joy{stickid} A{axisid}",
                                    on_bind=self._on_bind_axis,
                                    on_invert=self._on_invert_axis)
            self.live_sliders[key] = slider
            self.sliders_area.add_widget(slider)
        self._set_joystick_visible(True)
        self._refresh_slider_binds()

    def _role_for(self, stickid, axisid):
        """Return the role name bound to this physical axis, or None."""
        for role, role_leaf in self.roles.items():
            if not role_leaf.has_key(["axis"]):
                continue
            if role_leaf.get_object(["axis"]).value != axisid:
                continue
            joy = 0
            if role_leaf.has_key(["joystick"]):
                joy = role_leaf.get_object(["joystick"]).value
            if joy == stickid:
                return role
        return None

    def _on_bind_axis(self, stickid, axisid, role):
        """Bind (or unbind) a physical axis to a flight role."""
        if role == "none":
            # clear whichever role currently points here
            for r, role_leaf in self.roles.items():
                if not role_leaf.has_key(["axis"]):
                    continue
                if role_leaf.get_object(["axis"]).value == axisid:
                    role_leaf.get_object(["axis"]).set(-1)
            print(f"Unbound Joy{stickid} A{axisid}")
        else:
            role_leaf = self.roles.get(role)
            if role_leaf is None or not role_leaf.has_key(["axis"]):
                return
            # this role can only point at one axis; clear its old binding
            old = self._role_for(stickid, axisid)
            if old is not None and old != role:
                self.roles[old].get_object(["axis"]).set(-1)
            role_leaf.get_object(["axis"]).set(axisid)
            if role_leaf.has_key(["joystick"]):
                role_leaf.get_object(["joystick"]).set(stickid)
            print(f"Bound Joy{stickid} A{axisid} to '{role}'")
        self._refresh_slider_binds()

    def _refresh_slider_binds(self):
        """Sync each slider's dropdown and invert checkbox to the role bound
        to it (invert is per-role: axes.<role>.inverse)."""
        for key, slider in self.live_sliders.items():
            role = self._role_for(*key)
            slider.set_bound_role(role)
            inverted = False
            if role is not None and role in self.roles:
                role_leaf = self.roles[role]
                if role_leaf.has_key(["inverse"]):
                    inverted = bool(role_leaf.get_object(["inverse"]).value)
            slider.set_inverted(inverted)

    def _on_invert_axis(self, stickid, axisid, inverted):
        """Set axes.<role>.inverse for the role bound to this axis."""
        role = self._role_for(stickid, axisid)
        if role is None or role not in self.roles:
            print(f"No role bound to Joy{stickid} A{axisid}; invert ignored")
            return
        role_leaf = self.roles[role]
        if role_leaf.has_key(["inverse"]):
            role_leaf.get_object(["inverse"]).set(inverted)
            print(f"[{role}] inverse -> {inverted}")
        self._refresh_slider_binds()

    def max_deflection(self):
        """Largest |current value| across the live sliders of BOUND axes only,
        excluding the throttle role.

        An axis is bound when some role in the config maps to it (axis != -1).
        The throttle axis is ignored too - it is a stay-where-you-put-it axis,
        not a centered stick axis, so its resting value must not feed the
        deadband calculation.
        """
        bound = set()
        for role, role_leaf in self.roles.items():
            if role == "throttle":
                continue
            if not role_leaf.has_key(["axis"]):
                continue
            axis = role_leaf.get_object(["axis"]).value
            if axis is None or axis == -1:
                continue
            joy = 0
            if role_leaf.has_key(["joystick"]):
                joy = role_leaf.get_object(["joystick"]).value
            bound.add((joy, axis))
        m = 0.0
        for key, slider in self.live_sliders.items():
            if key in bound:
                m = max(m, abs(slider.slider.value))
        return m


# Test Code
if __name__ == "__main__":
    pass
    