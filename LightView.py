import bpy
from bpy.props import *

# Global settings

# Light type settings
meshorlamp = False
meshtypes = (
    # Mesh Types
    ("PLANE", "Area", "Use Area light type", "LAMP_AREA", 0),
    ("BOX", "Area", "Use Area light type", "LAMP_AREA", 1),
    ("SPHERE", "Area", "Use Area light type", "LAMP_AREA", 2),
    ("ICOSPHERE", "Area", "Use Area light type", "LAMP_AREA", 3)
    )
lamptypes = (
    # Lamp types
    ("POINT", "Point", "Use Point light type", "LAMP_POINT", 0),
    ("SUN", "Sun", "Use Sun light type", "LAMP_SUN", 1),
    ("SPOT", "Spot", "Use Spot light type", "LAMP_SPOT", 2), 
    ("AREA", "Area", "Use Area light type", "LAMP_AREA", 3),
    ("HEMI", "Hemi", "Use Hemi light type", "LAMP_HEMI", 4)
    )

# Class to define properties
class LightViewProperties(bpy.types.PropertyGroup):
    p = bpy.props
    options = bpy.props.BoolProperty(name="Options", description="Additional option", default=False)
    meshorlamp = bpy.props.BoolProperty(name="Mesh light", description="Mesh Based Light", default=False) # mesh or lamp object

    lv_meshtype = p.EnumProperty(name="Light Type", items=meshtypes, description="Choose which type of light you want created", default="AREA")

    lv_lampsize = p.FloatProperty(name="Light Size", min=0.0, max=100.0, default=0.10, description="Size of the area of the created lamp") # lamp size 
    lv_custom_mat = bpy.props.BoolProperty(name="Custom Material", description="Use an existing material", default=False) # custom mat
    lv_lightstrength = p.FloatProperty(name="Light Strength", min=0.0, max=5000.0, default=1.0, description="Strength of the light") # light strength
    # light color

############################    
## Draw Panel in Toolbar
############################
class addLightViewPanel(bpy.types.Panel):
    bl_label = "LightView"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = 'objectmode'

    def draw(self, context):
        search_props = bpy.context.window_manager.lightview
        layout = self.layout
        row = self.layout.row()
        # Find index of lv_lamptype selection, tuple wants number not string
        lamptypeindex = [icoLamptype for icoLamptype in lamptypes if search_props.lv_lamptype in icoLamptype][0][4]
        icontype = lamptypes[lamptypeindex][3] # icon for lamp type.
        row.operator("object.lightview", text="Add Light!", icon=icontype) # Run the lightview operator
        col = layout.column()
        col.label("Light Type")
        row = layout.row()
        row.prop(search_props, "lv_lamptype", text="")
        row.prop(search_props, "options", icon="SCRIPTPLUGINS") # Show/Hide Option
        row = self.layout.row()
        if search_props.options:
            col = layout.column()
            col.label("Light settings")
            

# Create Operator
class OBJECT_OT_makelight(bpy.types.Operator):
    bl_idname = "object.lightview"
    bl_label = "LightView"
    bl_description = "Create Light from current view"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        search_props = bpy.context.window_manager.lightview
        scn = bpy.context.screen.scene

        origcam = scn.camera # remember original Camera
        bpy.ops.object.camera_add() # add new camera 
        coordcam = bpy.context.active_object # I'm the new view coordinate camera
        scn.camera = coordcam # now make me the active camera
        bpy.ops.view3d.camera_to_view() # now that I'm active, align me to the current view
        viewcoords = coordcam.location # get my coordinates coordinates

        # Add new lamp object with coordcam coordinates and aligned to view
        bpy.ops.object.lamp_add(type=search_props.lv_lamptype, view_align=True, location=viewcoords)
        newlight = bpy.context.active_object # I'm the new light
        # Done with coord camera, first unselect all, then reselect and delete
        bpy.ops.object.select_all() # deselect
        coordcam.select = True # Select coordcam
        bpy.ops.object.delete() # Delete coord camera
        scn.camera = origcam # set original camera as active again
        newlight.select = True # Select newlight
        return {'FINISHED'} # operator worked! 

### Wrap this baby up, define Classes to register
classes = [
    LightViewProperties, 
    addLightViewPanel, 
    OBJECT_OT_makelight
    ]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.WindowManager.lightview = bpy.props.PointerProperty(type=LightViewProperties)
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.WindowManager.lightview
if __name__ == "__main__":
    register()