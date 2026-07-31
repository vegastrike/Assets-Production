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

def main():
    # Resolve the SDL3 library name for the current platform (SDL3.dll on
    # Windows, libSDL3.dylib on macOS, libSDL3.so on Linux) instead of
    # hardcoding the Linux name, so this works cross-platform.
    libname = ctypes.util.find_library("SDL3")
    if libname is None:
        libname = "libSDL3.so.0"  # fallback for Linux when find_library fails
    sdl = ctypes.CDLL(libname)
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
    json.dump(monitors, sys.stdout)

if __name__ == "__main__":
    main()
