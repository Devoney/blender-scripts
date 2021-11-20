from enum import Enum, unique
from BooleanLib import union
from MeshLib import cube
from ObjectLib import centerOrigin, translate, rotate
import ObjectLib
import ExportLib
import OpenscadLib
import bpy

class FingerJointStart(Enum):
  INNER = 1
  OUTER = 2

class FingerjointsCreator():
  materialThickness = 0
  burn = 1
  def __init__(self, materialThickness, burn):
    self.materialThickness = materialThickness
    self.burn = burn

  def joint(self, nrOfFingers, length, type = 'male'):
    defaultWidth = length / nrOfFingers
    allFingers = None
    lastX = None
    for i in range(0, nrOfFingers):
      even = (i % 2) == 0
      if type == 'male' and not even:
        continue
      if type == 'female' and even:
        continue

      isFirst = i == 0
      isLast = i == (nrOfFingers-1)
      burnCompensation = self.burn
      x = (defaultWidth / 2) + (i * defaultWidth)
      
      if (not isFirst and not isLast):
        burnCompensation = burnCompensation + self.burn
      
      if isFirst:
        x = x + (burnCompensation / 2)
      elif isLast:
        x = x - (burnCompensation / 2)
      lastX = x

      fingerWidth = defaultWidth + burnCompensation
      finger = cube((fingerWidth, self.materialThickness * 2, self.materialThickness))
      translate(finger, (x, 0, 0))

      if allFingers is None:
        allFingers = finger
      else:
        union(allFingers, finger)
    
    centerOrigin(allFingers)
    allFingers.location.x = 0
    return allFingers

  def fingerjoints(self, nrOfFingers, length, start, invert=False):
    nrOfFingerParts = self._getNrOfFingerParts(nrOfFingers, start)

    defaultWidth = length / nrOfFingerParts
    x = 0
    # print("nrOfFingerParts: " + str(nrOfFingerParts))
    previousFinger = None
    firstWidth = None
    for i in range(0,nrOfFingerParts):
      # print("\t" + str(i))
      burnCompensation = 0
      if self._isFinger(i, start):
        # print("\tisFinger")
        burnCompensation = self.burn
        isFirst = i == 0
        isLast = i == (nrOfFingerParts-1)
        if (not isFirst and not isLast) or nrOfFingerParts == 1:
          burnCompensation = burnCompensation + self.burn
        
        fingerWidth = defaultWidth
        if not invert:
          fingerWidth = fingerWidth + burnCompensation
        else:
          fingerWidth = fingerWidth - burnCompensation
        size = (fingerWidth, self.materialThickness * 2, self.materialThickness)
        if firstWidth is None:
          firstWidth = size[0]
        # print("\tSize=" + str(size))
        fingerX = x
        if isFirst:
          fingerX = fingerX + (burnCompensation / 2)
        if isLast:
          fingerX = fingerX - (burnCompensation / 2)
        finger = cube(size=size, location=(fingerX, 0, 0))
        if previousFinger is not None:
          union(previousFinger, finger)
        else:
          previousFinger = finger
      x = x + defaultWidth
    
    if firstWidth is None:
      firstWidth = length

    translateX = -((length / 2) - (firstWidth / 2))
    #if nrOfFingerParts > 1:
    translateX = translateX - (burnCompensation / 2)
    translate(previousFinger, (translateX, 0, 0))
    centerOrigin(previousFinger)
    return previousFinger

  def _getNrOfFingerParts(self, nrOfFingers, start):
    fingerParts = (nrOfFingers * 2)
    correction = 0
    if start == FingerJointStart.INNER:
      correction = 1
    else:
      correction = -1

    fingerParts = fingerParts + correction
    return fingerParts

  def _isFinger(self, index, start):
    # print("\tstart: " + str(start) + "\t" + str(FingerJointStart.OUTER) + " " + str(FingerJointStart.INNER))
    isEven = True if (index % 2) == 0 else False
    # print("\tisEven: " + str(isEven))
    returnValue = False
    if isEven:
      # print("\tOuter")
      returnValue = str(start) ==str(FingerJointStart.OUTER)
    else:
      # print("\tInner")
      returnValue = str(start) == str(FingerJointStart.INNER)
    # print("\treturnValue: " + str(returnValue))
    return returnValue

def _getSmallestAxis(obj):
  smallestDimensionAxis = None
  if obj.dimensions.x < obj.dimensions.y:
    smallestDimensionAxis = 'x'
    smallestDimension = obj.dimensions.x
  else:
    smallestDimensionAxis = 'y'
    smallestDimension = obj.dimensions.y
  
  if obj.dimensions.z < smallestDimension:
    smallestDimensionAxis = 'z'

  return smallestDimensionAxis

def _layFlat(obj):
  xRot = 0
  yRot = 0
  zRot = 0

  smallestAxis = _getSmallestAxis(obj)
  if smallestAxis == 'x':
    yRot = 90
  elif smallestAxis == 'y':
    xRot = 90

  rotate(obj, (xRot, yRot, zRot))

def exportForCutting(partNames, distanceBetweenParts, assemblyName, boundingBox, combined=False):
  boundingBoxMax = boundingBox.maximum

  previousPart = None
  objectsToExport = []
  for partName in partNames:
      cloneName = 'ffe_' + partName
      ObjectLib.deselectAll()
      ObjectLib.selectObject(partName)
      ObjectLib.clone(partName, 0, cloneName)
      part = ObjectLib.getObject(cloneName)

      ObjectLib.resetRotation(part)
      _layFlat(part)
      ObjectLib.applyAllTransformations(part)
      ObjectLib.centerOrigin(part, 'BOUNDS')

      print('Moving part ' + part.name)        
      part.location.y = boundingBoxMax.y + distanceBetweenParts + (part.dimensions.y / 2)
      part.location.z = 0

      if previousPart is not None:
          part.location.x = previousPart.location.x + (previousPart.dimensions.x / 2) + (part.dimensions.x / 2) + (10/1000)

      previousPart = part
      objectsToExport.append(part)

  if combined:
    uniqueParts = ObjectLib.joinObjects(objectsToExport, assemblyName)
    objectsToExport = [uniqueParts]
    
  for objToExport in objectsToExport:
    stlFilePath = ExportLib.export(objToExport, True, 1000)
    OpenscadLib.stlTo(stlFilePath, ['dxf', 'svg'])