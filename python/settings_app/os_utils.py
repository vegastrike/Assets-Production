import ctypes
import os
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


# --- Display detection via SDL3 (ctypes) ---
#
# The engine renders through SDL3, so we query the same library the game
# uses. This is OS-agnostic and, crucially, works correctly under Wayland,
# unlike the previous `screeninfo` approach (which read X11/xrandr and
# reported the XWayland-scaled resolution, e.g. 4096x2304 instead of the
# monitor's native 3840x2160).

SDL_INIT_VIDEO = 0x00000020

class _SDL_DisplayMode(ctypes.Structure):
    _fields_ = [
        ("displayID", ctypes.c_uint32),
        ("format", ctypes.c_uint32),
        ("w", ctypes.c_int),
        ("h", ctypes.c_int),
        ("pixel_density", ctypes.c_float),
        ("refresh_rate", ctypes.c_float),
        ("refresh_rate_numerator", ctypes.c_int),
        ("refresh_rate_denominator", ctypes.c_int),
        ("internal", ctypes.c_void_p),
    ]

_sdl = None

def _load_sdl():
    global _sdl
    if _sdl is None:
        _sdl = ctypes.CDLL("libSDL3.so.0")
    return _sdl

class Monitor:
    """A lightweight stand-in for a screeninfo.Monitor."""
    def __init__(self, name, is_primary, width, height):
        self.name = name
        self.is_primary = is_primary
        self.width = width
        self.height = height

def get_monitors():
    """Return the connected displays via SDL3 as a list of Monitor objects.

    Resolution is reported in physical pixels (SDL's desktop mode reports
    logical pixels; multiply by pixel_density to get the native size).
    """
    sdl = _load_sdl()
    sdl.SDL_Init(SDL_INIT_VIDEO)

    sdl.SDL_GetDisplays.argtypes = [ctypes.POINTER(ctypes.c_int)]
    sdl.SDL_GetDisplays.restype = ctypes.POINTER(ctypes.c_uint32)
    sdl.SDL_GetDisplayName.argtypes = [ctypes.c_uint32]
    sdl.SDL_GetDisplayName.restype = ctypes.c_char_p
    sdl.SDL_GetPrimaryDisplay.argtypes = []
    sdl.SDL_GetPrimaryDisplay.restype = ctypes.c_uint32
    sdl.SDL_GetDesktopDisplayMode.argtypes = [ctypes.c_uint32]
    sdl.SDL_GetDesktopDisplayMode.restype = ctypes.POINTER(_SDL_DisplayMode)
    sdl.SDL_free.argtypes = [ctypes.c_void_p]
    sdl.SDL_free.restype = None

    count = ctypes.c_int(0)
    ids = sdl.SDL_GetDisplays(ctypes.byref(count))
    primary = sdl.SDL_GetPrimaryDisplay()

    monitors = []
    try:
        for i in range(count.value):
            display_id = ids[i]
            name = sdl.SDL_GetDisplayName(display_id)
            mode = sdl.SDL_GetDesktopDisplayMode(display_id)
            if not mode:
                continue
            m = mode.contents
            monitors.append(Monitor(
                name=name.decode() if name else str(display_id),
                is_primary=(display_id == primary),
                width=round(m.w * m.pixel_density),
                height=round(m.h * m.pixel_density),
            ))
    finally:
        if ids:
            sdl.SDL_free(ids)
        sdl.SDL_Quit()

    return monitors

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
