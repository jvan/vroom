from glarray import GLArray
try:
   import Image
except:
   from PIL import Image
from OpenGL.GL import *

class PointCloud(GLArray):

   def __init__(self, vertex_data=None, color_data=None):
      GLArray.__init__(self, vertex_data, color_data)
      self._sprite_texture = None

   def sprite(self, filename):
      print ' -- initializing point sprite {}'.format(filename)
      im = Image.open(filename)
      try:
         ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBA", 0, -1)
      except SystemError:
         ix, iy, image = im.size[0], im.size[1], im.tostring("raw", "RGBX", 0, -1)

      self._sprite_texture = glGenTextures(1) 
      glBindTexture(GL_TEXTURE_2D, self._sprite_texture)
      glTexImage2D(
            GL_TEXTURE_2D, 0, 3, ix, iy, 0, 
            GL_RGBA, GL_UNSIGNED_BYTE, image
      )
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
      glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);

   def _pre_draw(self):
      GLArray._pre_draw(self)

      if self._sprite_texture == None:
         return
      
      glDepthMask(GL_FALSE);

      glEnable(GL_POINT_SMOOTH);
      glEnable(GL_BLEND);
      glBlendFunc(GL_SRC_ALPHA, GL_ONE);

      glEnable(GL_TEXTURE_2D);
      glBindTexture(GL_TEXTURE_2D, self._sprite_texture);

      glTexEnvf(GL_POINT_SPRITE, GL_COORD_REPLACE, GL_TRUE);
      glEnable(GL_POINT_SPRITE);

      glPointSize(15.0);

   def _post_draw(self):
      GLArray._post_draw(self)

      if self._sprite_texture == None:
         return 

      glDisable(GL_TEXTURE_2D)
      glDisable(GL_BLEND)
      glDisable(GL_POINT_SPRITE)
      glBindTexture(GL_TEXTURE_2D, 0)

   
   def center(self):
      try:
         return self._center
      except:
         self._center = [0.0, 0.0, 0.0]
         for i in range(3):
            self._center[i] = sum(v[i] for v in self._vertex_data) / len(self._vertex_data)
         return self._center

