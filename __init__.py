bl_info = {
    "name": "Simple Export",
    "author": "OGISY",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "3D Viewport > Sidebar (N) > Simple Export",
    "description": "Batch export objects or collections to FBX / OBJ in one click",
    "category": "Import-Export",
}

# Permite recargar el addon (F3 > Reload Scripts) sin reiniciar Blender
if "bpy" in locals():
    import importlib
    importlib.reload(utils)
    importlib.reload(properties)
    importlib.reload(operators)
    importlib.reload(panels)
else:
    from . import utils, properties, operators, panels

import bpy


def register():
    properties.register()
    operators.register()
    panels.register()


def unregister():
    panels.unregister()
    operators.unregister()
    properties.unregister()
