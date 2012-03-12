from application import *
from utils import *
from environment import *
from color import *
from lighting import *
from transform import *
from rendering import *
from typography import *

_App = None
_App_Path = None 
_Module_Name = None
_Resource_Paths = None

pushMatrix = glPushMatrix
popMatrix = glPopMatrix
pointSize = glPointSize
lineWidth = glLineWidth

red   = [1.0, 0.0, 0.0]
green = [0.0, 1.0, 0.0]
blue  = [0.0, 0.0, 1.0]


class _Global: pass
Global = _Global()

class point_list(list):
   def for_each(self, callback, *args, **kwargs):
      for point in self:
         pushMatrix()
         translate(point)
         callback(*args, **kwargs)
         popMatrix()

class ResourceNotFound: 
   def __init__(self, filename):
      self.filename = filename

def  get_resource(filename):

   print ' -- searching for resource {}'.format(filename)

   # Check for the file in the application's data directory
   path = os.path.join(_Resource_Paths[0], 'data', filename)
   if os.path.exists(path):
      print ' -- found application resource {}'.format(path)
      return path

   # Check for the file in the global vroom resource dir
   path = os.path.join(_Resource_Paths[1], 'data', filename)
   if os.path.exists(path):
      print ' -- found global resource {}'.format(path)
      return path

   #return os.path.join(_App_Path, 'data', filename)
   raise ResourceNotFound(filename)

from random import random, randrange

def random_vertex(start, stop):
   return [randrange(start, stop) for i in range(3)] 

def random_color():
   return [random() for i in range(3)]

def random_vertex_generator(n, start=-1.0, stop=1.0):
   for i in range(n):
      yield random_vertex(start, stop)

def random_color_generator(n):
   for i in range(n):
      yield random_color()
