# System imports

try:
   import Image
except:
   from PIL import Image

from OpenGL.GL import *

import hashlib

# Vroom imports

from vroom.utils.debug import *

class TextureManager:
   ''' Texture object manager.

   When live coding is enabled it is possible that the initialization function
   could be called multiple times. To avoid creating multiple copies of texture
   data the TextureManager class maintains a cache of textures and will return
   an existing texture object if has already been created.

   NOTE: This class is used internall by vroom. The application should not need 
   to deal directly with this class. For texture support see the Texture class
   below.
   '''

   def __init__(self):
      self.cache = { }

   def get_texture(self, data):
      # Since textures can be initialized from filenames or directly from image
      # data the data itself is used as the key.
      m = hashlib.md5()
      m.update(data)
      key = m.hexdigest()

      # If the texture data already exists return the existing texture object. 
      # Otherwise create a new texture object and store it in the cache.
      if key in self.cache:
         #debug(msg='Returning cached texture object', level=VERBOSE).flush()
         return self.cache[key]

      #debug(msg='Creating new Texture object', level=VERBOSE).flush()
      texture = Texture()
      self.cache[key] = texture
      return texture

# Global texture manager object
_TextureManager = TextureManager()

class Texture:
   ''' Primary texture object.

   Textures objects can be initialized either from a filename or directly from
   image data. The preferred way to create a texture is through one of the static
   methods below as these utilize the TextureManager to avoid redundant data.

   It is possible to create a texture object directly and then call the load()
   method to initialized the image data. In this case the TextureManager is not
   called duplicate texture data could be created.
   '''

   @staticmethod
   def from_file(filename):
      #debug(msg='initializing texture from file', level=STATUS).flush()
      #debug(level=VERBOSE, indent=1).add('filename', filename).flush()

      image = Image.open(filename)

      try:
         ix, iy, image = image.size[0], image.size[1], image.tostring("raw", "RGBA", 0, -1)
      except SystemError:
         ix, iy, image = image.size[0], image.size[1], image.tostring("raw", "RGBX", 0, -1)

      return Texture.from_data(ix, iy, image)

   @staticmethod
   def from_data(ix, iy, image):
      #debug(msg='initializing texture from data', level=VERBOSE).flush()
      texture = _TextureManager.get_texture(image)
      texture.load(ix, iy, image)
      return texture

   def __init__(self):
      self.texture = glGenTextures(1)

   # Public interface
   
   def bind(self):
      glEnable(GL_TEXTURE_2D)
      glBindTexture(GL_TEXTURE_2D, self.texture)

   def unbind(self):
      glDisable(GL_TEXTURE_2D)
      glBindTexture(GL_TEXTURE_2D, 0)

   def load(self, ix, iy, image):
      self.bind()
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
      glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, 
            GL_RGBA, GL_UNSIGNED_BYTE, image)
      self.unbind()

