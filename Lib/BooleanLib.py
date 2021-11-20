import bpy
import ObjectLib

def _modifier(objectA, objectB, operation, deleteObjectB, apply=True):
    ObjectLib.selectObject(objectA)
    modifierType = 'BOOLEAN'
    modifier = objectA.modifiers.new(name=modifierType + '_' + operation, type=modifierType)
    modifier.object = objectB
    modifier.operation = operation
    modifier.use_self = True

    if apply:
        bpy.ops.object.modifier_apply(modifier=modifier.name)
        if deleteObjectB:
            ObjectLib.delete(objectB)

def union(objectA, objectB, deleteObjectB=True, apply=True):
    _modifier(objectA, objectB, 'UNION', deleteObjectB, apply)

def difference(objectA, objectB, deleteObjectB=True, apply=True):
    _modifier(objectA, objectB, 'DIFFERENCE', deleteObjectB, apply)

def intersect(objectA, objectB, deleteObjectB=True, apply=True):
    _modifier(objectA, objectB, 'INTERSECT', deleteObjectB, apply)
