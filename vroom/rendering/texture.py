try:
   import Image
except:
   from PIL import Image

from OpenGL.GL import *

class Texture:

   def __init__(self, filename):
      image = Image.open(filename)

      try:
         ix, iy, image = image.size[0], image.size[1], image.tostring("raw", "RGBA", 0, -1)
      except SystemError:
         ix, iy, image = image.size[0], image.size[1], image.tostring("raw", "RGBX", 0, -1)

      self.texture = glGenTextures(1) 
      self.bind()
      self.load(ix, iy, image)
      self.unbind()

   def bind(self):
      glEnable(GL_TEXTURE_2D)
      glBindTexture(GL_TEXTURE_2D, self.texture)

   def unbind(self):
      glDisable(GL_TEXTURE_2D)
      glBindTexture(GL_TEXTURE_2D, 0)

   def load(self, ix, iy, image):
      glTexImage2D(
            GL_TEXTURE_2D, 0, 3, ix, iy, 0, 
            GL_RGBA, GL_UNSIGNED_BYTE, image
      )
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);

