from OpenGL.GL import glPushMatrix, glPopMatrix
from vroom.transform import translate

class BatchRenderer:
   def __init__(self, callback):
      self._callback = callback

   def __call__(self, points, *args, **kwargs):
      for p in points:
         glPushMatrix()
         translate(p)
         self._callback(*args, **kwargs)
         glPopMatrix()

def EnableBatchMode(func):
   func.for_each = BatchRenderer(func)
   return func

