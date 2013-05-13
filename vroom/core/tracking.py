from environment import pushMatrix, popMatrix
from transform import translate
from color import color, red
from vroom.rendering.cube import cube
from vroom.utils.debug import *

from OpenGL.GL import *

import numpy
import ctypes

class Tracker:

   def __init__(self):
      self.tracked_objects = []
      self.active = None
      self.debugging = False
      self.dragging = False

   def add_object(self, obj):
      debug().add('object', obj).flush()
      self.tracked_objects.append(obj)
      debug(indent=1).add('tracked objects', len(self.tracked_objects))

   def draw(self):
      for obj in self.tracked_objects:
         if hasattr(obj, 'active'):
            color(red)
         else:
            color(0.25)

         pushMatrix()
         translate(obj.origin)
         obj.region.draw()
         popMatrix()

   def check_for_collision(self, pos):
      debug().flush()
      self.dragging = False
      for obj in self.tracked_objects:
         if obj.region.contains(pos):
            setattr(obj, 'active', True)
            self.dragging = True
            self.active  = { 'object': obj }
         elif hasattr(obj, 'active'):
            delattr(obj, 'active')

   def release(self):
      self.dragging = False
      if self.active and hasattr(self.active['object'], 'active'):
         delattr(self.active['object'], 'active')

   def move_active(self, pos):
      if not self.active:
         return 

      self.active['object'].move_to(pos)
      

_Tracker = Tracker()

def add_tracked_object(obj):
   global _Tracker
   _Tracker.add_object(obj)

def tracker_debug(enable):
   global _Tracker
   _Tracker.debugging = enable

def map_buffer(vbo):
   ''' Get data from vertex buffer object.
   
   vbo    -- vertex buffer object

   return -- 1D numpy array containing vertex data (flattened)
   '''

   func = ctypes.pythonapi.PyBuffer_FromMemory
   func.restype = ctypes.py_object
   
   vbo.bind()
   vp = glMapBuffer(vbo.target, GL_READ_WRITE)
   buffer = func(
      ctypes.c_void_p(vp), vbo.size
   )
   array = numpy.frombuffer(buffer, 'f')

   return array

class BoundingRegion:

   class Range:
      def __init__(self, _range):
         self.min = _range[0]
         self.max = _range[1]

      def __str__(self):
         return '[{}, {}]'.format(self.min, self.max)

      def delta(self):
         return (self.max - self.min)

      def mid(self):
         return (self.max + self.min)/2.0

      def contains(self, val):
         return val >= self.min and val <= self.max

   def __init__(self, x_bounds, y_bounds, z_bounds):
      self.bounds = { 'x': BoundingRegion.Range(x_bounds),
                      'y': BoundingRegion.Range(y_bounds),
                      'z': BoundingRegion.Range(z_bounds) }

   def __str__(self):
      return 'region\n\tx: {}\n\ty: {}\n\tz: {}'.format(self.bounds['x'], self.bounds['y'], self.bounds['z'])

   def draw(self):
      pushMatrix()
      translate(-self.bounds['x'].delta()/2.0,
                -self.bounds['y'].delta()/2.0,
                -self.bounds['z'].delta()/2.0)
      cube(self.bounds['x'].delta(),
           self.bounds['y'].delta(),
           self.bounds['z'].delta()) 
      popMatrix()

   def center(self):
      return [self.bounds['x'].mid(),
              self.bounds['y'].mid(), 
              self.bounds['z'].mid()]

   def contains(self, pos):
      (x,y,z) = pos
      if not self.bounds['x'].contains(x): return False
      if not self.bounds['y'].contains(y): return False
      if not self.bounds['z'].contains(z): return False
      return True


def compute_bounding_region(vbo):
   vertex_data = map_buffer(vbo)

   # compute min and max values for each coordinate
   x_min = numpy.min(vertex_data[::3])
   x_max = numpy.max(vertex_data[::3])

   y_min = numpy.min(vertex_data[1::3])
   y_max = numpy.max(vertex_data[1::3])

   z_min = numpy.min(vertex_data[2::3])
   z_max = numpy.max(vertex_data[2::3])

   glUnmapBuffer(vbo.target)
   vbo.unbind()

   return BoundingRegion([x_min, x_max],
                         [y_min, y_max],
                         [z_min, z_max])


