# utils.py

import ast
import os

import bpy

preset_enum_items_refs = {}


def get_operator_presets(operator):
    presets = [('NO_PRESET', "(no preset)", "", 0)]
    names = set()
    for d in bpy.utils.script_paths(subdir="presets/operator/" + operator):
        if not os.path.isdir(d):
            continue
        for f in os.listdir(d):
            if f.endswith(".py"):
                names.add(os.path.splitext(f)[0])
    for i, name in enumerate(sorted(names), start=1):
        presets.append((name, name, "", i))
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


def set_preset(props, attr, operator_idname, value):
    items = preset_enum_items_refs.get(operator_idname, [])
    setattr(props, attr, items[value][0] if value < len(items) else 'NO_PRESET')


def load_operator_preset(operator, preset):
    """Lee un preset de operador (File > Export > ... > Operator Presets) y
    devuelve sus valores como kwargs para el operador."""
    options = {}
    if preset == 'NO_PRESET':
        return options

    for d in bpy.utils.script_paths(subdir="presets/operator/" + operator):
        fp = os.path.join(d, preset + ".py")
        if not os.path.isfile(fp):
            continue
        print("Simple Export: using preset " + fp)
        with open(fp, 'r', encoding='utf-8') as file:
            for line in file:
                # Formato de Blender: "op.<prop> = <valor>"
                if not line.startswith("op."):
                    continue
                key, sep, value = line[3:].partition(" = ")
                if not sep:
                    continue
                try:
                    options[key.strip()] = ast.literal_eval(value.strip())
                except (ValueError, SyntaxError):
                    print("Simple Export: skipping preset line " + line.strip())
        break

    # Ignora opciones que no existan en esta version de Blender
    category, name = operator.split(".")
    op = getattr(getattr(bpy.ops, category), name)
    valid = op.get_rna_type().properties.keys()
    return {k: v for k, v in options.items() if k in valid}
