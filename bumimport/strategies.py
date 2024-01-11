"""Implementations of import strategies"""

import fnmatch
import importlib
import os
import sys
from types import ModuleType

def flat_import(module: str | ModuleType, path: str | os.PathLike) -> None:
    """Recursively import all modules in a path to the provided module"""

    if isinstance(module, str):
        if module in sys.modules:
            module = sys.modules[module]
        else:
            raise ValueError(f"No module named: {module}")
    elif not isinstance(module, ModuleType):
        raise TypeError(f"Invalid module type: {type(module)}")

    if isinstance(path, str):
        if os.path.isfile(path):
            path = os.path.dirname(path)  # call flat_import with path=__file__
        elif not os.path.isdir(path):
            raise ValueError(f"No path named: {path}")
    elif not isinstance(path, os.PathLike):
        raise TypeError(f"Invalid path type: {type(path)}")

    sys_path = sys.path

    for root, dirs, _ in os.walk(path):
        for d in dirs:
            d = os.path.join(root, d)
            sys.path.insert(0, d)
            for f in fnmatch.filter(os.listdir(d), "*.py"):
                f = os.path.splitext(f)[0]
                setattr(module, f, importlib.import_module(f))

    sys.path = sys_path
