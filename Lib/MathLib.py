from math import pi, sqrt
from mathutils import Vector, Euler

def eulerToDegrees(euler):
    fac = 180/pi
    eulerVector = Vector(euler)
    return fac * eulerVector

def degreesToEuler(degrees):
    fac = 180/pi
    x = degrees.x / fac
    y = degrees.y / fac
    z = degrees.z / fac
    return Euler((x, y, z), 'XYZ')