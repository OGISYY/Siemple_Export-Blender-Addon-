# utils.py

import bpy
import os

preset_enum_items_refs = {}

def get_operator_presets(operator):
    presets = [('NO_PRESET', "(no preset)", "", 0)]
    for d in bpy.utils.script_paths(subdir="presets/operator/" + operator):
        for f in os.listdir(d):
            if not f.endswith(".py"):
                continue
            f = os.path.splitext(f)[0]
            presets.append((f, f, ""))
    # Blender's doc warns that not keeping reference to enum props array can
    # cause crashs and weird issues:
    preset_enum_items_refs[operator] = presets
    return presets


def get_preset_index(operator_idname, preset_name):
    items = preset_enum_items_refs.get(operator_idname, [])
    for i, item in enumerate(items):
        if item[0] == preset_name:
            return i
    return 0
