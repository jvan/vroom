try:
   import Image
except:
   from PIL import Image

from OpenGL.GL import *

import hashlib

class TextureManager:

   def __init__(self):
      self.cache = { }

   def get_texture(self, data):
      m = hashlib.md5()
      m.update(data)
      key = m.hexdigest()
      if key in self.cache:
         print 'Returning cached texture object'
         return self.cache[key]
      else:
         print 'Creating new Texture object'
         texture = Texture()
         self.cache[key] = texture
         return texture

_TextureManager = TextureManager()

class Texture:

   def __init__(self):
      self.texture = glGenTextures(1)
   
   @staticmethod
   def from_file(filename):
      print 'initializing texture from file'
      image = Image.open(filename)

      try:
         ix, iy, image = image.size[0], image.size[1], image.tostring("raw", "RGBA", 0, -1)
      except SystemError:
         ix, iy, image = image.size[0], image.size[1], image.tostring("raw", "RGBX", 0, -1)

      return Texture.from_data(ix, iy, image)

   @staticmethod
   def from_data(ix, iy, image):
      print 'initializing texture from data'

      #texture = Texture()
      texture = _TextureManager.get_texture(image)
      texture.bind()
      texture.load(ix, iy, image)
      texture.unbind()
      return texture


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

