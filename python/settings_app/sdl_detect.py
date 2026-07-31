import ctypes, json, sys

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
    sdl = ctypes.CDLL("libSDL3.so.0")
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
