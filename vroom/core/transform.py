# System imports

from OpenGL.GL import glRotatef, glTranslate, glScale
import numpy
import pyvrui

# Vroom imports

from vroom.utils.debug import *

class Vector:
   def __init__(self, x=0.0, y=0.0, z=0.0):
      self.x, self.y, self.z = x, y, z 

   def data(self):
      return [self.x, self.y, self.z]

   @staticmethod
   def helper(*args):
      num_args = len(args)

      if num_args == 1:
         if type(args[0]) == list:
            return Vector.generate_from_list(args[0])
         else:
            raise Exception('Vector.helper: wrong type (expected list)') 
      elif num_args == 3:
         x, y, z = args
         return Vector(x,y,z)
      else:
         raise Exception('Vector.helper: wrong number of arguments (expected 1 or 3)')

   @staticmethod
   def generate_from_list(values):
      if len(values) == 3:
         x, y, z = values
         return Vector(x,y,z)
      else:
         raise Exception('Vector.generate_from_list: wrong number of elements (expected 3)')

def rotate(*args):
   ''' Rotate about the x-, y-, and z-axis.

   syntax:
      rotate(rx, ry, rz)
      rotate([rx, ry, rz])
   '''
   
   rx, ry, rz = Vector.helper(*args).data()

   glRotatef(rx, 1.0, 0.0, 0.0)
   glRotatef(ry, 0.0, 1.0, 0.0)
   glRotatef(rz, 0.0, 0.0, 1.0)

def rotateX(rx):
   glRotatef(rx, 1.0, 0.0, 0.0)

def rotateY(ry):
   glRotatef(ry, 0.0, 1.0, 0.0)

def rotateZ(rz):
   glRotatef(rz, 0.0, 0.0, 1.0)

def translate(*args):
   ''' Move in (x,y,z) space.

   syntax:
      translate(x,y,z)
      translate([x,y,z])
   '''

   tx, ty, tz = Vector.helper(*args).data() 
   glTranslate(tx, ty, tz)

def translateX(tx):
   translate(tx, 0, 0)

def translateY(ty):
   translate(0, ty, 0)

def translateZ(tz):
   translate(0, 0, tz)

def scale(*args):
   ''' Scale the model in x-, y-, and z-directions.

   syntax:
      scale(s)
      scale(sx, sy, sz)
      scale([sx, sy, sz])
   '''

   if len(args) == 1 and type(args[0]) == float:
      sx = sy = sz = args[0]
   else:
      sx, sy, sz = Vector.helper(*args).data()

   glScale(sx, sy, sz)

def centerDisplay():
   t =  Vrui.NavTransform.identity
   t = t * Vrui.NavTransform.translateFromOriginTo(Vrui.getDisplayCenter())
   t = t * Vrui.NavTransform.scale(Vrui.getInchFactor())
   Vrui.setNavigationTransformation(t)

def center(points):
   c = numpy.array(points).sum(0) / -len(points)
   return list(c)

