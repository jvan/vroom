from OpenGL.GL import glPushMatrix, glPopMatrix, glBegin, glEnd, glVertex2f, GL_LINES
from vroom.transform import scale, rotate

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

