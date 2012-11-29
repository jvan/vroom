# System imports

from OpenGL.GL import glPushMatrix, glPopMatrix
from OpenGL.GL import glBegin, glEnd, glVertex2f, GL_LINES

import math

# Vroom imports

from vroom.core.transform import scale, rotate

def arrow_2d():
   ''' Draw a 2-dimensional arrow in the x-y plane.'''

   length = 0.05 # length of the arrow head
   theta  = math.radians(20.0) # angle of the arrow head
   
   glBegin(GL_LINES)

   # Draw the shaft of the array along the y-axis
   glVertex2f(0.0, 0.0)
   glVertex2f(0.0, 1.0)
   
   # Draw the left side of the arrow head
   glVertex2f(0.0, 1.0)
   glVertex2f(-length*math.cos(theta), 1.0-length*math.sin(theta))

   # Draw the right side of the arrow head
   glVertex2f(0.0, 1.0)
   glVertex2f(length*math.cos(theta), 1.0-length*math.sin(theta))

   glEnd()

def axes(length=1.0):
   ''' Draw x,y,z axes.
   
   length -- length of the arrows along axes
   '''

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

