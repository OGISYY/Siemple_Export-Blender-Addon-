import bpy
import importlib
from . import properties, operators, panels

bl_info = {
    "name": "Simple Export",
    "blender": (4, 0, 0),
    "category": "3D View",
}

def register():
    importlib.reload(properties)
    importlib.reload(operators)
    importlib.reload(panels)
    properties.register()
    operators.register()
    panels.register()

def unregister():
    panels.unregister()
    operators.unregister()
    properties.unregister()