from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

import game_config as gc
from graphics_factory.label_control_pair import CaptureBindingButton
from graphics_factory.divider import DividerLine

# Device types (display name -> config key)
DEVICE_CHOICES = [('Key', 'keyboard'), ('Mouse', 'mouse'), ('Joy', 'joystick')]


class BindingRow(BoxLayout):
    """One row: action name + device type (from config) + binding field
    (click to capture, auto-detects device) + Add + Delete."""

    def __init__(self, parent: BoxLayout, action_key: str, device: str, binding: dict,
                 on_capture, on_add, on_delete, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=70, **kwargs)
        parent.add_widget(self)

        self.action_key = action_key
        self.device = device
        self.binding = binding

        # Action name (wide, bold)
        self.add_widget(Label(text=action_key, size_hint_x=0.50, halign='left', valign='middle', bold=True))

        # Device type label (from config binding, or '?' if blank)
        self.device_label = Label(
            text=self._display_name(device), size_hint_x=0.10, halign='center', valign='middle'
        )
        self.add_widget(self.device_label)

        # Mapping field: click to capture (auto-detects device)
        self.capture = CaptureBindingButton(
            parent=self, binding=binding, device=device,
            on_capture=on_capture
        )
        self.capture.size_hint_x = 0.35

        # Add and Delete on the same row
        add_btn = Button(text="+", size_hint_x=0.08, height=35, size_hint_y=None, pos_hint={'center_y': 0.5})
        add_btn.bind(on_press=lambda _: on_add(self))
        self.add_widget(add_btn)
        del_btn = Button(text="x", size_hint_x=0.08, height=35, size_hint_y=None, pos_hint={'center_y': 0.5})
        del_btn.bind(on_press=lambda _: on_delete(self))
        self.add_widget(del_btn)

    @staticmethod
    def _display_name(device):
        for disp, d in DEVICE_CHOICES:
            if d == device:
                return disp
        return '?'

    def refresh(self):
        # Update device label + capture display after a capture/device change
        self.device_label.text = self._display_name(self.device)
        self.capture.device = self.device
        self.capture.button.text = self.capture.format_binding()
        if hasattr(self, 'on_changed'):
            self.on_changed()


class ActionBindingsGroup(BoxLayout):
    """One action: a list of rows, each with name/toggle/binding/add/delete."""

    def __init__(self, parent: BoxLayout, action_key: str, action_branch: gc.ConfigBranch, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, **kwargs)
        self.bind(minimum_height=self.setter('height'))
        parent.add_widget(self)

        self.action_key = action_key
        self.action_branch = action_branch
        self.rows = []          # BindingRow widgets

        # Load existing bindings (flattened across devices, preserving order)
        for _, device in DEVICE_CHOICES:
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
            on_capture=lambda new_device, new_binding, d=device, h=holder:
                self._on_capture(d, h['row'], new_device, new_binding),
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

    def _on_capture(self, old_device, row, new_device, new_binding):
        # The captured binding may be a different device than the row started
        # with; update the row to the detected device.
        row.device = new_device
        row.binding = new_binding
        row.refresh()
        self._write_all()

    def _write_all(self):
        # Rebuild per-device arrays from the current rows and write each leaf
        by_device = {d: [] for _, d in DEVICE_CHOICES}
        for row in self.rows:
            if row.binding:
                by_device[row.device].append(row.binding)
        for _, device in DEVICE_CHOICES:
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
