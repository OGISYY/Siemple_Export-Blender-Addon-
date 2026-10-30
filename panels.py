import bpy


class SIMPLEEXPORT_PT_panel(bpy.types.Panel):
    bl_label = "Simple Export"  # Titulo que se ve en UI
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Simple Export'  # Nombre el cual tendra en la barra de addons

    def draw(self, context):
        #Definimos campos
        layout = self.layout  # Nuestra Ui dentro de codigo
        props = context.scene.simple_export  # props
        #Alineacion
        layout.use_property_split = True
        layout.use_property_decorate = False

        #Text Settings
        boxA = layout.box()
        colA = boxA.column(align=True)
        colA.prop(props, "export_path")
        colA.prop(props, "prefix")
        colA.prop(props, "suffix")

        layout.separator()

        #Object Type
        box_toggles = layout.box()
        box_toggles.label(text="Object Types:")
        box_toggles.use_property_split = False
        grid = box_toggles.grid_flow(columns=3, align=True)
        grid.prop(props, "object_types", expand=True)

        layout.separator()

        # Export Settings
        box_exportSettings = layout.box()
        col = box_exportSettings.column(align=True)
        col.label(text="Export Settings:")
        col.prop(props, "file_format")
        col.prop(props, "mode")
        col.prop(props, "limit")
        box_exportSettings.prop(props, "apply_modifiers")
        if props.file_format == "FBX":
            box_exportSettings.prop(props, "apply_transform")

        layout.separator()

        #? Some extensions formats
        box_formats = layout.box()
        box_formats.label(text=props.file_format + " Settings:")
        col = box_formats.column()
        if props.file_format == "OBJ":
            col.prop(props, "obj_preset_enum")
        elif props.file_format == "FBX":
            col.prop(props, "fbx_preset_enum")

        #! Export Button
        layout.separator()
        row = layout.row()
        row.scale_y = 1.5
        row.operator("simple_export.export", text="Simple Export", icon="EXPORT")


def register():
    bpy.utils.register_class(SIMPLEEXPORT_PT_panel)


def unregister():
    bpy.utils.unregister_class(SIMPLEEXPORT_PT_panel)
