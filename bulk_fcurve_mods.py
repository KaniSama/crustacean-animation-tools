import bpy
from bpy.types import Panel, Operator, Menu, PropertyGroup



class ClearModifiers(Operator):
    bl_idname = "bulkmods.clear_modifiers"
    bl_label = "Clear ALL"
    bl_description = "Clears all modifiers from selected objects"
        
    def execute(self, context):
        
        self.report({'INFO'}, 'bruh.')
        bpy.ops.graph.select_all()
                     
        return {'FINISHED'}

class ClearModifiersFromSelected(Operator):
    bl_idname = "bulkmods.clear_modifiers_from_selected"
    bl_label = "Clear from selected"
    bl_description = "Clears all modifiers from selected channels"
        
    def execute(self, context):
        
        self.report({'INFO'}, 'bruh.')
        bpy.ops.graph.select_all()
                     
        return {'FINISHED'}

class CrossCopyModifiersInSelected(Operator):
    bl_idname = "bulkmods.cross_copy_modifiers_in_selected"
    bl_label = "Cross-copy in selected"
    bl_description = "Copies all modifiers in any selected channel to all other selected channels"
        
    def execute(self, context):
        
        self.report({'INFO'}, 'bruh.')
        bpy.ops.graph.select_all()
                     
        return {'FINISHED'}
    


class BulkFCurveModsPanel(Panel):
    bl_idname = "GRAPH_PT_BulkFCurveModsPanel"
    bl_label = "Bulk FCurve Modifiers"
    bl_space_type = 'GRAPH_EDITOR'
    bl_region_type = 'UI'
    bl_area_type = 'GRAPH_EDITOR'
    bl_category = 'Modifiers'
    bl_options = {'HIDE_HEADER'}

    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.label(text='Bulk edit FCurve modifiers:')
        
        row = layout.row()
        row.operator(ClearModifiers.bl_idname, text = ClearModifiers.bl_label, icon = 'BRUSH_DATA')
        
        row = layout.row()
        row.operator(ClearModifiersFromSelected.bl_idname, text = ClearModifiersFromSelected.bl_label, icon = 'TRACKING_CLEAR_FORWARDS')
        
        row = layout.row()
        row.operator(CrossCopyModifiersInSelected.bl_idname, text = CrossCopyModifiersInSelected.bl_label, icon = 'FORCE_TURBULENCE')




classes = [
    ClearModifiers,
    ClearModifiersFromSelected,
    CrossCopyModifiersInSelected,
    BulkFCurveModsPanel,
]


def register():
    for __class in classes:
        bpy.utils.register_class(__class)

def unregister():
    for __class in classes:
        bpy.utils.unregister_class(__class)


if __name__ == "__main__":
    register()