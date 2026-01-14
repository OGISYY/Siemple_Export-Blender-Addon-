import bpy
import os

class Exporter(bpy.types.Operator):
    bl_idname = "export.validate"
    bl_label = "Configuration Validate"
    bl_description="Check if the configuration is correct"
    bl_options = {"REGISTER", "UNDO"}

    def load_operator_preset(self, operator, preset):
        options = {}
        if preset == 'NO_PRESET':
            return options

        for d in bpy.utils.script_paths(subdir="presets/operator/" + operator):
            fp = "".join([d, "/", preset, ".py"])
            if os.path.isfile(fp):  # Found the preset file
                print("Using preset " + fp)
                file = open(fp, 'r')
                for line in file.readlines():
                    # This assumes formatting of these files remains exactly the same
                    if line.startswith("op."):
                        line = line.removeprefix("op.")
                        split = line.split(" = ")
                        key = split[0]
                        value = split[1]
                        options[key] = eval(value)
                file.close()
                return options
        # If it didn't find the preset, use empty options
        # (the preset option should look blank if the file doesn't exist anyway)
        return options
    def execute(self, context):

        props = context.scene.props
        self.file_count = 0

        base_dir = bpy.path.abspath(props.export_path)
        if not base_dir or not os.path.isdir(base_dir):
            
            self.report(
                {"ERROR"}, "Save blend file somewhere before exporting or add an export path."
            )
            return{"FINISHED"}
        base_dir = bpy.path.abspath(base_dir) #? Converto to absolute dir
        if not os.path.isdir(base_dir): #? Check if this dir is correct
            self.report({"ERROR"},"This Export path is not correct.")
            return{"FINISHED"}
            
        view_layer = context.view_layer
        obj_active =  view_layer.objects.active
        selection = context.selected_objects
        objects = view_layer.objects.values()

        if props.limit == "SELECTED":
            objects = selection

        mode = ""

        if obj_active:
            mode = obj_active.mode
            bpy.ops.object.mode_set(mode="OBJECT") #! Only Work in Object Mode

        if props.mode == "OBJECTS":
            for obj in objects:
                if obj.type not in props.object_types:
                    continue
                bpy.ops.object.select_all(action="DESELECT")
                obj.select_set(True)
        
        elif props.mode == 'COLLECTIONS':
            for col in bpy.data.collections.values():
                bpy.ops.object.select_all(action='DESELECT')
                for obj in col.objects:
                    if obj.type not in props.object_types:
                        continue
                    if not obj in objects:
                        continue
                    obj.select_set(True)
                if context.selected_objects:
                    self.export_selection(col.name, context, base_dir)

        for obj in selection:
            obj.select_set(True)
            view_layer.objects.active = obj_active

            # Return to whatever mode the user was in
            if obj_active:
                bpy.ops.object.mode_set(mode=mode)

            if self.file_count == 0:
                self.report({'ERROR'}, "NOTHING TO EXPORT")
            else:
                self.report({'INFO'}, "Exported " +
                            str(self.file_count) + " file(s)")

        
        return {"FINISHED"}



    def export_selection(self, itemname, context, base_dir ):
        props = context.scene.props

        prefix = props.prefix
        suffix = props.suffix
        name = prefix + bpy.path.clean_name(itemname) + suffix
        fp = os.path.join(base_dir, name)

        if props.file_format == "OBJ":
            options = self.load_operator_preset(
                'wm.obj_export', props.obj_preset)
            options["filepath"] = fp+".obj"
            options["export_selected_objects"] = True
            options["apply_modifiers"] = props.apply_modifiers
            bpy.ops.wm.obj_export(**options)
            self.file_count += 1

        elif props.file_format == "FBX":
            options = self.load_operator_preset(
                'export_scene.fbx', props.fbx_preset)
            options["filepath"] = fp+".fbx"
            options["use_selection"] = True
            options["use_mesh_modifiers"] = props.apply_modifiers
            bpy.ops.export_scene.fbx(**options)
            self.file_count += 1




        
def register():
    bpy.utils.register_class(Exporter)

def unregister():
    bpy.utils.unregister_class(Exporter)