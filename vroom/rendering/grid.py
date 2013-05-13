# System imports

from OpenGL.GL import GL_LINES

# vroom imports

from vroom.utils.debug import *

from buffers import Buffer

class Grid:

   def __init__(self):
      self.x = None
      self.y = None
      self.nx = None
      self.ny = None

   def __call__(self, x, y, nx, ny):
      checks = [ 
            self.x != x, 
            self.y != y, 
            self.nx != nx, 
            self.ny != ny ]
      if any(checks):
         self._update(x, y, nx, ny)

      self.buffer.draw()

   def _update(self, x, y, nx, ny):
      debug(msg='updating cache').flush()
      
      self.x = x
      self.y = y
      self.nx = nx
      self.ny = ny

      dx = self.x / self.nx
      dy = self.y / self.ny

      points = [ ]
      for i in range(nx):
         points.append([i*dx, 0.0, 0.0])
         points.append([i*dx,   y, 0.0])
      points.append([x, 0.0, 0.0])
      points.append([x, y,   0.0])

      for i in range(ny):
         points.append([0.0, i*dy, 0.0])
         points.append([x,   i*dy, 0.0])
      points.append([0, y, 0.0])
      points.append([x, y, 0.0])

      print('(x={}, y={})'.format(self.x, self.y))
      print('(nx={}, ny={})'.format(self.nx, self.ny))

      print('len(points)={}'.format(len(points)))

      self.buffer = Buffer(points)
      self.buffer.renderMode('lines')

grid = Grid()

