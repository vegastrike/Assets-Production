from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

import game_config as gc
from graphics_factory.label_control_pair import CaptureBindingButton
from graphics_factory.divider import DividerLine

# The per-device binding arrays in the actions section
DEVICES = ['keyboard', 'mouse', 'joystick', 'hat']


class ActionRow(BoxLayout):
    """One row for one action: title + per-device binding columns."""

    def __init__(self, parent: BoxLayout, action_key: str, action_branch: gc.ConfigBranch, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=120, **kwargs)
        parent.add_widget(self)

        self.action_key = action_key
        self.action_branch = action_branch
        self._leaf = {}
        self._bindings = {}

        # Title column
        title = Label(text=action_key, valign='middle', halign='left',
                      size_hint_x=0.25, text_size=(None, None))
        title.bind(size=lambda inst, sz: setattr(inst, 'text_size', sz))
        self.add_widget(title)

        # One column per device
        self.columns = {}
        for device in DEVICES:
            col = BoxLayout(orientation='vertical', size_hint_x=0.25)
            self.columns[device] = col
            self.add_widget(col)
            self._populate_column(device, col)

    def _populate_column(self, device: str, col: BoxLayout):
        # Get the per-device leaf (a ConfigLeaf whose .value is the array)
        leaf = self.action_branch.get_object([device]) if self.action_branch.has_key([device]) else None
        self._leaf[device] = leaf
        self._bindings[device] = list(leaf.value) if leaf else []

        header = Label(text=device.upper(), font_size=14, height=30, size_hint_y=None)
        col.add_widget(header)

        # Show ALL existing bindings (the engine supports multiple binds per
        # device per action, e.g. AccelKey = '+', 'keypad-plus', '=').
        for binding in self._bindings[device]:
            self._add_binding_button(device, col, binding)

        # Always allow adding another (multiple per device are valid).
        add_btn = Button(text="+ add", height=35, size_hint_y=None)
        add_btn.bind(on_press=lambda _: self._add_binding(device))
        col.add_widget(add_btn)

    def _add_binding_button(self, device, col, binding):
        # Replace-mode capture: click -> press new input -> callback replaces this entry
        CaptureBindingButton(
            parent=col, binding=binding, device=device,
            on_capture=lambda new_binding, d=device, old=binding: self._replace_binding(d, old, new_binding)
        )

    def _add_binding(self, device):
        # Add an empty entry that captures immediately; it is only written to
        # config once a real binding is captured (via _replace_binding).
        placeholder = {}
        self._bindings[device] = [placeholder]
        CaptureBindingButton(
            parent=self.columns[device], binding=placeholder, device=device,
            on_capture=lambda new_binding, d=device, old=placeholder: self._replace_binding(d, old, new_binding)
        )


    def _replace_binding(self, device, old_binding, new_binding):
        arr = self._bindings[device]
        for i, b in enumerate(arr):
            # Identity match (handles duplicate empty placeholders correctly)
            if b is old_binding or b == old_binding:
                arr[i] = new_binding
                break
        self._write_device(device)

    def _write_device(self, device):
        leaf = self._leaf.get(device)
        if leaf is None:
            return
        # Preserve all other entries; write the whole array (read-modify-write)
        leaf.set(list(self._bindings[device]))
        # Refresh the column display
        col = self.columns[device]
        col.clear_widgets()
        self._populate_column(device, col)


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
            ActionRow(parent=config_layout, action_key=action_key, action_branch=action_branch)
