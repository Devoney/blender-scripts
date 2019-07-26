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

class ExportTypes(Enum):
    fbx = 0
    obj = 1
    stl = 2

exportDir = bpy.path.abspath("//Export\\")
collectionNames = ['Collection']
qualityLevels = [
    Quality.Low, 
    Quality.Medium, 
    Quality.High
]    

exportFileTypes = [
    ExportTypes.fbx,
    ExportTypes.obj, 
    ExportTypes.stl
]
    
def hasSubdivisionModifier(obj):
    return 'Subdivision' in obj.modifiers

def ensure_dir(file_path):
    if not os.path.exists(file_path):
        os.makedirs(file_path)

def dump(obj):
    pprint(getmembers(obj))
    
def export(fileType, qualityLevel, collectionName):
    exportDict = {
        ExportTypes.fbx: bpy.ops.export_scene.fbx,
        ExportTypes.obj: bpy.ops.export_scene.obj,
        ExportTypes.stl: bpy.ops.export_mesh.stl
    }
    
    exportPath = exportDir + collectionName + "\\" + fileType.name + "\\"
    ensure_dir(exportPath)
    qualityLevelExportPath = exportPath + "\\" + collectionName 
    if qualityLevel != "default":
        qualityLevelExportPath = qualityLevelExportPath + '_' + qualityLevel
    exportDict[fileType](filepath=qualityLevelExportPath + '.' + fileType.name, use_selection=True)   

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
            
            for exportFileType in exportFileTypes:        
                export(exportFileType, qualityLevelDesc, collectionName)
            
            if qualityLevelDesc == "default":
                break