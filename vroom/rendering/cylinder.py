from OpenGL.GL import glFrontFace, glPushMatrix, glPopMatrix, GL_CCW, GL_CW
from OpenGL.GLU import gluQuadricTexture, gluCylinder, gluDisk

from vroom.transform import translateZ

from quadric import _get_quadric, _set_draw_style
from settings import CylinderRes, DiskRes

def cylinder(radius, height, **kwargs):
   quadric = _get_quadric()
   texture = kwargs.get('texture', None)
   style = kwargs.get('style', 'wireframe')
   if texture:
      style = 'solid'
      gluQuadricTexture(quadric, True)
      texture.bind()
   else:
      gluQuadricTexture(quadric, False)
   _set_draw_style(style)
   glFrontFace(GL_CW)
   #disk(radius, texture=texture)
   gluDisk(quadric, 0, radius, DiskRes['slices'], DiskRes['loops'])
   glFrontFace(GL_CCW)
   gluCylinder(quadric, radius, radius, height, CylinderRes['slices'], CylinderRes['stacks'])
   glPushMatrix()
   translateZ(height)
   #disk(radius, texture=texture)
   gluDisk(quadric, 0, radius, DiskRes['slices'], DiskRes['loops'])
   glPopMatrix()
   if texture:
      texture.unbind()

