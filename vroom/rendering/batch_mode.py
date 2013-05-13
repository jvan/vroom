# System imports

from OpenGL.GL import glPushMatrix, glPopMatrix

# Vroom imports

from vroom.core.transform import translate

class BatchRender:
   """ The BatchRender class is used in conjunction with the EnableBatchMode
   decorator below to enable a function to be called for a series of points.

   It is not meant to be used outside of the EnableBatchMode decorator.
   """

   def __init__(self, callback):
      self._callback = callback

   def __call__(self, points, *args, **kwargs):
      for p in points:
         glPushMatrix()
         translate(p)
         self._callback(*args, **kwargs)
         glPopMatrix()

def EnableBatchMode(func):
   """ Decorator to enable a function to be called for a series of points.
   
   Often times we want to do something like the following:

      for point in points:
         pushMatrix()
         translate(point)
         do_something()
         popMatrix()

   EnableBatchMode adds a for_each attribute to the function which is a 
   BatchRender functor (see above). This allows the function to be called 
   repeatedly for a series of points. For example, one could write the
   following to draw a series of spheres with centers defined in the list
   points:

      sphere.for_each(points, 1.0, style='solid')

   This accomplishes the same thing as the block of text above, but is much
   more readable.
   
   NOTE: The point_list class below accomplishes the same thing. It is likely
   that at some point one of these methods will e deprecated and removed.
   """

   func.for_each = BatchRender(func)
   return func

class point_list(list):
   """ Adds a for_each method to the standard python list.

   This approach is very similar to the EnableBatchMode decorator above except
   the callback and points array are switched. To draw a series of spheres as
   in the example above one would write:

      points.for_each(sphere, 1.0, style='solid')

   The benefit of this method over the previous one is that the arguments passed
   to the for_each function are all related.
   """

   def for_each(self, callback, *args, **kwargs):
      for point in self:
         glPushMatrix()
         translate(point)
         callback(*args, **kwargs)
         glPopMatrix()


class NewBatchRender:
   def __init__(self, f, *args, **kwargs):
      self.func = f
      self.args = args
      self.kwargs = kwargs
      self._triggered = False

   def __del__(self):
      if not self._triggered:
         self._func(*self.args, **self.kwargs)

   def for_each(self, points):
      for pos in points:
         glPushMatrix()
         translate(pos)
         self.func(*self.args, **self.kwargs)
         glPopMatrix()
      self._triggered = True

   def at(self, point):
      glPushMatrix()
      translate(point)
      self.func(*self.args, **self.kwargs)
      glPopMatrix()
      self._triggered = True

def draw(func, *args, **kwargs):
   return NewBatchRender(func, *args, **kwargs)
