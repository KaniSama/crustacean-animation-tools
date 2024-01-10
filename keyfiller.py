import bpy

bl_info = {
    "name": "Keyfiller",
    "author": "crab emoji",
    "version": (0, 1),
    "blender": (3, 6, 2),
    "location": "Dope Sheet > Key > Keyfill",
    "description": "Inserts keyframes on all channels for every keyframe on any other channel",
    #"warning": " is mye fist adon",
    #"doc_url": "",
    "category": "Animation",
}




class KEYFILLER_MT(bpy.types.Operator):
    """For every keyframe on any channel, inserts a keyframe on all channels"""
    bl_idname = "keyfiller.keyfill"
    bl_label = "Keyfill"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        # TODO : THIS WHOLE BIT ->
        ## -1. ?? Remember the hidden channels & current frame
        _visible_channels_prev = context.visible_fcurves #context.active_action.fcurves
        _current_frame_prev = context.scene.frame_current
        ## 0. ?? Unhide all channels
        for __channel in context.active_action.fcurves:
            __channel.hide = False
        ## 1. Get all keyframes
        ## 2. Iterate over all existing keyframes. Insert a keyframe for all channels where there's a keyframe on any channel.
        bpy.ops.screen.frame_jump(end = False)
        bpy.ops.screen.keyframe_jump(next = False)
        
        while True:
            __result = bpy.ops.screen.keyframe_jump(next = True)
            
            if __result != {"FINISHED"}:
                break
            
            bpy.ops.action.keyframe_insert(type='ALL')
                
        ## 3. Return the caret to the original position
        context.scene.frame_set(_current_frame_prev)
        ## 4. ?? Hide all previously hidden channels
        for __channel in context.active_action.fcurves:
            if __channel not in _visible_channels_prev:
                __channel.hide = True
        
        return {'FINISHED'}
    
    def menu_item(self, context):
        self.layout.separator()
        self.layout.operator(KEYFILLER_MT.bl_idname, icon='MOD_HUE_SATURATION')
    




classes = {
    KEYFILLER_MT
}

def register():
    for _class in classes:
        bpy.utils.register_class(_class)
        
        if (callable(_class.menu_item)):
            bpy.types.DOPESHEET_MT_key.append(_class.menu_item)

def unregister():
    for _class in classes:
        bpy.utils.register_class(_class)
        
        if (callable(_class.menu_item)):
            bpy.types.DOPESHEET_MT_key.remove(_class.menu_item)

if __name__ == "__main__":
    register()