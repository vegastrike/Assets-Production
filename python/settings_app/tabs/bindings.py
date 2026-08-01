from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

import game_config as gc
from graphics_factory.label_control_pair import CaptureBindingButton
from graphics_factory.divider import DividerLine

# The per-device binding arrays in the actions section
DEVICES = ['keyboard', 'mouse', 'joystick', 'hat']


class BindingRow(BoxLayout):
    """One row = one binding (device + capture button + wipe button)."""

    def __init__(self, parent: BoxLayout, device: str, binding: dict,
                 on_capture, on_wipe, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=45, **kwargs)
        parent.add_widget(self)

        self.device = device
        self.binding = binding

        self.add_widget(Label(text=device, size_hint_x=0.2, halign='left'))

        CaptureBindingButton(
            parent=self, binding=binding, device=device,
            on_capture=on_capture
        )

        wipe_btn = Button(text="x", size_hint_x=0.1, height=40, size_hint_y=None)
        wipe_btn.bind(on_press=lambda _: on_wipe(self))
        self.add_widget(wipe_btn)


class ActionGroup(BoxLayout):
    """One action: header (name + add) + a row per binding."""

    def __init__(self, parent: BoxLayout, action_key: str, action_branch: gc.ConfigBranch, **kwargs):
        super().__init__(orientation='vertical', size_hint_y=None, **kwargs)
        parent.add_widget(self)

        self.action_key = action_key
        self.action_branch = action_branch
        self.rows = []          # BindingRow widgets

        # Header: action name + add button
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        self.add_widget(header)
        title = Label(text=action_key, valign='middle', halign='left', bold=True)
        title.bind(size=lambda inst, sz: setattr(inst, 'text_size', sz))
        header.add_widget(title)
        add_btn = Button(text="+ add binding", size_hint_x=0.25, height=35, size_hint_y=None)
        add_btn.bind(on_press=lambda _: self._add_binding())
        header.add_widget(add_btn)

        self.rows_area = BoxLayout(orientation='vertical', size_hint_y=None)
        self.rows_area.bind(minimum_height=self.rows_area.setter('height'))
        self.add_widget(self.rows_area)

        # Load existing bindings (flattened across devices, preserving order)
        for device in DEVICES:
            if self.action_branch.has_key([device]):
                leaf = self.action_branch.get_object([device])
                for binding in leaf.value:
                    self._add_row(device, binding)

    def _device_leaf(self, device):
        if self.action_branch.has_key([device]):
            return self.action_branch.get_object([device])
        return None

    def _add_row(self, device, binding):
        row = BindingRow(
            parent=self.rows_area, device=device, binding=binding,
            on_capture=lambda new_binding, d=device, r=None: self._on_capture(d, r, new_binding),
            on_wipe=lambda r: self._on_wipe(r)
        )
        # r defaults to None; fix it to this row after creation
        row.on_capture = lambda new_binding, d=device, r=row: self._on_capture(d, r, new_binding)
        self.rows.append(row)

    def _add_binding(self):
        # Add a blank row on the first device that has a leaf; it captures
        # immediately (placeholder only written once captured).
        for device in DEVICES:
            leaf = self._device_leaf(device)
            if leaf is not None:
                self._add_row(device, {})
                return
        # No device leaves exist; nothing to bind to (shouldn't happen)

    def _on_capture(self, device, row, new_binding):
        row.binding = new_binding
        self._write_all()

    def _on_wipe(self, row):
        if row in self.rows:
            self.rows.remove(row)
            self.rows_area.remove_widget(row)
        # If this was the last row, keep an empty row visible (clear, don't delete)
        if not self.rows:
            self._add_binding()
        self._write_all()

    def _write_all(self):
        # Rebuild per-device arrays from the current rows and write each leaf
        by_device = {d: [] for d in DEVICES}
        for row in self.rows:
            if row.binding:
                by_device[row.device].append(row.binding)
        for device in DEVICES:
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
            ActionGroup(parent=config_layout, action_key=action_key, action_branch=action_branch)
