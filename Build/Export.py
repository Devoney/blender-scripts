import bpy;
from inspect import getmembers
from pprint import pprint
from enum import Enum
import os

class Quality(Enum):
    Low = 0
    Medium = 1
    High = 2
    Ultra = 3
    
def hasSubdivisionModifier(obj):
    return 'Subdivision' in obj.modifiers

def ensure_dir(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def dump(obj):
    pprint(getmembers(obj))

collectionNames = ['MyCollection', 'Collection 3']
exportDir = bpy.path.abspath("//Export\\")
qualityLevels = [Quality.Low, Quality.Medium, Quality.High]    

for collectionName in collectionNames:
    objectsInCollection = bpy.data.collections[collectionName].objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objectsInCollection:
        obj.select_set(True)

        for qualityLevel in qualityLevels:
            qualityLevelDesc = "default"
            for obj in objectsInCollection:
                if hasSubdivisionModifier(obj):
                    qualityLevelDesc = qualityLevel.name

                if hasSubdivisionModifier(obj):
                    obj.modifiers['Subdivision'].levels = qualityLevel.value                    
                    
            exportPathStl = exportDir + collectionName + "\\STL\\"
            ensure_dir(exportPathStl)
            qualityLevelExportPathStl = exportPathStl + "\\" + collectionName 
            if qualityLevelDesc != "default":
                qualityLevelExportPathStl = qualityLevelExportPathStl + '_' + qualityLevelDesc
            
            exportPathFbx = exportDir + collectionName + "\\FBX\\"
            ensure_dir(exportPathFbx)
            qualityLevelExportPathFbx = exportPathFbx + "\\" + collectionName
            if qualityLevelDesc != "default":
                qualityLevelExportPathFbx = qualityLevelExportPathFbx + '_' + qualityLevelDesc
            
            bpy.ops.export_mesh.stl(filepath=qualityLevelExportPathStl + '.stl', use_selection=True)
            bpy.ops.export_scene.fbx(filepath=qualityLevelExportPathFbx + '.fbx', use_selection=True)
            
            if qualityLevelDesc == "default":
                break