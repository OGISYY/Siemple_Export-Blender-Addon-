import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import PropertyGroup
from .utils import get_operator_presets, get_preset_index, preset_enum_items_refs

class Properties(PropertyGroup):
    prefix : StringProperty(name="Prefix", default="")
    suffix : StringProperty(name="Suffix", default="")

    export_path: StringProperty(
        name="Directory",
        description="Path to export",
        default="Path",
        subtype='DIR_PATH'  
    )

    apply_modifiers : BoolProperty(name="Apply Modifiers", default=False)
    # apply_transform: BoolProperty(name="Apply Transform", default=False)

    object_types: EnumProperty(
        name="Object Types",
        options={"ENUM_FLAG"},
        description="Object Selection",
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
        name="Format:",
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
        items=lambda self, context: get_operator_presets('wm.obj_export'),
        get=lambda self: get_preset_index('wm.obj_export', self.obj_preset),
        set=lambda self, value: setattr(
            self, 'obj_preset',
            preset_enum_items_refs['wm.obj_export'][value][0]
        ),
    )
    fbx_preset: StringProperty(default='NO_PRESET')
    fbx_preset_enum: EnumProperty(
        name="Preset", options={'SKIP_SAVE'},
        description="Use export settings from a preset.\n(Create in the export settings from the File > Export > FBX (.fbx))",
        items=lambda self, context: get_operator_presets('export_scene.fbx'),
        get=lambda self: get_preset_index('export_scene.fbx', self.fbx_preset),
        set=lambda self, value: setattr(
            self, 'fbx_preset', preset_enum_items_refs['export_scene.fbx'][value][0]),
    )


    
def register():
    if hasattr(bpy.types.Scene, "props"):
        del bpy.types.Scene.props
        print("Reload")

    bpy.utils.register_class(Properties)
    bpy.types.Scene.props = bpy.props.PointerProperty(type=Properties)

def unregister():
    bpy.utils.unregister_class(Properties)
    del bpy.types.Scene.props
