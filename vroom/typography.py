import FTGL
from OpenGL.GL import *

Font = None

# processing syntax
#
# text(data, x, y)
# text(data, x, y, z)
# text(stringdata, x, y, width, height)
# text(stringdata, x, y, width, height, z)

def text(data, x, y, z):
   _text_pixmap(data, x, y, z)

def _text_pixmap(data, x, y, z):
   glPushMatrix()
   glTranslatef(x, y, z)
   glRasterPos(0.05, 0.05)
   Font.Render(data)
   glPopMatrix()

def _text_texture(data, x, y, z):
   print ' rendering text={} at ({}, {}, {})'.format(data, x, y, z)
   glEnable(GL_TEXTURE_2D)
   glEnable(GL_BLEND)
   glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
   glPushMatrix()
   glTranslatef(x, y, z)
   Font.Render(data)
   glPopMatrix()
   glDisable(GL_TEXTURE_2D)
   glDisable(GL_BLEND)

# processing syntax
#
# textFont(font)
# textFont(font, size)

def textFont(filename, size=10):
   global Font
   Font = FTGL.PixmapFont(filename)
   Font.FaceSize(size, 0)
