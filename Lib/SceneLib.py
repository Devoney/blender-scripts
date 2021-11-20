import bpy

def setCursor(x, y, z):
  cursor = bpy.context.scene.cursor
  cursor.location[0] = x
  cursor.location[1] = y
  cursor.location[2] = z

def editMode():
  bpy.ops.object.mode_set(mode='EDIT')

def objectMode():
  bpy.ops.object.mode_set(mode='OBJECT')

def findObject(name):
  return bpy.data.objects[name]

def findObjects(nameStartsWith):
  objs = []
  for obj in bpy.data.objects:
    if obj.name.startswith(nameStartsWith):
      objs.append(obj)
  return objs

def useMillimeterScale():
  bpy.context.scene.unit_settings.scale_length = 0.001

def showIndicesOfSelected():
  bpy.context.preferences.view.show_developer_ui = True
  bpy.context.space_data.overlay.show_extra_indices = True