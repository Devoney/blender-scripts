import bpy
import ObjectLib
import os

def export(obj, useSceneUnit=False, globalScale=1):
  ObjectLib.selectObject(obj)
  filepath = os.path.dirname(bpy.data.filepath) + '\\Output\\' + obj.name + '.stl'
  bpy.ops.export_mesh.stl(
    filepath=filepath, 
    check_existing=True, 
    filter_glob='*.stl', 
    use_selection=True, 
    global_scale=globalScale, 
    use_scene_unit=useSceneUnit, 
    ascii=False, 
    use_mesh_modifiers=True, 
    batch_mode='OFF', 
    axis_forward='Y', 
    axis_up='Z'
  )
  return filepath