import bpy
import math
from mathutils import Vector
from bpy.props import *
from bpy.types import Panel

# Global settings

# Light type settings
meshorlamp = False
lamptypes = (
    # Lamp types
    ("POINT", "Point", "Use Point light type", "LAMP_POINT", 0),
    ("SUN", "Sun", "Use Sun light type", "LAMP_SUN", 1),
    ("SPOT", "Spot", "Use Spot light type", "LAMP_SPOT", 2), 
    ("AREA", "Area", "Use Area light type", "LAMP_AREA", 3),
    # Mesh Types
    ("PLANE", "Plane", "Use Plane light type", "MESH_PLANE", 4),
    ("CIRCLE", "Circle", "Use Circle light type", "MESH_CIRCLE", 5),
    ("CUBE", "Cube", "Use Cube light type", "MESH_CUBE", 6),
    ("SPHERE", "Sphere", "Use Sphere light type", "MESH_UVSPHERE", 7),
    ("ICOSPHERE", "Icosphere", "Use Icosphere light type", "MESH_ICOSPHERE", 8),
    ("CAMERA", "Camera", "Use Camera light type", "CAMERA_DATA", 9)
    )

lamp_light = ["POINT", "SUN", "SPOT", "AREA"]
mesh_light = ["PLANE", "CIRCLE", "CUBE", "SPHERE", "ICOSPHERE"]
# Class to define properties
class LightCannonProperties(bpy.types.PropertyGroup):
    p = bpy.props

# UI Switches
    # mesh/lamp light objects
    lv_meshlight = p.BoolProperty(name="Mesh light", description="Mesh Based Light", default=False) 
    lv_lamptype = p.EnumProperty(name="Lamp Light Type", items=lamptypes, description="Choose which type of lamp light you want created", default='SPOT') # default 3/area
    lv_lightsize = p.FloatProperty(name="Light Size", min=0.0, max=10000.0, default=0.10, description="Size of the area of the created lamp") # light size
    lv_lightsizearea = p.FloatProperty(name="Area Light Size", min=0.0, max=10000.0, default=1.0, description="Size of the square area lamp") # square area light size
# Area Lamp
    lv_areatype = p.EnumProperty(name="Shape of Area Lamp", items=[('SQUARE', 'Square', 'Square area shape', 0), ('RECTANGLE', 'Rectangle', 'Recntangle area shape', 1)], description="Choose which type of lamp light you want created", default="SQUARE")
    lv_lightsizeY = p.FloatProperty(name="Light Size Y", min=0.0, max=10000.0, default=0.75, description="Size of the Y area of the created lamp") # light size 
# Spot lamp
    lv_spotsize = p.IntProperty(name="Spot Size", min=1, max=180, default=45, description="Size of the spot for the created lamp") # spot size 
    lv_spotblend = p.FloatProperty(name="Spot Blend", min=0.0, max=1.0, default=0.150, description="Softness of the spotlight edge") # spot blend 
    lv_spotshowcone = p.BoolProperty(name="Show Spot Cone", description="Show Spotlight cone", default=False) # custom mat
# Mesh Type props
    lv_meshradius = p.FloatProperty(name="Radius", min=0.0, max=1000000.0, default=1, description="The size/radius of created mesh") # light size 
    lv_meshcirclefill = p.EnumProperty(name="Fill type for circle", items=[('NGON', 'Ngon', 'Use Ngons', 0), ('TRIFAN', 'Trifan', 'Use Triangle fans', 1)], description="Choose the fill type for your circle", default="NGON")
    lv_meshverticies = p.IntProperty(name="Verticies", min=3, max=500, default=16, description="Amount of Verticies in mesh") # Verticies
    lv_meshsegments = p.IntProperty(name="Segments", min=3, max=500, default=32, description="Amount of Segments in sphere") # segments
    lv_meshringcount = p.IntProperty(name="Rings", min=3, max=500, default=16, description="Amount of Rings in sphere") # ring_count
    lv_meshsubdivisions = p.IntProperty(name="Subdivisions", min=1, max=8, default=2, description="Amount of Subdivisions in Icosphere") # subdivisions
# Materials ####
    lv_custom_mat = p.BoolProperty(name="Custom Material", description="Use an existing material", default=False) # custom mat
    lv_emissionstrength = p.FloatProperty(name="Light Strength", min=0.0, max=5000.0, default=1.0, description="Strength of the light") # light strength
    lv_emissioncolor = p.FloatVectorProperty(size=4, subtype="COLOR", default=(1.0, 1.0, 1.0, 1.0), min=0, max=1.0) # light color
    # Ray Visibility
    lv_raycamera = p.BoolProperty(name="Camera", description="Camera Ray Visibility", default=False) 
    lv_raydiffuse = p.BoolProperty(name="Diffuse", description="Diffuse Ray Visibility", default=True) 
    lv_rayglossy = p.BoolProperty(name="Glossy", description="Glossy Ray Visibility", default=True) 
    lv_raytransmission = p.BoolProperty(name="Transmission", description="Transmission Ray Visibility", default=True) 
    lv_rayshadow = p.BoolProperty(name="Shadow", description="Shadow Ray Visibility", default=True) 

############################    
## Draw Panel in Toolbar
############################
class addLightCannonPanel(Panel):
    bl_idname = "LIGHTCANNON_PT_lightCannonPanel"
    bl_label = "Light Cannon"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Light Cannon'
    bl_context = 'objectmode'

    def draw(self, context):
        props = bpy.context.window_manager.lightcannon
        layout = self.layout
        row = layout.row()
        row.prop(props, "lv_lamptype", text="Type")
        row = self.layout.row()
        # Make UI buttons show names
        # Find index of lv_lamptype selection, tuple wants number not string
        lamptypeindex = [icoLamptype for icoLamptype in lamptypes if props.lv_lamptype in icoLamptype][0][4]
        lightname = lamptypes[lamptypeindex][1] # name for lamp type.
        # icontype = lamptypes[lamptypeindex][3] # icon for lamp type.
        lighttext = "Create " + lightname + " Light!"
        # create operator button from custom icons
        row.operator("object.lightcannon", text=lighttext, icon="PLAY")
        row = layout.row()
        row.label(text="Settings") # sloppy to add space
        box = self.layout.box()
        col = box.column(align=True)
        col.label(text=lightname + " Options")
        # Spot
        if lightname == 'Spot':
            col = box.column()
            col.prop(props, "lv_lightsize", text="Light Size")
            col = box.column(align=True)
            col.label(text="Spot Settings")
            col.prop(props, "lv_spotsize", text="Spot Size")
            col.prop(props, "lv_spotblend", text="Blend")
            col.prop(props, "lv_spotshowcone", text="Show Cone")
        # Area
        elif lightname == 'Area':
            col = box.column(align=True)
            col.prop(props, "lv_areatype", text="")
            if props.lv_areatype == "SQUARE":
                col.prop(props, "lv_lightsizearea", text="Light Size")
            else:
                col.prop(props, "lv_lightsizearea", text="Light Size X")
                col.prop(props, "lv_lightsizeY", text="Light Size Y")
        # Point and Sun
        elif lightname in ['Point', 'Sun']:
            col = box.column()
            col.prop(props, "lv_lightsize", text="Light Size")
        # Mesh types
        # Plane
        elif lightname == "Plane":
            col = box.column(align=True)
            col.prop(props, "lv_meshradius", text="Radius")
        elif lightname == "Circle":
            col = box.column(align=True)
            col.prop(props, "lv_meshradius", text="Radius") # radius
            col.prop(props, "lv_meshverticies", text="Verticies") # verticies
            col.prop(props, "lv_meshcirclefill", text="Fill Type") # fill_type
        elif lightname == "Cube":
            col = box.column(align=True)
            col.prop(props, "lv_meshradius", text="Radius") # radius
        elif lightname == "Sphere":
            col = box.column(align=True)
            col.prop(props, "lv_meshradius", text="Radius") # radius
            col.prop(props, "lv_meshsegments", text="Segments") # segments
            col.prop(props, "lv_meshringcount", text="Ring Count") # ring_count
        elif lightname == "Ic":
            col = box.column(align=True)
            col.prop(props, "lv_meshradius", text="Radius") # radius
            # subdivisions
        elif lightname == "Camera":
            col = box.column(align=True)
            col.label(text="!!!WARNING!!!")
            col.label(text="NO LIGHT CREATED")
            col.label(text="WITH THIS OPTION!")

        # Material
        box = self.layout.box()
        row = box.row()
        row.label(text="Emission Settings")
        col = box.column(align=True)
        col.prop(props, "lv_emissioncolor", text="")
        col.prop(props, "lv_emissionstrength", text="Strength")

        # Ray visibility
        box = self.layout.box()
        col = box.column()
        col.label(text="Ray Visibility")
        row = box.row()
        row.prop(props, "lv_raycamera", text="Camera")
        row.prop(props, "lv_raydiffuse", text="Diffuse")
        row = box.row()
        row.prop(props, "lv_rayglossy", text="Glossy")
        row.prop(props, "lv_raytransmission", text="Transmission")
        row = box.row()
        row.prop(props, "lv_rayshadow", text="Shadow")

###################
# Make Tools

def node_output_clean(node_tree):
    # Clean nodes so just output
    nodes = node_tree.nodes
    for node in nodes:
        if not node.type == 'OUTPUT_MATERIAL':
            nodes.remove(node)
    return node_tree.nodes[0]

def addlightcannonmat(obj):
    props = bpy.context.window_manager.lightcannon
    # Create Material and use nodes
    material = bpy.data.materials.new(name='LightCannonMat')
    material.use_nodes = True
    node_tree = material.node_tree
    out_node = node_output_clean(node_tree) # Clean nodes
    emission = node_tree.nodes.new('ShaderNodeEmission') # New light shader
    node_tree.links.new(out_node.inputs[0], emission.outputs[0]) # Connect to output

    # Custom Settings
    material.diffuse_color = props.lv_emissioncolor # set viewport color
    emission.inputs['Color'].default_value = props.lv_emissioncolor
    emission.inputs['Strength'].default_value = props.lv_emissionstrength
    obj.data.materials.append(material)
    return {'FINISHED'}
    

###################
# Create Operator
class OBJECT_OT_makelight(bpy.types.Operator):
    bl_idname = "object.lightcannon"
    bl_label = "LightCannon"
    bl_description = "Create Light from current view"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        props = bpy.context.window_manager.lightcannon
        scn = bpy.context.scene

        origcam = scn.camera # remember original Camera
        bpy.ops.object.camera_add() # add new camera 
        coordcam = bpy.context.active_object # I'm the new view coordinate camera
        scn.camera = coordcam # now make me the active camera
        bpy.ops.view3d.camera_to_view() # now that I'm active, align me to the current view
        viewcoords = coordcam.location # get my coordinates coordinates
        # Add Object
        current_lightype = props.lv_lamptype
        
        # Add new lamp object with coordcam coordinates and aligned to view
        if current_lightype in lamp_light:
            bpy.ops.object.light_add(type=current_lightype, align="VIEW", location=viewcoords)
            newlight = bpy.context.active_object # I'm the new light
            newlight.color = props.lv_emissioncolor
            # newlight.data.node_tree.nodes['Emission'].inputs[0].default_value = props.lv_emissioncolor
            if current_lightype == "SPOT":
                newlight.data.shadow_soft_size = props.lv_lightsize
                newlight.data.spot_size = math.radians(props.lv_spotsize)
                newlight.data.spot_blend = props.lv_spotblend
                newlight.data.show_cone = props.lv_spotshowcone

            if current_lightype == "AREA":
                newlight.data.shape = props.lv_areatype
                newlight.data.size = props.lv_lightsizearea
                newlight.data.size_y = props.lv_lightsizeY
            
            else: # It's a point or sun which only have one option
                newlight.data.shadow_soft_size = props.lv_lightsize

        # Checking Mesh Types Now
        elif current_lightype in mesh_light:
            if current_lightype == "PLANE":
                bpy.ops.mesh.primitive_plane_add(align="VIEW", location=viewcoords)

            elif current_lightype == "CIRCLE":
                bpy.ops.mesh.primitive_circle_add(vertices=props.lv_meshverticies, radius=props.lv_meshradius, fill_type=props.lv_meshcirclefill, align="VIEW", location=viewcoords)

            elif current_lightype == "CUBE":
                bpy.ops.mesh.primitive_cube_add(align="VIEW", location=viewcoords)

            elif current_lightype == "SPHERE":
                bpy.ops.mesh.primitive_uv_sphere_add(segments=props.lv_meshsegments, ring_count=props.lv_meshringcount, size=props.lv_meshradius, align="VIEW", location=viewcoords)

            elif current_lightype == "ICOSPHERE":
                bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=props.lv_meshsubdivisions, align="VIEW", location=viewcoords)

            # Add Emission material to new mesh obj
            newlight = bpy.context.active_object # I'm the new light
            addlightcannonmat(newlight)

            # Set custom Ray Visibility
            raylight = newlight.cycles_visibility

            raylight.camera = props.lv_raycamera
            raylight.diffuse = props.lv_raydiffuse
            raylight.glossy = props.lv_rayglossy
            raylight.transmission = props.lv_raytransmission
            raylight.shadow = props.lv_rayshadow

        # Done with coord camera, first unselect all, then reselect and delete
        if current_lightype != "CAMERA":
            bpy.ops.object.select_all() # deselect all
            coordcam.select_set(True) # Select coordcam, don't need it
            bpy.ops.object.delete() # Delete coordcam, we'll miss you.
            scn.camera = origcam # set original camera as active again
        else:
            newlight = bpy.context.active_object
        newlight.select_set(True) # Select newlight

        # Add Newly created object to LightCannon Collection
        lc_collection = bpy.data.collections.keys()
        if 'LightCannon' not in lc_collection: # Check if it exists
            mycol=bpy.data.collections.new(name="LightCannon") # Make the collection
            bpy.context.scene.collection.children.link(mycol) # Link it to the Master Collection so it shows up
        
        bpy.ops.collection.objects_remove_active() # Remove this new object from any collections it might be in

        bpy.data.collections["LightCannon"].objects.link(newlight) # Link new object to LightCannon collection
        # bpy.context.scene.collection.objects.unlink(newlight) # Unlink from scene collection
        
        return {'FINISHED'} # operator worked! 