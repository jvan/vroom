# System imports

from OpenGL.GL import glFrontFace, glPushMatrix, glPopMatrix, GL_CCW, GL_CW
from OpenGL.GLU import gluQuadricTexture, gluCylinder, gluDisk

# Vroom imports

from vroom.core.transform import translateZ

from quadric import _get_quadric, _set_draw_style
from settings import CylinderRes, DiskRes

def cylinder(radius, height, **kwargs):
   ''' Draw a cylinder with given radius and height.'''
   
   # Get any keyword arguments 
   style   = kwargs.get('style', 'wireframe')
   texture = kwargs.get('texture', None)

   quadric = _get_quadric()

   # Setup texture if specified
   if texture:
      style = 'solid'
      gluQuadricTexture(quadric, True)
      texture.bind()

   # Set the quadric draw style (line or fill)
   _set_draw_style(style)

   # Draw the bottom end of the cylinder
   glFrontFace(GL_CW)
   gluDisk(quadric, 0, radius, DiskRes['slices'], DiskRes['loops'])
   glFrontFace(GL_CCW)

   # Draw the body of the cylinder
   gluCylinder(quadric, radius, radius, height, CylinderRes['slices'], CylinderRes['stacks'])

   # Draw the top end of the cylinder
   glPushMatrix()
   translateZ(height)
   gluDisk(quadric, 0, radius, DiskRes['slices'], DiskRes['loops'])
   glPopMatrix()

   # Clean up texture data if specified
   if texture:
      texture.unbind()
      gluQuadricTexture(quadric, False)

