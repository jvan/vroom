from OpenGL.GL import glPushMatrix, glPopMatrix, glBegin, glEnd, glVertex2f, GL_LINES
from vroom.transform import scale, rotate
from glarray import GLArray
import math

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
      print ' Grid: updating cache...'
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

      self.buffer = GLArray(points)
      self.buffer.renderMode(GL_LINES)

grid = Grid()

def arrow_2d():
   l = 0.05
   theta = math.radians(20.0)
   
   glBegin(GL_LINES)
   glVertex2f(0.0, 0.0)
   glVertex2f(0.0, 1.0)
   
   glVertex2f(0.0, 1.0)
   glVertex2f(-l*math.cos(theta), 1.0-l*math.sin(theta))

   glVertex2f(0.0, 1.0)
   glVertex2f(l*math.cos(theta), 1.0-l*math.sin(theta))
   glEnd()

def axes(length=1.0):

   glPushMatrix()
   scale(length)

   # y-axis
   arrow_2d()

   # z-axis
   glPushMatrix()
   rotate(90.0, 0.0, 0.0)
   arrow_2d()
   glPopMatrix()

   # x-axis
   glPushMatrix()
   rotate(0.0, 0.0, -90.0)
   arrow_2d()
   glPopMatrix() 

   glPopMatrix()


