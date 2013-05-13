# System imports

from OpenGL.GL import *

# Vroom imports

from vroom.utils.debug import *

from buffers import Buffer
from texture import Texture

class PointCloud(Buffer):
   ''' Point data renderer.

   The PointCloud class is useful for rendering point data. It is a subclass of
   GLArray specialized for points. A PointCloud object is initialized with 
   vertex data represting the points and optionally color data for each point.
   Point sprite can be used in rendering.
   '''

   def __init__(self, vertex_data=None, color_data=None):
      Buffer.__init__(self, vertex_data, color_data)

      self._sprite_texture = None
      self._point_size = 1.0
      self._point_sprite_size = 15.0

   def sprite(self, filename):
      ''' Enable or disable point sprite rendering.
      
      If filename is not None a texture object will be created from the
      filename and point sprites will be used when rendering. If filename is
      None point sprite rendering will be disabled.

      filename -- path to point sprite texture (or None to disable sprites)
      '''

      if filename:
         #debug(msg='initializing point sprite').add('filename', filename).flush()
         self._sprite_texture = Texture.from_file(filename)
      else:
         #debug(msg='point sprite rendering disabled').flush()
         self._sprite_texture = None

   def pointSize(self, size):
      ''' Set the point size.

      There are two different point sizes used depending on whether point
      sprite rendering is enabled. The default point size without sprites is
      1.0. The defualt point size with sprites is 15.0.
      '''
      
      if self._sprite_texture:
         self._point_sprite_size = size
      else:
         self._point_size = size

   def _pre_draw(self):
      Buffer._pre_draw(self)

      if self._sprite_texture == None:
         glPointSize(self._point_size);
         return

      glDepthMask(GL_FALSE);

      glEnable(GL_POINT_SMOOTH);
      glEnable(GL_BLEND);
      glBlendFunc(GL_SRC_ALPHA, GL_ONE);

      self._sprite_texture.bind()

      glPointSize(self._point_sprite_size)

      glTexEnvf(GL_POINT_SPRITE, GL_COORD_REPLACE, GL_TRUE);
      glEnable(GL_POINT_SPRITE);

   def _post_draw(self):
      Buffer._post_draw(self)

      if self._sprite_texture == None:
         return 

      self._sprite_texture.unbind()

      glDisable(GL_BLEND)
      glDisable(GL_POINT_SPRITE)
   
   #def center(self):
      #try:
         #return self._center
      #except:
         #self._center = [0.0, 0.0, 0.0]
         #for i in range(3):
            #self._center[i] = sum(v[i] for v in self._vertex_data) / len(self._vertex_data)
         #return self._center

