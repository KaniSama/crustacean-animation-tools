import bpy
from bpy.props import (
    BoolProperty,
    PointerProperty,
)
from bpy.types import (
    PropertyGroup,
    AddonPreferences,
)


bl_info = {
    "name": " 🦀 Crustacean Animation Toolset 🦀",
    "author": "crab emoji 🦀",
    "version": (0, 0, 2),
    "blender": (3, 6, 2),
    "location": "?",
    "description": "Adds workflow improvements for some very specific animation needs.",
    "warning": "Inividual modules lack proper testing, may cause problems",
    "wiki_url":    "https://github.com/KaniSama/crustacean-animation-tools/blob/main/README.md",
    "tracker_url": "https://github.com/KaniSama/crustacean-animation-tools/issues",
    "category": "Animation",
}


sub_modules_names = (
    "keyframe_pies",
    "keyfiller",
    "cls_setup_char",
)


sub_modules = [__import__(__package__ + "." + submod, {}, {}, submod) for submod in sub_modules_names]
sub_modules.sort(key=lambda mod: (mod.bl_info['category'], mod.bl_info['name']))


def _get_pref_class(mod):
    import inspect

    for obj in vars(mod).values():
        if inspect.isclass(obj) and issubclass(obj, PropertyGroup):
            if hasattr(obj, 'bl_idname') and obj.bl_idname == mod.__name__:
                return obj


def get_addon_preferences(name=''):
    """Acquisition and registration"""
    addons = bpy.context.preferences.addons
    if __name__ not in addons:  # wm.read_factory_settings()
        return None
    addon_prefs = addons[__name__].preferences
    if name:
        if not hasattr(addon_prefs, name):
            for mod in sub_modules:
                if mod.__name__.split('.')[-1] == name:
                    cls = _get_pref_class(mod)
                    if cls:
                        prop = PointerProperty(type=cls)
                        create_property(CrustaceanAnimationPrefs, name, prop)
                        bpy.utils.unregister_class(CrustaceanAnimationPrefs)
                        bpy.utils.register_class(CrustaceanAnimationPrefs)
        return getattr(addon_prefs, name, None)
    else:
        return addon_prefs


def create_property(cls, name, prop):
    if not hasattr(cls, '__annotations__'):
        cls.__annotations__ = dict()
    cls.__annotations__[name] = prop


def register_submodule(mod):
    mod.register()
    mod.__addon_enabled__ = True


def unregister_submodule(mod):
    if mod.__addon_enabled__:
        mod.unregister()
        mod.__addon_enabled__ = False

        prefs = get_addon_preferences()
        name = mod.__name__.split('.')[-1]
        if hasattr(CrustaceanAnimationPrefs, name):
            delattr(CrustaceanAnimationPrefs, name)
            if prefs:
                bpy.utils.unregister_class(CrustaceanAnimationPrefs)
                bpy.utils.register_class(CrustaceanAnimationPrefs)
                if name in prefs:
                    del prefs[name]




#
# Preference settings
#




class OpenDocsOperator(bpy.types.Operator):
    """Open a web browser window with the documentation for the add-on"""
    bl_idname = "cat.opendocs"
    bl_label = "Open Documentation"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        bpy.ops.wm.url_open(url='https://github.com/KaniSama/crustacean-animation-tools/blob/main/README.md')
        
        return {"FINISHED"}



class CrustaceanAnimationPrefs(AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        
        layout.operator("cat.opendocs", text='Open Documentation', icon="HELP")

        for mod in sub_modules:
            mod_name = mod.__name__.split('.')[-1]
            info = mod.bl_info
            column = layout.column()
            box = column.box()

            # first stage
            expand = getattr(self, 'show_expanded_' + mod_name)
            icon = 'TRIA_DOWN' if expand else 'TRIA_RIGHT'
            col = box.column()
            row = col.row()
            sub = row.row()
            sub.context_pointer_set('addon_prefs', self)
            op = sub.operator('wm.context_toggle', text='', icon=icon,
                              emboss=False)
            op.data_path = 'addon_prefs.show_expanded_' + mod_name
            sub.label(text='{}: {}'.format(info['category'], info['name']))
            sub = row.row()
            sub.alignment = 'RIGHT'
            if info.get('warning'):
                sub.label(text='', icon='ERROR')
            sub.prop(self, 'use_' + mod_name, text='')

            # The second stage
            if expand:
                if info.get('description'):
                    split = col.row().split(factor=0.15)
                    split.label(text='Description:')
                    split.label(text=info['description'])
                if info.get('location'):
                    split = col.row().split(factor=0.15)
                    split.label(text='Location:')
                    split.label(text=info['location'])
                """
                if info.get('author'):
                    split = col.row().split(factor=0.15)
                    split.label(text='Author:')
                    split.label(text=info['author'])
                """
                if info.get('version'):
                    split = col.row().split(factor=0.15)
                    split.label(text='Version:')
                    split.label(text='.'.join(str(x) for x in info['version']),
                                translate=False)
                if info.get('warning'):
                    split = col.row().split(factor=0.15)
                    split.label(text='Warning:')
                    split.label(text='  ' + info['warning'], icon='ERROR')

                tot_row = int(bool(info.get('doc_url')))
                if tot_row:
                    split = col.row().split(factor=0.15)
                    split.label(text='Internet:')
                    if info.get('doc_url'):
                        op = split.operator('wm.url_open',
                                            text='Documentation', icon='HELP')
                        op.url = info.get('doc_url')
                    for i in range(4 - tot_row):
                        split.separator()

                # Details and settings
                if getattr(self, 'use_' + mod_name):
                    prefs = get_addon_preferences(mod_name)

                    if prefs and hasattr(prefs, 'draw'):
                        box = box.column()
                        prefs.layout = box
                        try:
                            prefs.draw(context)
                        except:
                            import traceback
                            traceback.print_exc()
                            box.label(text='Error (see console)', icon='ERROR')
                        del prefs.layout

        row = layout.row()
        row.label(text="Module settings are applied after program restart", icon="FILE_PARENT")


for mod in sub_modules:
    info = mod.bl_info
    mod_name = mod.__name__.split('.')[-1]

    def gen_update(mod):
        def update(self, context):
            enabled = getattr(self, 'use_' + mod.__name__.split('.')[-1])
            if enabled:
                register_submodule(mod)
            else:
                unregister_submodule(mod)
            mod.__addon_enabled__ = enabled
        return update

    create_property(
        CrustaceanAnimationPrefs,
        'use_' + mod_name,
        BoolProperty(
            name=info['name'],
            description=info.get('description', ''),
            update=gen_update(mod),
            default=True,
        ))

    create_property(
        CrustaceanAnimationPrefs,
        'show_expanded_' + mod_name,
        BoolProperty())


classes = (
    OpenDocsOperator,
    CrustaceanAnimationPrefs,
)

        
        
        
        
#
# Registration
#





def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    prefs = get_addon_preferences()
    for mod in sub_modules:
        if not hasattr(mod, '__addon_enabled__'):
            mod.__addon_enabled__ = False
        name = mod.__name__.split('.')[-1]
        if getattr(prefs, 'use_' + name):
            register_submodule(mod)


def unregister():
    for mod in sub_modules:
        if mod.__addon_enabled__:
            unregister_submodule(mod)

    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
