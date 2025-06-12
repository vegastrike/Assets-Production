import json
import sys
import tkinter as tk
import tkinter.ttk as ttk

import game_config as gc

def get_tabs(config_json):
    return list(config_json.keys())

def get_labels(config_json, key):
    return list(config_json[key].keys())


def get_label_and_checkbutton(root_element, label_text, initial_value):
    frame_row = ttk.Frame(root_element, bg="#2e2e2e")
    frame_row.pack(pady=10)

    label = ttk.Label(frame_row, text=f"{label_text}:", fg="white", bg="#2e2e2e", font=("Arial", 12))
    label.pack(side="left", padx=5)

    toggle_var = tk.BooleanVar(value=initial_value)
    toggle_button = tk.Checkbutton(frame_row, variable=toggle_var, bg="#2e2e2e", activebackground="#2e2e2e", 
                                   fg="white", selectcolor="#444444", font=("Arial", 12))
    toggle_button.pack(side="left", padx=5)

    return toggle_var

def get_tab_data(root_element, tab_json, level=0):
    for key, value in tab_json.items():
        # Add a label and a control (e.g. checkbox) on the same line
        frame_row = ttk.Frame(root_element, bg="#2e2e2e")
        frame_row.pack(pady=10)

        label = ttk.Label(frame_row, text=f"{key}:", fg="white", bg="#2e2e2e", font=("Arial", 12))
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


def generate_lower_level_section(frame, section: gc.ConfigBranch):
    # Create a label for the section
    section_label = ttk.Label(frame, text=f"{section.key}", font=("Arial", 14, "bold"))
    section_label.pack(anchor="w", padx=10, pady=5)

    inner_frame = ttk.Frame(frame)
    inner_frame.config(borderwidth=2, relief="solid") # Add border

    # Populate the sub-frame with data from the section and key
    for key, value in section.value.items():
        if isinstance(value, gc.ConfigBranch):
            # For nested dictionaries, recursively call this function
            generate_lower_level_section(inner_frame, section.value[section], section, key)
        elif isinstance(value, gc.ConfigLeaf):
            # Create a label and control for each key-value pair
            label = ttk.Label(frame, text=f"{key}: {value.value} (orig: {value.original_value})", font=("Arial", 12))
            label.pack(anchor="w", padx=10, pady=5)
        else:
            # Create a label and control for each key-value pair
            label = ttk.Label(frame, text=f"{key}: {value}", font=("Arial", 12))
            label.pack(anchor="w", padx=10, pady=5)
            sys.exit(f"Unsupported value type: {type(value)} for key: {key}")

# This section converts the JSON configuration into a GUI representation.
def generate_first_level_section(right_frame, section:gc.ConfigBranch):
    inner_frame = create_frame_in_a_scrollbar_frame(right_frame)

    if not section:
        return

    # Populate the sub-frame with data from the section
    for key, value in section.value.items():
        if isinstance(value, gc.ConfigBranch):
            # For nested dictionaries, recursively call this function
            generate_lower_level_section(inner_frame, value)
        elif isinstance(value, gc.ConfigLeaf):
            # Create a label and control for each key-value pair
            label = ttk.Label(inner_frame, text=f"{key}: {value.value} (orig: {value.original_value})", font=("Arial", 12))
            label.pack(anchor="w", padx=10, pady=5)
        else:
            # Create a label and control for each key-value pair
            label = ttk.Label(inner_frame, text=f"{key}: {value}", font=("Arial", 12))
            label.pack(anchor="w", padx=10, pady=5)
            sys.exit(f"Unsupported value type: {type(value)} for key: {key}")


def create_frame_in_a_scrollbar_frame(parent_frame):
    # Add a scrollbar to the left frame
    scrollbar = ttk.Scrollbar(parent_frame, orient="vertical")
    scrollbar.pack(side="right", fill="y")

    # Create a canvas to hold the content
    canvas = tk.Canvas(parent_frame, yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=False)

    # Configure the scrollbar to scroll the canvas
    scrollbar.config(command=canvas.yview)

    # Create an inner frame inside the canvas
    inner_frame = ttk.Frame(canvas)
    inner_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Add the inner frame to the canvas
    canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    return inner_frame

# Test Code
if __name__ == "__main__":
    # Load JSON file into a variable
    with open('config.json', 'r') as file:
        config_json = json.load(file)

    # Example usage
    print(get_tabs(config_json))
    print(get_labels(config_json, 'graphics'))
    print(get_labels(config_json, 'physics'))