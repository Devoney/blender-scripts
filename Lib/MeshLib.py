import bpy
from mathutils import Vector

def cube(size, **kwargs):
    location = None
    if 'location' in kwargs:
        location = kwargs['location']
    if location is None:
        location = (0, 0, 0)
    
    bpy.ops.mesh.primitive_cube_add(size=1, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, 1))
    cube = bpy.context.object
    if 'name' in kwargs is not None:
        cube.name = kwargs['name']
    cube.dimensions = Vector(size)
    return cube

def cylinder(radius, depth, vertices=32, location = None):
    if location is None:
        location = (0, 0, 0)
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, enter_editmode=False, align='WORLD', location=location, scale=(1, 1, 1))
    return bpy.context.object

def icosphere(radius, **kwargs):
    bpy.ops.mesh.primitive_ico_sphere_add(
        radius=radius,
        subdivisions=1,
        enter_editmode=False,
        align='WORLD',
        location=(0, 0, 0), 
        scale=(1, 1, 1)
    )

    icosph = bpy.context.object

    if 'name' in kwargs is not None:
        icosph.name = kwargs['name']

    return icosph
