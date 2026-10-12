import ctypes
import ctypes.util
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


# --- Display detection via SDL2 (in-process) ---
#
# This settings app runs inside Kivy, which uses SDL2 for its own OpenGL
# context - so SDL2 is already loaded and safe to query in-process (no
# subprocess needed). It also reports the true physical resolution under
# Wayland, unlike `screeninfo` (which read X11/xrandr through XWayland and
# reported the scaled size, e.g. 4096x2304 instead of 3840x2160).
#
# The engine is migrating to SDL3; when Kivy does too, these SDL2 calls
# (SDL_GetNumVideoDisplays / SDL_GetDesktopDisplayMode / SDL_GetDisplayDPI)
# can be swapped for their SDL3 equivalents in one place.

SDL_INIT_VIDEO = 0x00000020


class _SDL2_DisplayMode(ctypes.Structure):
    _fields_ = [
        ("format", ctypes.c_uint32),
        ("w", ctypes.c_int),
        ("h", ctypes.c_int),
        ("refresh_rate", ctypes.c_int),
        ("driverdata", ctypes.c_void_p),
    ]


def _load_sdl2():
    """Load the SDL2 library for the current platform.

    ctypes.util.find_library resolves the name on most systems, but on
    macOS a Homebrew SDL2 is not in the default dyld search path, so fall
    back to `brew --prefix sdl2` (per reviewer feedback).
    """
    libname = ctypes.util.find_library("SDL2")
    if libname is None:
        if sys.platform == "darwin":
            try:
                prefix = subprocess.check_output(["brew", "--prefix", "sdl2"], text=True).strip()
                libname = f"{prefix}/lib/libSDL2.dylib"
            except (subprocess.CalledProcessError, OSError):
                libname = "libSDL2-2.0.dylib"
        elif sys.platform == "win32":
            libname = "SDL2.dll"
        else:
            libname = "libSDL2-2.0.so.0"
    return ctypes.CDLL(libname)


def get_monitors():
    """Return the connected displays via SDL2 as a list of Monitor objects.

    SDL2's SDL_DisplayMode w/h are in points; scale by the display DPI
    relative to 96 DPI to get the physical resolution.
    """
    try:
        sdl = _load_sdl2()
    except OSError:
        return []

    sdl.SDL_Init(SDL_INIT_VIDEO)
    sdl.SDL_GetNumVideoDisplays.argtypes = []
    sdl.SDL_GetNumVideoDisplays.restype = ctypes.c_int
    sdl.SDL_GetDisplayName.argtypes = [ctypes.c_int]
    sdl.SDL_GetDisplayName.restype = ctypes.c_char_p
    sdl.SDL_GetDesktopDisplayMode.argtypes = [ctypes.c_int, ctypes.POINTER(_SDL2_DisplayMode)]
    sdl.SDL_GetDesktopDisplayMode.restype = ctypes.c_int
    sdl.SDL_GetDisplayDPI.argtypes = [ctypes.c_int,
                                      ctypes.POINTER(ctypes.c_float),
                                      ctypes.POINTER(ctypes.c_float),
                                      ctypes.POINTER(ctypes.c_float)]
    sdl.SDL_GetDisplayDPI.restype = ctypes.c_int

    n = sdl.SDL_GetNumVideoDisplays()
    monitors = []
    for i in range(n):
        name = sdl.SDL_GetDisplayName(i)
        mode = _SDL2_DisplayMode()
        if sdl.SDL_GetDesktopDisplayMode(i, ctypes.byref(mode)) != 0:
            continue
        # SDL2 has no pixel_density; SDL_DisplayMode.w/h are in points. For a
        # physical resolution, scale by the display DPI relative to 96 DPI.
        ddpi = ctypes.c_float(0)
        hdpi = ctypes.c_float(0)
        vdpi = ctypes.c_float(0)
        sx = sy = 1.0
        if sdl.SDL_GetDisplayDPI(i, ctypes.byref(ddpi), ctypes.byref(hdpi), ctypes.byref(vdpi)) == 0 and ddpi.value > 0:
            sx = hdpi.value / ddpi.value if hdpi.value > 0 else 1.0
            sy = vdpi.value / ddpi.value if vdpi.value > 0 else 1.0
        monitors.append({
            "name": name.decode() if name else str(i),
            "is_primary": i == 0,  # SDL2 has no primary concept; use the first
            "width": round(mode.w * sx),
            "height": round(mode.h * sy),
        })
    return [Monitor(m["name"], m["is_primary"], m["width"], m["height"]) for m in monitors]


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
