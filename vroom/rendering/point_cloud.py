from glarray import GLArray
from texture import Texture

from OpenGL.GL import *

class PointCloud(GLArray):

   def __init__(self, vertex_data=None, color_data=None):
      GLArray.__init__(self, vertex_data, color_data)
      self._sprite_texture = None

   def sprite(self, filename):
      print ' -- initializing point sprite {}'.format(filename)

      self._sprite_texture = Texture.from_file(filename)

   def _pre_draw(self):
      GLArray._pre_draw(self)

      if self._sprite_texture == None:
         return

      glDepthMask(GL_FALSE);

      glEnable(GL_POINT_SMOOTH);
      glEnable(GL_BLEND);
      glBlendFunc(GL_SRC_ALPHA, GL_ONE);

      self._sprite_texture.bind()

      glTexEnvf(GL_POINT_SPRITE, GL_COORD_REPLACE, GL_TRUE);
      glEnable(GL_POINT_SPRITE);

      glPointSize(15.0);

   def _post_draw(self):
      GLArray._post_draw(self)

      if self._sprite_texture == None:
         return 

      self._sprite_texture.unbind()

      glDisable(GL_BLEND)
      glDisable(GL_POINT_SPRITE)
   
   def center(self):
      try:
         return self._center
      except:
         self._center = [0.0, 0.0, 0.0]
         for i in range(3):
            self._center[i] = sum(v[i] for v in self._vertex_data) / len(self._vertex_data)
         return self._center

