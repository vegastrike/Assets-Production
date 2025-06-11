import json
import tkinter as tk

def get_tabs(config_json):
    return list(config_json.keys())

def get_labels(config_json, key):
    return list(config_json[key].keys())


def get_label_and_checkbutton(root_element, label_text, initial_value):
    frame_row = tk.Frame(root_element, bg="#2e2e2e")
    frame_row.pack(pady=10)

    label = tk.Label(frame_row, text=f"{label_text}:", fg="white", bg="#2e2e2e", font=("Arial", 12))
    label.pack(side="left", padx=5)

    toggle_var = tk.BooleanVar(value=initial_value)
    toggle_button = tk.Checkbutton(frame_row, variable=toggle_var, bg="#2e2e2e", activebackground="#2e2e2e", 
                                   fg="white", selectcolor="#444444", font=("Arial", 12))
    toggle_button.pack(side="left", padx=5)

    return toggle_var

def get_tab_data(root_element, tab_json, level=0):
    for key, value in tab_json.items():
        # Add a label and a control (e.g. checkbox) on the same line
        frame_row = tk.Frame(root_element, bg="#2e2e2e")
        frame_row.pack(pady=10)

        label = tk.Label(frame_row, text=f"{key}:", fg="white", bg="#2e2e2e", font=("Arial", 12))
        label.pack(side="left", padx=5)

        if isinstance(value, bool):
            toggle_var = tk.BooleanVar(value=value)
            toggle_button = tk.Checkbutton(frame_row, variable=toggle_var, bg="#2e2e2e", activebackground="#2e2e2e", 
                                        fg="white", selectcolor="#444444", font=("Arial", 12))
            toggle_button.pack(side="left", padx=5)

        if isinstance(value, str):
            text_field_var = tk.StringVar(value=value)
            text_field = tk.Entry(frame_row, textvariable=text_field_var, bg="#444444", fg="white", font=("Arial", 10), insertbackground="white")
            text_field.pack(side="left", padx=5, fill="x", expand=True)

        if isinstance(value, int):
            int_var = tk.IntVar(value=value)
            text_field = tk.Entry(frame_row, textvariable=int_var, bg="#444444", fg="white", font=("Arial", 10), insertbackground="white")
            text_field.pack(side="left", padx=5, fill="x", expand=True)
        if isinstance(value, float):
            float_var = tk.DoubleVar(value=value)
            text_field = tk.Entry(frame_row, textvariable=float_var, bg="#444444", fg="white", font=("Arial", 10), insertbackground="white")
            text_field.pack(side="left", padx=5, fill="x", expand=True)
        if isinstance(value, dict):
            pass


# Some quick tests
# Load JSON file into a variable
with open('config.json', 'r') as file:
    config_json = json.load(file)

# Example usage
print(get_tabs(config_json))
print(get_labels(config_json, 'graphics'))
print(get_labels(config_json, 'physics'))