bl_info = {
    "name": "Keyframe Pies",
    "author": "crab emoji",
    "version": (0, 5),
    "blender": (3, 6, 2),
    "location": "Hold I for pie :P",
    "description": "Replaces the old keyframe insertion menu with a stylish pie menu.",
    "warning": " is mye fist adon",
    "doc_url": "",
    "category": "Animation",
}

import bpy
from bpy.types import Menu






def set_keybinds():
    # handle the keymap
    wm = bpy.context.window_manager
    
    # Remake the old mapping to trigger on "Release"
    kc = wm.keyconfigs.active
    _keybind = "I"
    if kc:
        km = kc.keymaps.find(name="Pose")
        kmis = km.keymap_items
        kmi = kmis.find_from_operator(idname="anim.keyframe_insert_menu")
        kmi.value = "RELEASE"
        _keybind = kmi.type
        #km.restore_item_to_default(kmi)
    
    # Add the new keymap
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new(name='Pose')
        kmi = km.keymap_items.new('wm.call_menu_pie', _keybind, 'CLICK_DRAG')
        kmi.properties.name = "VIEW_3D_PIE_KeyframePie"
        addon_keymaps.append((km, kmi))




#############################################################   CLASSES



class VIEW_3D_PIE_KeyframePie(Menu):
    # label is displayed at the center of the pie menu.
    bl_label = "Insert Keyframe..."

    def draw(self, context):
        layout = self.layout

        pie = layout.menu_pie()
        # 4 - LEFT
#        pie.operator('anim.keyframe_insert_by_name', text="Loc + Rot + Scale", icon='BONE_DATA').type = 'LocRotScale'
        box = pie.split().column()
        box.operator('anim.keyframe_insert_by_name', text="Location", icon='ORIENTATION_LOCAL').type = 'Location'
        box.operator('anim.keyframe_insert_by_name', text="Rotation", icon='ORIENTATION_GIMBAL').type = 'Rotation'
        box.operator('anim.keyframe_insert_by_name', text="Scale", icon='OBJECT_HIDDEN').type = 'Scaling'
        # 6 - RIGHT
        pie.operator('anim.keyframe_insert_by_name', text="Whole Character", icon='POSE_HLT').type = 'WholeCharacter'
        # 2 - BOTTOM
        pie.operator('anim.keyframe_insert_by_name', text="Loc + Rot + Scale", icon='BONE_DATA').type = 'LocRotScale'
        # 8 - TOP
        pie.operator('anim.keyframe_insert_by_name', text="Available", icon='DOT').type = 'Available'
        
        # 7 - TOP - LEFT
#        pie.operator('anim.keyframe_insert_by_name', text="Location", icon='ORIENTATION_LOCAL').type = 'Location'
        # 9 - TOP - RIGHT
        
        # 1 - BOTTOM - LEFT
        
        # 3 - BOTTOM - RIGHT
        

class VIEW_3D_PANEL_ResetKeybindsPanel(bpy.types.Panel):
    """This panel will have a button to reset the keybinds
        because they don't seem to persist through program close/open"""
    bl_label = "Keyframe Pies"
    bl_idname = "panel.VIEW_3D_PANEL_ResetKeybindsPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Start add-on")

        row = layout.row()
        row.operator("kfp.reset_keybinds", icon='ACTION')
    

class VIEW_3D_PANEL_ResetKeybinds(bpy.types.Operator):
    """Set the keybind for KeyframePies again"""
    bl_idname = "kfp.reset_keybinds"
    bl_label = "Start add-on"
    
    def execute(self, context):
        set_keybinds()
        
        return {'FINISHED'}






############################################################# REGISTERING


classes = {
    VIEW_3D_PIE_KeyframePie,
    VIEW_3D_PANEL_ResetKeybindsPanel,
    VIEW_3D_PANEL_ResetKeybinds
}

# store keymaps here to access after registration
addon_keymaps = []



def register():
    
    for _class in classes:
        bpy.utils.register_class(_class)

    set_keybinds()
        


def unregister():
    
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
    
    # Restore the previous keybind to its original value
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.active
    if kc:
        km = kc.keymaps.find(name="Pose")
        kmis = km.keymap_items
        kmi = kmis.find_from_operator(idname="anim.keyframe_insert_menu")
        km.restore_item_to_default(kmi)
    
    # unregister
    bpy.utils.unregister_class(VIEW_3D_PANEL_ResetKeybindsPanel)
    bpy.utils.unregister_class(VIEW_3D_PIE_KeyframePie)
    
    for _class in classes:
        bpy.utils.register_class(_class)



if __name__ == "__main__":
    register()
    
#    bpy.ops.wm.call_menu_pie(name='VIEW_3D_PIE_KeyframePie')