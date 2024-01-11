import bpy

bl_info = {
    "name": "CLS Setup Character",
    "author": "crab emoji",
    "version": (0, 1),
    "blender": (3, 6, 2),
    "location": "Dope Sheet > Key > Set up for simulation",
    "description": "Automates setting an initial position for a given character rig",
    "category": "Animation",
}




class CLS_SETUP_CHAR_MT(bpy.types.Operator):
    """Creates initial keyframes for a given character rig"""
    bl_idname = "cls.setup_char"
    bl_label = "Set up for simulation"
    bl_options = {'REGISTER', 'UNDO'}
    
    # Property determines whether the Root bone is included in the keyframe insertion
    include_root: bpy.props.BoolProperty(default = False)
    # Determines which frame to set the keyframes on
    frame_to_key: bpy.props.IntProperty(default = bpy.context.scene.frame_start - 100)
    # Determines which bone is the Root (if it's included)
    root_bone_name: bpy.props.StringProperty(default = "P-root")
    
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def draw(self, context):
        row = self.layout
        row.prop(self, "frame_to_key", text="Set keyframes on frame:")
        row.prop(self, "include_root", text="Also set keyframe for the Root bone")
        if self.include_root:
            row.prop(self, "root_bone_name", text="Root bone")
        
    
    def execute(self, context):
        
        # 1. Get the mode we're in
        _current_mode = context.mode
        
        # 2. Enable Pose Mode
        if _current_mode != 'POSE':
            bpy.ops.object.mode_set(mode='POSE')
        
        # 3. Remember current frame
        _current_frame = context.scene.frame_current
        
        # 4. Move to Frame1 and calculate Frame1 - 100
        bpy.ops.screen.frame_jump(end = False)
        context.scene.frame_set(context.scene.frame_current - 100)
        
        if context.scene.frame_current < 0:
            self.report(type = {'ERROR'}, message = 'Animation needs to start at least on frame 100 !')
            context.scene.frame_set(_current_frame)
            return {'CANCELLED'}
        
        # 5. Select all bones & reset their properties
        bpy.ops.pose.select_all(action='SELECT')
        
        if not self.include_root:
            __root_bone = bpy.context.object.pose.bones.get("Root")
            if __root_bone:
                __root_bone.bone.select = False
        
        bpy.ops.pose.rot_clear()
        bpy.ops.pose.scale_clear()
        bpy.ops.pose.transforms_clear()
        
        # 6. Insert keyframe on all channels
        bpy.ops.action.keyframe_insert(type='ALL')
        
        # 7. Set caret to where it was previously
        context.scene.frame_set(_current_frame)
        
        return {"FINISHED"}
    
    def menu_item(self, context):
        self.layout.separator()
        self.layout.operator_context = 'INVOKE_DEFAULT' #'INVOKE_AREA'
        self.layout.operator(CLS_SETUP_CHAR_MT.bl_idname, icon='CON_ARMATURE')




classes = {
    CLS_SETUP_CHAR_MT,
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