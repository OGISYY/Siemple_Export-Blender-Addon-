import bpy
import os

from .utils import load_operator_preset


class SIMPLEEXPORT_OT_export(bpy.types.Operator):
    bl_idname = "simple_export.export"
    bl_label = "Simple Export"
    bl_description = "Export the objects or collections with the current settings"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return context.scene is not None and context.view_layer is not None

    def execute(self, context):
        props = context.scene.simple_export
        self.file_count = 0

        #? Validar ruta de exportacion
        if props.export_path.startswith("//") and not bpy.data.is_saved:
            self.report({"ERROR"}, "Save the blend file before using a relative export path ('//').")
            return {"CANCELLED"}

        base_dir = bpy.path.abspath(props.export_path)
        if not base_dir.strip():
            self.report({"ERROR"}, "Set an export directory.")
            return {"CANCELLED"}
        try:
            os.makedirs(base_dir, exist_ok=True)
        except OSError as e:
            self.report({"ERROR"}, "Invalid export path: " + str(e))
            return {"CANCELLED"}

        view_layer = context.view_layer
        obj_active = view_layer.objects.active
        selection = list(context.selected_objects)

        if props.limit == "SELECTED":
            objects = selection
        else:
            objects = [obj for obj in view_layer.objects if obj.visible_get()]
        objects = [obj for obj in objects if obj.type in props.object_types]
        objects_set = set(objects)

        #! Solo funciona en Object Mode
        mode = obj_active.mode if obj_active else "OBJECT"
        if mode != "OBJECT" and bpy.ops.object.mode_set.poll():
            bpy.ops.object.mode_set(mode="OBJECT")

        try:
            if props.mode == "OBJECTS":
                for obj in objects:
                    self.select_only(view_layer, [obj])
                    view_layer.objects.active = obj
                    self.export_selection(obj.name, context, base_dir)

            elif props.mode == "COLLECTIONS":
                scene_col = context.scene.collection
                for col in [scene_col] + list(scene_col.children_recursive):
                    col_objects = [obj for obj in col.objects if obj in objects_set]
                    if not col_objects:
                        continue
                    self.select_only(view_layer, col_objects)
                    view_layer.objects.active = col_objects[0]
                    # Los objetos sueltos en la Scene Collection usan el nombre de la escena
                    name = context.scene.name if col == scene_col else col.name
                    self.export_selection(name, context, base_dir)
        except Exception as e:
            self.report({"ERROR"}, "Export failed: " + str(e))
            return {"CANCELLED"}
        finally:
            #? Restaurar seleccion, objeto activo y modo del usuario
            self.select_only(view_layer, selection)
            view_layer.objects.active = obj_active
            if obj_active and mode != "OBJECT" and bpy.ops.object.mode_set.poll():
                bpy.ops.object.mode_set(mode=mode)

        if self.file_count == 0:
            self.report({"WARNING"}, "Nothing to export (check selection, limit and object types).")
            return {"CANCELLED"}

        self.report({"INFO"}, "Exported %d file(s) to %s" % (self.file_count, base_dir))
        return {"FINISHED"}

    @staticmethod
    def select_only(view_layer, objects):
        for obj in view_layer.objects:
            obj.select_set(False)
        for obj in objects:
            if obj.name in view_layer.objects:
                obj.select_set(True)

    def export_selection(self, itemname, context, base_dir):
        props = context.scene.simple_export

        name = props.prefix + bpy.path.clean_name(itemname) + props.suffix
        fp = os.path.join(base_dir, name)

        if props.file_format == "OBJ":
            options = load_operator_preset('wm.obj_export', props.obj_preset)
            options["filepath"] = fp + ".obj"
            options["export_selected_objects"] = True
            options["apply_modifiers"] = props.apply_modifiers
            bpy.ops.wm.obj_export(**options)
            self.file_count += 1

        elif props.file_format == "FBX":
            options = load_operator_preset('export_scene.fbx', props.fbx_preset)
            options["filepath"] = fp + ".fbx"
            options["use_selection"] = True
            options["use_mesh_modifiers"] = props.apply_modifiers
            options["bake_space_transform"] = props.apply_transform
            bpy.ops.export_scene.fbx(**options)
            self.file_count += 1


def register():
    bpy.utils.register_class(SIMPLEEXPORT_OT_export)


def unregister():
    bpy.utils.unregister_class(SIMPLEEXPORT_OT_export)
