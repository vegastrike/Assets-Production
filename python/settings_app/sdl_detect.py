##
# sdl_detect.py
#
# Vega Strike - Space Simulation, Combat and Trading
# Copyright (C) 2001-2026 The Vega Strike Contributors:
# Project creator: Daniel Horn
# Original development team: As listed in the AUTHORS file
# Current development team: Roy Falk, Benjamen R. Meyer, Stephen G. Tuggy
#
# https://github.com/vegastrike/Vega-Strike-Engine-Source
#
# This file is part of Vega Strike.
#
# Vega Strike is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Vega Strike is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Vega Strike.  If not, see <https://www.gnu.org/licenses/>.
import ctypes
import ctypes.util
import json
import sys

SDL_INIT_VIDEO = 0x00000020


class _SDL3_DisplayMode(ctypes.Structure):
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


class _SDL2_DisplayMode(ctypes.Structure):
    _fields_ = [
        ("format", ctypes.c_uint32),
        ("w", ctypes.c_int),
        ("h", ctypes.c_int),
        ("refresh_rate", ctypes.c_int),
        ("driverdata", ctypes.c_void_p),
    ]


def _load_lib(prefix):
    """Load an SDL library by name prefix (e.g. 'SDL3' or 'SDL2')."""
    libname = ctypes.util.find_library(prefix)
    if libname is None:
        # Platform-aware fallbacks for the two SDL major versions.
        libname = {
            ("SDL3", "win32"): "SDL3.dll",
            ("SDL3", "darwin"): "libSDL3.dylib",
            ("SDL3", "linux"): "libSDL3.so.0",
            ("SDL2", "win32"): "SDL2.dll",
            ("SDL2", "darwin"): "libSDL2-2.0.dylib",
            ("SDL2", "linux"): "libSDL2-2.0.so.0",
        }[(prefix, sys.platform)]
    return ctypes.CDLL(libname)


def _detect_sdl3():
    """Enumerate displays via SDL3 (master engine)."""
    sdl = _load_lib("SDL3")
    sdl.SDL_Init(SDL_INIT_VIDEO)
    sdl.SDL_GetDisplays.argtypes = [ctypes.POINTER(ctypes.c_int)]
    sdl.SDL_GetDisplays.restype = ctypes.POINTER(ctypes.c_uint32)
    sdl.SDL_GetDisplayName.argtypes = [ctypes.c_uint32]
    sdl.SDL_GetDisplayName.restype = ctypes.c_char_p
    sdl.SDL_GetPrimaryDisplay.argtypes = []
    sdl.SDL_GetPrimaryDisplay.restype = ctypes.c_uint32
    sdl.SDL_GetDesktopDisplayMode.argtypes = [ctypes.c_uint32]
    sdl.SDL_GetDesktopDisplayMode.restype = ctypes.POINTER(_SDL3_DisplayMode)
    sdl.SDL_free.argtypes = [ctypes.c_void_p]
    sdl.SDL_free.restype = None

    count = ctypes.c_int(0)
    ids = sdl.SDL_GetDisplays(ctypes.byref(count))
    primary = sdl.SDL_GetPrimaryDisplay()
    monitors = []
    try:
        for i in range(count.value):
            did = ids[i]
            name = sdl.SDL_GetDisplayName(did)
            mode = sdl.SDL_GetDesktopDisplayMode(did)
            if not mode:
                continue
            m = mode.contents
            monitors.append({
                "name": name.decode() if name else str(did),
                "is_primary": did == primary,
                "width": round(m.w * m.pixel_density),
                "height": round(m.h * m.pixel_density),
            })
    finally:
        if ids:
            sdl.SDL_free(ids)
        sdl.SDL_Quit()
    return monitors


def _detect_sdl2():
    """Enumerate displays via SDL2 (0.10.x engine)."""
    sdl = _load_lib("SDL2")
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
    sdl.SDL_Quit()
    return monitors


def main():
    # Try SDL3 (master engine) first; fall back to SDL2 (0.10.x engine).
    try:
        monitors = _detect_sdl3()
    except OSError:
        monitors = _detect_sdl2()
    json.dump(monitors, sys.stdout)


if __name__ == "__main__":
    main()
