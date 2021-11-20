import bpy
import copy
import ObjectLib
import SceneLib

def mirror(obj, axis, apply=True):
  axisIndex = bytes(axis, 'ascii')[0] - 120
  loc = copy.deepcopy(obj.location)
  half = obj.dimensions[axisIndex] / 2
  loc[axisIndex] = loc[axisIndex] + half
  SceneLib.setCursor(loc.x, loc.y, loc.z)

  ObjectLib.selectObject(obj)
  bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
  mirrorModifier = obj.modifiers.new(name='Mirror', type='MIRROR')
  mirrorModifier.use_axis[2] = True
  if apply:
    bpy.ops.object.modifier_apply(modifier=mirrorModifier.name)
    return None
  else:
    return mirrorModifier

def solidify(obj, thickness):
  modifier = obj.modifiers.new(name='SOLIDIFY', type='SOLIDIFY')
  modifier.thickness = thickness
  modifier.offset = 0