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
    """One row = one binding: device toggle + mapping field (click to capture)."""

    def __init__(self, parent: BoxLayout, device: str, binding: dict,
                 on_capture, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=45, **kwargs)
        parent.add_widget(self)

        self.device = device
        self.binding = binding

        # Device toggle (Key/Mouse/Joy). Set to the current device's index.
        self.toggle = DeviceToggleButton(size_hint_x=0.15, height=40, size_hint_y=None,
                                         on_change=self._on_device_change)
        names = [n for n, _ in DEVICE_CHOICES]
        self.toggle.index = names.index(self._display_name(device)) if device in self._display_names() else 0
        self.toggle.text = DEVICE_CHOICES[self.toggle.index][0]
        self.add_widget(self.toggle)

        # The mapping field: click to capture for the current device.
        self.capture = CaptureBindingButton(
            parent=self, binding=binding, device=device,
            on_capture=on_capture
        )

    @staticmethod
    def _display_names():
        return {d for _, d in DEVICE_CHOICES}

    def _display_name(self, device):
        for disp, d in DEVICE_CHOICES:
            if d == device:
                return disp
        return 'Key'

    def _on_device_change(self, new_device):
        # Change which device this row binds to. The binding dict shape needs
        # to switch to the new device's format (empty until captured).
        self.device = new_device
        self.capture.device = new_device
        self.capture.binding = {}
        self.capture.button.text = self.capture.format_binding()
        # Let the parent know the device changed so it can write back.
        if hasattr(self, 'on_device_changed'):
            self.on_device_changed()


class ActionBindingsGroup(BoxLayout):
    """One action: header (name + add + delete) + a row per binding."""

    def __init__(self, parent: BoxLayout, action_key: str, action_branch: gc.ConfigBranch, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, **kwargs)
        parent.add_widget(self)

        self.action_key = action_key
        self.action_branch = action_branch
        self.rows = []          # BindingRow widgets

        # Header row: action name + add + delete, all on one line
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=45)
        self.add_widget(header)
        title = Label(text=action_key, valign='middle', halign='left', bold=True, size_hint_x=0.5)
        title.bind(size=lambda inst, sz: setattr(inst, 'text_size', sz))
        header.add_widget(title)
        add_btn = Button(text="+ add", size_hint_x=0.15, height=40, size_hint_y=None)
        add_btn.bind(on_press=lambda _: self._add_binding())
        header.add_widget(add_btn)
        del_btn = Button(text="x", size_hint_x=0.1, height=40, size_hint_y=None)
        del_btn.bind(on_press=lambda _: self._delete_last())
        header.add_widget(del_btn)

        self.rows_area = BoxLayout(orientation='vertical', size_hint_y=None)
        self.rows_area.bind(minimum_height=self.rows_area.setter('height'))
        self.add_widget(self.rows_area)

        # Load existing bindings (flattened across devices, preserving order)
        for device, _ in DEVICE_CHOICES:
            if self.action_branch.has_key([device]):
                leaf = self.action_branch.get_object([device])
                for binding in leaf.value:
                    self._add_row(device, binding)
        # If no bindings at all, start with one blank row
        if not self.rows:
            self._add_binding()

    def _device_leaf(self, device):
        if self.action_branch.has_key([device]):
            return self.action_branch.get_object([device])
        return None

    def _add_row(self, device, binding):
        row = BindingRow(
            parent=self.rows_area, device=device, binding=binding,
            on_capture=lambda new_binding, d=device, r=None: self._on_capture(d, r, new_binding)
        )
        row.on_capture = lambda new_binding, d=device, r=row: self._on_capture(d, r, new_binding)
        row.on_device_changed = lambda r=row: self._on_device_changed(r)
        self.rows.append(row)

    def _on_device_changed(self, row):
        # Device toggle switched; write back the (now empty) binding
        self._write_all()

    def _add_binding(self):
        # Add a blank row on keyboard by default; user toggles the device.
        self._add_row('keyboard', {})

    def _delete_last(self):
        # Delete the last binding row; keep at least one blank row visible.
        if self.rows:
            row = self.rows.pop()
            self.rows_area.remove_widget(row)
        if not self.rows:
            self._add_binding()
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
