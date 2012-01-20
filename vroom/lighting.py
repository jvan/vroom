from OpenGL.GL import *
from color import Color

def lighting(enable):
   ''' Enable or disable lighting.'''

   if enable:
      glEnable(GL_LIGHTING)
   else:
      glDisable(GL_LIGHTING)

def material(*args):
   ''' Set the current material color.

   syntax:
      material(grey)
      material(r, g, b)
      material([r, g, b])
   '''

   color = Color.helper(*args)
   
   glMaterialfv(GL_FRONT, GL_DIFFUSE, color.data())
   glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0,1.0,1.0,1.0])
   glMaterialfv(GL_FRONT, GL_SHININESS, 50.0)


def transparency(enable):
   if enable:
      glEnable(GL_BLEND)
      glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
   else:
      glDisable(GL_BLEND)
