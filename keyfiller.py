import bpy

bl_info = {
    "name": "Keyfiller",
    "author": "crab emoji",
    "version": (0, 2),
    "blender": (3, 6, 2),
    "location": "Dope Sheet > Key > Keyfill",
    "description": "Inserts keyframes on all channels for every keyframe on any other channel",
    #"warning": " is mye fist adon",
    #"doc_url": "",
    "category": "Animation",
}



class KEYCHOOSER_MT(bpy.types.Operator):
    """Select only keyframes on certain timings (2's, 3's, etc.)"""
    bl_idname = "keyfiller.keychooser"
    bl_label = "Keychoose"
    bl_options = {'REGISTER', 'UNDO'}
    
    count_x: bpy.props.IntProperty(
        name = "Every X frames",
        description = "Select only every Xth frame",
        default = 2
    )
    offset_x: bpy.props.IntProperty(
        name = "Offset",
        description = "Starting frame",
        default = 0
    )
    deselect_instead: bpy.props.BoolProperty(
        name = "Invert selection",
        description = "Deselects every Xth frame",
        default = False
    )
    
    def execute(self, context):
        bpy.context.area.type = 'DOPESHEET_EDITOR'
        
        # 1. Remember the current frame & deselect all keyframes
        _current_frame_prev = context.scene.frame_current
        _action = 'DESELECT'
        bpy.ops.action.select_all(action = _action)
        
        # 2. Select keyframes on current frame once every X frames
        X = self.count_x
        frame_start = context.scene.frame_start + self.offset_x
        for frame in range(frame_start, context.scene.frame_end + 1):
            X += 1
            
            if not self.deselect_instead:
                if X >= self.count_x:
                    frame_select_current(context, frame)
                    
                    X = 0
            else:
                if X < self.count_x:
                    frame_select_current(context, frame)
                else:
                    X = 0
                
        
        bpy.ops.screen.frame_current = _current_frame_prev
        
        return {'FINISHED'}
    
    def menu_item(self, context):
        self.layout.operator(KEYCHOOSER_MT.bl_idname, icon='ACTION_TWEAK')
        
def frame_select_current(context, frame):
    context.scene.frame_current = frame
    _mode = 'CFRA'
    bpy.ops.action.select_column(mode = _mode)


class KEYFILLER_MT(bpy.types.Operator):
    """For every keyframe on any channel, inserts a keyframe on all channels"""
    bl_idname = "keyfiller.keyfill"
    bl_label = "Keyfill"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        
        ## 0. Remember the hidden channels & current frame
        _visible_channels_prev = context.visible_fcurves #context.active_action.fcurves
        _current_frame_prev = context.scene.frame_current
        
        ## 1. Unhide all channels
        for __channel in context.active_action.fcurves:
            __channel.hide = False
            
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
        
        ## 4. Hide all previously hidden channels
        for __channel in context.active_action.fcurves:
            if __channel not in _visible_channels_prev:
                __channel.hide = True
        
        return {'FINISHED'}
    
    def menu_item(self, context):
        self.layout.separator()
        self.layout.operator(KEYFILLER_MT.bl_idname, icon='MOD_HUE_SATURATION')
    




classes = {
    KEYFILLER_MT,
    KEYCHOOSER_MT
}

def register():
    for _class in classes:
        bpy.utils.register_class(_class)
        
        if (callable(_class.menu_item)):
            bpy.types.DOPESHEET_MT_key.append(_class.menu_item)

def unregister():
    for _class in classes:
        bpy.utils.unregister_class(_class)
        
        if (callable(_class.menu_item)):
            bpy.types.DOPESHEET_MT_key.remove(_class.menu_item)

if __name__ == "__main__":
    register()