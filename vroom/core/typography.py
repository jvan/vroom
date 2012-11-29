# System imports

from OpenGL.GL import *
import FTGL

# Global font object
_Font = None

def text(data, *args):
   ''' Render text.

   syntax:
      text(data, x, y, z)
      text(data [x, y, z])
   '''

   if len(args) == 1:
      x, y, z = args[0]
   else:
      x, y, z = args

   _text_pixmap(data, x, y, z)

def _text_pixmap(data, x, y, z):
   glPushMatrix()
   glTranslatef(x, y, z)
   glRasterPos(0.05, 0.05)
   _Font.Render(data)
   glPopMatrix()

def _text_texture(data, x, y, z):
   glEnable(GL_TEXTURE_2D)
   glEnable(GL_BLEND)
   glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
   glPushMatrix()
   glTranslatef(x, y, z)
   _Font.Render(data)
   glPopMatrix()
   glDisable(GL_TEXTURE_2D)
   glDisable(GL_BLEND)

def textFont(filename, size=10):
   ''' Set the font type and size.'''

   global _Font
   _Font = FTGL.PixmapFont(filename)
   textSize(size)

def textSize(size):
   global _Font
   _Font.FaceSize(size, 0)
