from importlib import import_module as _import_module

CShape3D = _import_module(".CShape3D", __name__)
__all__ = ["CShape3D"]
