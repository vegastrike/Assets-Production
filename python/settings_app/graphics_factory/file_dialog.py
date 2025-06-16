from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView

class FileChooserPopup(BoxLayout):
    def __init__(self, on_selection, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        self.on_selection = on_selection
        self.parent_popup = None
        
        button_row = BoxLayout(orientation='horizontal', size_hint=(1, 0.1), spacing=10)
        open_btn = Button(text="Open", size_hint=(0.5, 0.1))
        cancel_btn = Button(text="Cancel", size_hint=(0.5, 0.1))
        button_row.add_widget(open_btn)
        button_row.add_widget(cancel_btn)

        open_btn.bind(on_press=self.on_select)
        cancel_btn.bind(on_press=self.on_cancel)

        self.add_widget(button_row)
        
        self.file_chooser = FileChooserListView(size_hint=(1, 0.9), dirselect=True, path=None)
        self.add_widget(self.file_chooser)

        

    def on_select(self, instance):
        if self.on_selection and len(self.file_chooser.selection) > 0:
            selected_folder = self.file_chooser.selection[0]
            print(f"on_select: {selected_folder}")
            self.on_selection(selected_folder)
        print("Select")
        self.parent_popup.dismiss()

    def on_cancel(self, *args):
        print("Cancel")
        self.parent_popup.dismiss()