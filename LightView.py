import bpy
print("RUN")
# Let's create some functions
def lampfromview(coords):
    bpy.ops.object.lamp_add(type='AREA', view_align=True, location=coords)
    lamp = bpy.context.active_object
    # lamp.location = coords

############################    
## Draw Panel in Toolbar
############################
class addLightViewPanel(bpy.types.Panel):
    bl_label = "LightView"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_context = 'objectmode'

    def draw(self, context):
        layout = self.layout
        row = self.layout.row()
        row.label(text="LightView")
        row.operator("object.lightview", text="Run!", icon="PLAY")

# Create Operator
class OBJECT_OT_makelight(bpy.types.Operator):
    bl_idname = "object.lightview"
    bl_label = "LightView"
    bl_description = "Create Light from current view"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        scn = bpy.context.screen.scene
        #find current active camera and create variable
        origcam = scn.camera

        # add new camera and make it active
        bpy.ops.object.camera_add()
        coordcam = bpy.context.active_object
        scn.camera = coordcam
        # set camera to view
        bpy.ops.view3d.camera_to_view()
        # get camera location coordinates
        viewcoords = coordcam.location
        # Add new lamp object with camera coordinates and aligned to view
        lampfromview(viewcoords)

        # Done with coord camera, reselect and delete
        # Unselect all
        bpy.ops.object.select_all()
        # Select coordcam
        coordcam.select = True
        # Delete coord camera
        bpy.ops.object.delete()

        # set original camera as active again
        scn.camera = origcam
        return {'FINISHED'} # operator worked 

### Define Classes to register
classes = [addLightViewPanel, OBJECT_OT_makelight]

def register():
    for c in classes:
        bpy.utils.register_class(c)
    # bpy.types.WindowManager.curve_tracer = bpy.props.PointerProperty(type=TracerProperties)
def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    # del bpy.types.WindowManager.curve_tracer
if __name__ == "__main__":
    register()