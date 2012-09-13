from OpenGL.GL import *
from OpenGL.arrays import vbo
import numpy

from vroom.utils.debug import debug, STATUS, DEBUG, VERBOSE

class GLArray:

   RenderModes = { 
      'lines': GL_LINES,
      'triangles': GL_TRIANGLES 
      }

   def __init__(self, vertex_data=None, color_data=None, normal_data=None, index_data=None):

      self._vertex_buffer = None
      self._color_buffer = None
      self._index_buffer = None
      self._normal_buffer = None

      if vertex_data != None:
         self.loadVertexData(vertex_data)
      if color_data != None:
         self.loadColorData(color_data)
      if normal_data != None:
         self.loadNormalData(normal_data)
      if index_data != None:
         self.loadIndexData(index_data)
   
      self._render_mode = GL_POINTS

   def loadVertexData(self, data, mode='static'):
      debug(msg='loading vertex data', level=VERBOSE).flush()
      usage = GL_STATIC_DRAW if mode == 'static' else GL_DYNAMIC_DRAW 
      vertex_data = numpy.array(data, numpy.float32)
      self._vertex_buffer = vbo.VBO(data=vertex_data, usage=usage, target=GL_ARRAY_BUFFER)
      self._num_vertices = len(vertex_data)
   
   def loadColorData(self, data, mode='static'):
      debug(msg='loading color data', level=VERBOSE).flush()
      usage = GL_STATIC_DRAW if mode == 'static' else GL_DYNAMIC_DRAW 
      color_data = numpy.array(data, numpy.float32)
      self._color_buffer = vbo.VBO(data=color_data, usage=usage, target=GL_ARRAY_BUFFER)

   def loadNormalData(self, data, mode='static'):
      debug(msg='loading normal data', level=VERBOSE).flush()
      usage = GL_STATIC_DRAW if mode == 'static' else GL_DYNAMIC_DRAW 
      normal_data = numpy.array(data, numpy.float32)
      self._normal_buffer = vbo.VBO(data=normal_data, usage=usage, target=GL_ARRAY_BUFFER)

   def loadIndexData(self, data, mode='static'):
      debug(msg='loading index data', level=VERBOSE).flush()
      usage = GL_STATIC_DRAW if mode == 'static' else GL_DYNAMIC_DRAW 
      index_data = numpy.array(data, numpy.uint32)
      self._index_buffer = vbo.VBO(data=index_data, usage=usage, target=GL_ELEMENT_ARRAY_BUFFER)

   def renderMode(self, mode):
      if isinstance(mode, str):
         self._render_mode = GLArray.RenderModes[mode]
      else:
         self._render_mode = mode

   def _pre_draw(self):
      glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)

      if self._vertex_buffer:
         glEnable(GL_VERTEX_ARRAY)
         self._vertex_buffer.bind()
         glVertexPointer(3, GL_FLOAT, 0, None)
         
      if self._color_buffer:
         glEnable(GL_COLOR_ARRAY)
         self._color_buffer.bind()
         glColorPointer(4, GL_FLOAT, 0, None)

      if self._normal_buffer:
         glEnable(GL_NORMAL_ARRAY)
         self._normal_buffer.bind()
         glNormalPointer(GL_FLOAT, 0, None)

      if self._index_buffer:
         self._index_buffer.bind()

   def _post_draw(self):
      glPopClientAttrib()

      if self._vertex_buffer:
         self._vertex_buffer.unbind()
      
      if self._color_buffer:
         self._color_buffer.unbind()
   
      if self._normal_buffer:
         self._normal_buffer.unbind()

      if self._index_buffer:
         self._index_buffer.unbind()

   def draw(self):
      self._pre_draw()
      if self._index_buffer:
         glDrawElements(self._render_mode, len(self._index_buffer), GL_UNSIGNED_INT, None)
      else:
         glDrawArrays(self._render_mode, 0, self._num_vertices)
      self._post_draw()


