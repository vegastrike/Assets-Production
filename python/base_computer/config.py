# Merge the split JSON config files the same way the engine does, so
# base_computer scripts read the effective config instead of a single raw file.
#
# The engine (InitPaths) merges, in order, later values overwriting earlier:
#   1. datadir bindings.json, theme.json, engine.json, config.json  (defaults)
#   2. homedir bindings.json, theme.json, engine.json, config.json  (user overrides)
# Within each group config.json loads last so a user-facing setting wins.
#
# engine.json holds its engine tuning under a "base" key; unwrap it so
# constants/components land at the merged root (the C++ engine does not do this
# itself, which is why those keys were silently missing after the config split).

import json
import os

CONFIG_FILES = ("bindings.json", "theme.json", "engine.json", "config.json")


def _homedir():
    # ~/.vegastrike — matches the engine's HOMESUBDIR. Portability via getpass.
    import getpass
    import platform

    system = platform.system().lower()
    if system == "windows":
        import ntpath
        base = os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local")
        return os.path.join(base, ".vegastrike")
    if system == "darwin":
        return os.path.join(os.path.expanduser("~"), ".vegastrike")
    return os.path.join(os.path.expanduser("~"), ".vegastrike")


def _merge(into, src):
    """Deep-merge src into into (dicts only; later values win, recursively)."""
    for key, value in src.items():
        if isinstance(value, dict) and isinstance(into.get(key), dict):
            _merge(into[key], value)
        else:
            into[key] = value


def _matching_files(directory):
    for name in CONFIG_FILES:
        path = os.path.join(directory, name)
        if os.path.exists(path):
            yield name, path


def _load_merged(directory):
    merged = {}
    for name, path in _matching_files(directory):
        with open(path, "r") as file:
            data = json.load(file)
        # Unwrap engine.json's "base" so its tuning keys live at the root.
        if name == "engine.json" and isinstance(data, dict) and isinstance(data.get("base"), dict):
            data = data["base"]
        _merge(merged, data)
    return merged


def load_merged_config():
    """Return the effective config (datadir defaults, overridden by homedir)."""
    merged = _load_merged(os.getcwd())
    _merge(merged, _load_merged(_homedir()))
    return merged
