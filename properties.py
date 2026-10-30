import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import PropertyGroup
from .utils import get_operator_presets, get_preset_index, set_preset


class SIMPLEEXPORT_PG_properties(PropertyGroup):
    prefix: StringProperty(name="Prefix", default="")
    suffix: StringProperty(name="Suffix", default="")

    export_path: StringProperty(
        name="Directory",
        description="Folder to export to. '//' means the folder of the .blend file",
        default="//",
        subtype='DIR_PATH'
    )

    apply_modifiers: BoolProperty(
        name="Apply Modifiers",
        description="Apply modifiers to the exported meshes",
        default=False
    )
    apply_transform: BoolProperty(
        name="Apply Transform",
        description="Bake space transform into object data (FBX only)",
        default=False
    )

    object_types: EnumProperty(
        name="Object Types",
        options={"ENUM_FLAG"},
        description="Object types to export",
        items=[
            ('MESH', "Mesh", "", 1),
            ('CURVE', "Curve", "", 2),
            ('SURFACE', "Surface", "", 4),
            ('META', "Metaball", "", 8),
            ('FONT', "Text", "", 16),
            ('ARMATURE', "Armature", "", 64),
            ('EMPTY', "Empty", "", 128),
            ('LIGHT', "Lamp", "", 256),
            ('CAMERA', "Camera", "", 512),
        ],
        default={'MESH'}
    )

    file_format: EnumProperty(
        name="Format",
        description="Which file format to export to",
        items=[
            ("OBJ", "Wavefront (.obj)", "", 7),
            ("FBX", "FBX (.fbx)", "", 5),
        ],
        default="FBX"
    )

    mode: EnumProperty(
        name="Mode",
        description="What to export",
        items=[
            ("OBJECTS", "Objects", "Each object is exported to its own file", 1),
            ("COLLECTIONS", "Collections",
             "Each collection is exported into its own file", 3),
        ],
        default="COLLECTIONS"
    )

    limit: EnumProperty(
        name="Limit to",
        description="How to limit which objects are exported",
        items=[
            ("VISIBLE", "Visible", "", 1),
            ("SELECTED", "Selected", "", 2),
        ],
        default="SELECTED"
    )

    #! Rare Use
    obj_preset: StringProperty(default='NO_PRESET')
    obj_preset_enum: EnumProperty(
        name="Preset",
        options={'SKIP_SAVE'},
        description="Use export settings from a preset.\n(Create in the export settings from the File > Export > Wavefront (.obj))",
        items=lambda self, context: get_operator_presets('wm.obj_export'),
        get=lambda self: get_preset_index('wm.obj_export', self.obj_preset),
        set=lambda self, value: set_preset(self, 'obj_preset', 'wm.obj_export', value),
    )
    fbx_preset: StringProperty(default='NO_PRESET')
    fbx_preset_enum: EnumProperty(
        name="Preset",
        options={'SKIP_SAVE'},
        description="Use export settings from a preset.\n(Create in the export settings from the File > Export > FBX (.fbx))",
        items=lambda self, context: get_operator_presets('export_scene.fbx'),
        get=lambda self: get_preset_index('export_scene.fbx', self.fbx_preset),
        set=lambda self, value: set_preset(self, 'fbx_preset', 'export_scene.fbx', value),
    )


def register():
    bpy.utils.register_class(SIMPLEEXPORT_PG_properties)
    bpy.types.Scene.simple_export = bpy.props.PointerProperty(type=SIMPLEEXPORT_PG_properties)


def unregister():
    del bpy.types.Scene.simple_export
    bpy.utils.unregister_class(SIMPLEEXPORT_PG_properties)
