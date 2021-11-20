import bpy
import MathLib
from mathutils import Vector


def applyAllTransformations(obj):
    selectObject(obj)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)


def centerOrigin(obj, mode=None):
    if mode is None:
        mode = 'MEDIAN'  # Could also be BOUNDS
    selectObject(obj)
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center=mode)

def getObject(name):
    return bpy.data.objects[name]

def clone(obj, linked=False, name=None):
    selectObject(obj)
    bpy.ops.object.duplicate_move(
        OBJECT_OT_duplicate={
            "linked": linked,
            "mode": 'TRANSLATION'
        },
        TRANSFORM_OT_translate={
            "value": (0, 0, 0),
            "orient_type": 'GLOBAL',
            "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            "orient_matrix_type": 'GLOBAL',
            "constraint_axis": (False, False, False),
            "mirror": True,
            "use_proportional_edit": False,
            "proportional_edit_falloff": 'SMOOTH',
            "proportional_size": 1,
            "use_proportional_connected": False,
            "use_proportional_projected": False,
            "snap": False,
            "snap_target": 'CLOSEST',
            "snap_point": (0, 0, 0),
            "snap_align": False,
            "snap_normal": (0, 0, 0),
            "gpencil_strokes": False,
            "cursor_transform": False,
            "texture_space": False,
            "remove_on_cancel": False,
            "release_confirm": False,
            "use_accurate": False,
            "use_automerge_and_split": False
        }
    )

    if name is not None:
        bpy.context.object.name = name

    return bpy.context.object


def delete(obj):
    selectObject(obj)
    deleteSelected()


def deleteAll():
    selectAll()
    deleteSelected()


def deleteSelected():
    bpy.ops.object.delete(use_global=False)


def deselectAll():
    bpy.ops.object.select_all(action='DESELECT')


def resetRotation(obj):
    rot = MathLib.degreesToEuler(Vector((0, 0, 0)))
    obj.rotation_euler = rot


def rotate(obj, xyz):
    rot = MathLib.degreesToEuler(Vector(xyz))
    obj.rotation_euler = rot
    selectObject(obj)
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)


def scale(obj, xyz):
    x = obj.dimensions.x * xyz[0]
    y = obj.dimensions.y * xyz[1]
    z = obj.dimensions.z * xyz[2]
    obj.dimensions = Vector((x, y, z))


def selectAll():
    bpy.ops.object.select_all(action='SELECT')


def translate(obj, xyz):
    x = xyz[0]
    y = xyz[1]
    z = xyz[2]

    x = x + obj.location.x
    y = y + obj.location.y
    z = z + obj.location.z

    obj.location = Vector((x, y, z))


def selectObject(obj):
    deselectAll()
    if type(obj) is str:
        obj = getObject(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    

def selectObjects(objs):
    deselectAll()
    lastObj = None
    for obj in objs:
        obj.select_set(True)
        lastObj = obj
    bpy.context.view_layer.objects.active = lastObj


def joinObjects(objs, name=''):
    selectObjects(objs)
    bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    if name != '':
        obj.name = name
    return obj


def getBoundingBoxOfObjects(objects):
    class BoundingBox():
        minimum = Vector((0,0,0))
        maximum = Vector((0,0,0))

    boundingBox = BoundingBox()
    isSet = False
    for obj in objects:
        if not isSet:
            boundingBox.minimum.x = obj.location.x
            boundingBox.minimum.y = obj.location.y
            boundingBox.minimum.z = obj.location.z

            boundingBox.maximum.x = obj.location.x + obj.dimensions.x
            boundingBox.maximum.y = obj.location.y + obj.dimensions.y
            boundingBox.maximum.z = obj.location.z + obj.dimensions.z
        else:
            boundingBox.minimum.x = min(boundingBox.minimum.x, obj.location.x)
            boundingBox.minimum.y = min(boundingBox.minimum.y, obj.location.y)
            boundingBox.minimum.z = min(boundingBox.minimum.z, obj.location.z)

            boundingBox.maximum.x = max(boundingBox.maximum.x, obj.location.x + obj.dimensions.x)
            boundingBox.maximum.y = max(boundingBox.maximum.y, obj.location.y + obj.dimensions.y)
            boundingBox.maximum.z = max(boundingBox.maximum.z, obj.location.z + obj.dimensions.z)
        isSet = True
    
    return boundingBox