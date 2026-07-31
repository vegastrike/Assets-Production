import json
import os
import subprocess
import sys

import app_config as ac

# This file cannot be in the utils sub-folder where it belongs
def change_to_python_settings_app_folder():
    if ac.app_config.assets_folder:
        os.chdir(os.path.join(ac.app_config.assets_folder, "python", "settings_app"))

def append_subfolders_to_system_path():
    subfolders = ['tabs', 'graphics_factory']
    current_folder = os.getcwd()
    for folder in subfolders:
        sys.path.append(os.path.join(current_folder, folder))


# --- Display detection via SDL3 (in a subprocess) ---
#
# The engine renders through SDL3, so we query the same library the game
# uses. This is OS-agnostic and works correctly under Wayland, unlike the
# previous `screeninfo` approach (which read X11/xrandr and reported the
# XWayland-scaled resolution, e.g. 4096x2304 instead of the monitor's
# native 3840x2160).
#
# SDL must be queried in a child process: this settings app runs inside
# Kivy, which uses SDL2 for its own OpenGL context. Initialising SDL3 in
# the same process tears down that context and segfaults on rendering.

def get_monitors():
    """Return the connected displays via SDL3 as a list of Monitor objects.

    Resolution is reported in physical pixels (SDL's desktop mode reports
    logical pixels; multiply by pixel_density to get the native size).
    """
    script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sdl_detect.py")
    try:
        result = subprocess.run([sys.executable, script], capture_output=True, timeout=10)
    except (subprocess.TimeoutExpired, OSError):
        return []
    if result.returncode != 0:
        return []
    try:
        data = json.loads(result.stdout.decode())
    except ValueError:
        return []
    return [Monitor(m["name"], m["is_primary"], m["width"], m["height"]) for m in data]

class Monitor:
    """A lightweight stand-in for a screeninfo.Monitor."""
    def __init__(self, name, is_primary, width, height):
        self.name = name
        self.is_primary = is_primary
        self.width = width
        self.height = height

def number_of_screens():
    return len(get_monitors())

def resolution_for_screen(index):
    screens = get_monitors()
    if index >= len(screens):
        return None
    screen = screens[index]
    return (screen.width, screen.height)

# Test section
if __name__ == "__main__":
    print(number_of_screens())
    resolution_for_screen(0)
