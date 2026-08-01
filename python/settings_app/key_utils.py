acronyms = ['ai']

# SDL keycodes for modifier keys. These must never be bound as a key on
# their own - Kivy gives them bogus codepoints (shift -> '\u0130') and they
# are pressed as part of a chord (Shift+= -> '+').
MODIFIER_KEYCODES = {303, 304, 305, 306, 307, 308, 309, 310, 311}
# 303/304 = shift, 305/306 = ctrl, 307/308 = alt, 309/310 = meta, 311 = compose

# Kivy on_key_down passes 'keycode' as the SDL keycode (see
# kivy/core/window/window_sdl2.py: key = self.key_map[key]). The engine's
# config uses its own key names (initKeyMap in config_xml.cpp). Translate
# Kivy's key name (from Keyboard.keycodes) to the engine name, then map
# keycode -> engine name.
KIVY_TO_ENGINE = {
    'spacebar': 'space',
    'enter': 'return',
    'escape': 'esc',
    'numpad0': 'keypad-0', 'numpad1': 'keypad-1', 'numpad2': 'keypad-2',
    'numpad3': 'keypad-3', 'numpad4': 'keypad-4', 'numpad5': 'keypad-5',
    'numpad6': 'keypad-6', 'numpad7': 'keypad-7', 'numpad8': 'keypad-8',
    'numpad9': 'keypad-9',
    'numpaddecimal': 'keypad-period', 'numpaddivide': 'keypad-divide',
    'numpadmul': 'keypad-multiply', 'numpadsubstract': 'keypad-minus',
    'numpadadd': 'keypad-plus', 'numpadenter': 'keypad-enter',
    'up': 'cursor-up', 'down': 'cursor-down', 'left': 'cursor-left',
    'right': 'cursor-right',
    'insert': 'cursor-insert', 'home': 'cursor-home', 'end': 'cursor-end',
    'pageup': 'cursor-pageup', 'pagedown': 'cursor-pagedown',
    'delete': 'cursor-delete',
    'f1': 'function-1', 'f2': 'function-2', 'f3': 'function-3',
    'f4': 'function-4', 'f5': 'function-5', 'f6': 'function-6',
    'f7': 'function-7', 'f8': 'function-8', 'f9': 'function-9',
    'f10': 'function-10', 'f11': 'function-11', 'f12': 'function-12',
    'f13': 'function-13', 'f14': 'function-14', 'f15': 'function-15',
    'numlock': 'keypad-numlock', 'capslock': 'capslock',
    'scrollock': 'scrollock', 'pause': 'pause', 'tab': 'tab',
    'backspace': 'backspace', 'lctrl': 'left-ctrl', 'rctrl': 'right-ctrl',
    'alt': 'left-alt', 'alt-gr': 'right-alt',
}


def keycode_to_engine_name(keycode: int, codepoint: str) -> str:
    """Convert a captured key to the engine's config key name.

    Special keys (tab, arrows, F-keys, keypad, etc.) map via Kivy's
    Keyboard.keycodes (SDL keycode -> kivy name) then KIVY_TO_ENGINE.
    Printable keys use their codepoint (e.g. 'a', '1').
    """
    from kivy.core.window import Keyboard
    kivy_name = None
    for name, code in Keyboard.keycodes.items():
        if code == keycode:
            kivy_name = name
            break
    if kivy_name:
        engine_name = KIVY_TO_ENGINE.get(kivy_name)
        if engine_name:
            return engine_name
    if codepoint:
        return codepoint
    return None


# Friendly display names for engine key names.
ENGINE_KEY_DISPLAY = {
    'tab': 'Tab', 'return': 'Enter', 'enter': 'Numpad Enter', 'esc': 'Esc',
    'backspace': 'Backspace', 'space': 'Space', 'pause': 'Pause', 'break': 'Break',
    'cursor-up': '\u2191', 'cursor-down': '\u2193', 'cursor-left': '\u2190', 'cursor-right': '\u2192',
    'cursor-home': 'Home', 'cursor-end': 'End', 'cursor-insert': 'Insert', 'cursor-delete': 'Delete',
    'cursor-pageup': 'Page Up', 'cursor-pagedown': 'Page Down',
    'capslock': 'Caps Lock', 'scrollock': 'Scroll Lock', 'keypad-numlock': 'Num Lock',
    'less-than': '<', 'greater-than': '>',
    'left-ctrl': 'L Ctrl', 'right-ctrl': 'R Ctrl', 'left-alt': 'L Alt', 'right-alt': 'R Alt',
    'left-meta': 'L Meta', 'right-meta': 'R Meta', 'shift': 'Shift',
}


def format_key_display(engine_key: str) -> str:
    """Convert an engine config key name to a friendly display label.

    Handles function-N, keypad-N, and the ENGINE_KEY_DISPLAY table; otherwise
    returns the key as-is (printable chars).
    """
    if engine_key in ENGINE_KEY_DISPLAY:
        return ENGINE_KEY_DISPLAY[engine_key]
    if engine_key.startswith('function-'):
        return 'F' + engine_key[len('function-'):]
    if engine_key.startswith('keypad-'):
        return 'Numpad ' + engine_key[len('keypad-'):]
    return engine_key


def format_key(key: str) -> str:
    """
    Formats a key by converting underscores to spaces, capitalizing the first letter of each word,
    and fully capitalizing words that are acronyms.

    Args:
        key (str): The input key to format.
        acronyms (list): A list of acronyms to check against.

    Returns:
        str: The formatted key.
    """
    words = key.replace('_', ' ').split()
    formatted_words = [
        word.upper() if word in acronyms else word.capitalize()
        for word in words
    ]
    return ' '.join(formatted_words)


# Test
if __name__ == "__main__":
    keys = ['ai','audio_in_cockpit']
    
    for key in keys:
        print(format_key(key))
