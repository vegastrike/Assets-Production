from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

import game_config as gc
from graphics_factory.label_control_pair import CaptureBindingButton
from graphics_factory.divider import DividerLine

# Device types (display name -> config key)
DEVICE_CHOICES = [('Key', 'keyboard'), ('Mouse', 'mouse'), ('Joy', 'joystick')]


class DeviceToggleButton(Button):
    """A button that cycles Key -> Mouse -> Joy when clicked."""
    def __init__(self, on_change=None, **kwargs):
        super().__init__(**kwargs)
        self.on_change = on_change
        self.index = 0
        self.text = DEVICE_CHOICES[self.index][0]
        self.bind(on_press=lambda _: self.cycle())

    def cycle(self):
        self.index = (self.index + 1) % len(DEVICE_CHOICES)
        self.text = DEVICE_CHOICES[self.index][0]
        if self.on_change:
            self.on_change(self.device_name())

    def device_name(self):
        return DEVICE_CHOICES[self.index][1]


class BindingRow(BoxLayout):
    """One row: action name + device toggle + mapping field + Add + Delete."""

    def __init__(self, parent: BoxLayout, action_key: str, device: str, binding: dict,
                 on_capture, on_add, on_delete, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=45, **kwargs)
        parent.add_widget(self)

        self.action_key = action_key
        self.device = device
        self.binding = binding

        # Action name
        self.add_widget(Label(text=action_key, size_hint_x=0.25, halign='left', valign='middle'))

        # Device toggle (Key/Mouse/Joy)
        self.toggle = DeviceToggleButton(size_hint_x=0.12, height=40, size_hint_y=None,
                                         on_change=self._on_device_change)
        names = [n for n, _ in DEVICE_CHOICES]
        self.toggle.index = names.index(self._display_name(device)) if device in self._display_names() else 0
        self.toggle.text = DEVICE_CHOICES[self.toggle.index][0]
        self.add_widget(self.toggle)

        # Mapping field: click to capture
        self.capture = CaptureBindingButton(
            parent=self, binding=binding, device=device,
            on_capture=on_capture
        )

        # Add and Delete on the same row
        add_btn = Button(text="+", size_hint_x=0.08, height=40, size_hint_y=None)
        add_btn.bind(on_press=lambda _: on_add(self))
        self.add_widget(add_btn)
        del_btn = Button(text="x", size_hint_x=0.08, height=40, size_hint_y=None)
        del_btn.bind(on_press=lambda _: on_delete(self))
        self.add_widget(del_btn)

    @staticmethod
    def _display_names():
        return {d for _, d in DEVICE_CHOICES}

    def _display_name(self, device):
        for disp, d in DEVICE_CHOICES:
            if d == device:
                return disp
        return 'Key'

    def _on_device_change(self, new_device):
        self.device = new_device
        self.capture.device = new_device
        self.capture.binding = {}
        self.capture.button.text = self.capture.format_binding()
        if hasattr(self, 'on_changed'):
            self.on_changed()


class ActionBindingsGroup(BoxLayout):
    """One action: a list of rows, each with name/toggle/binding/add/delete."""

    def __init__(self, parent: BoxLayout, action_key: str, action_branch: gc.ConfigBranch, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, **kwargs)
        parent.add_widget(self)

        self.action_key = action_key
        self.action_branch = action_branch
        self.rows = []          # BindingRow widgets

        # Load existing bindings (flattened across devices, preserving order)
        for device, _ in DEVICE_CHOICES:
            if self.action_branch.has_key([device]):
                leaf = self.action_branch.get_object([device])
                for binding in leaf.value:
                    self._add_row(device, binding)
        # If no bindings at all, start with one blank row
        if not self.rows:
            self._add_row('keyboard', {})

    def _device_leaf(self, device):
        if self.action_branch.has_key([device]):
            return self.action_branch.get_object([device])
        return None

    def _add_row(self, device, binding):
        holder = {}
        row = BindingRow(
            parent=self, action_key=self.action_key, device=device, binding=binding,
            on_capture=lambda new_binding, d=device, h=holder: self._on_capture(d, h['row'], new_binding),
            on_add=lambda r: self._on_add(r),
            on_delete=lambda r: self._on_delete(r)
        )
        holder['row'] = row
        row.on_changed = lambda r=row: self._on_changed(r)
        self.rows.append(row)

    def _on_changed(self, row):
        self._write_all()

    def _on_add(self, row):
        # Add a new blank row at the bottom (simplest; reordering is fiddly)
        self._add_row('keyboard', {})

    def _on_delete(self, row):
        if row in self.rows:
            self.rows.remove(row)
            self.remove_widget(row)
        # Keep at least one blank row
        if not self.rows:
            self._add_row('keyboard', {})
        self._write_all()

    def _on_capture(self, device, row, new_binding):
        row.binding = new_binding
        self._write_all()

    def _write_all(self):
        # Rebuild per-device arrays from the current rows and write each leaf
        by_device = {d: [] for _, d in DEVICE_CHOICES}
        for row in self.rows:
            if row.binding:
                by_device[row.device].append(row.binding)
        for device, _ in DEVICE_CHOICES:
            leaf = self._device_leaf(device)
            if leaf is not None:
                leaf.set(by_device[device])


class BindingsTab(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.padding = 10

        self.tab_name = "Actions"

        # Title
        title_label = Label(text="Actions (bindings)".upper(), font_size=24, size_hint=(0.8, None), height=80,
                            halign='center')
        self.add_widget(title_label)

        # Divider
        self.add_widget(DividerLine())

        actions = gc.game_config.get_object(["actions"])
        if actions is None:
            self.add_widget(Label(text="No 'actions' section found in config.json", height=50, size_hint_y=None))
            return

        # Scrollable configuration area
        scroll_view = ScrollView(size_hint=(1, 0.8))
        config_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        config_layout.bind(minimum_height=config_layout.setter('height'))
        scroll_view.add_widget(config_layout)
        self.add_widget(scroll_view)

        for action_key in sorted(actions.value.keys()):
            action_branch = actions.get_object([action_key])
            ActionBindingsGroup(parent=config_layout, action_key=action_key, action_branch=action_branch)
