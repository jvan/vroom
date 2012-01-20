from OpenGL.GL import *
from OpenGL.arrays import vbo
import OpenGL
import numpy

class GLArray:

   RenderModes = { 'lines': GL_LINES }

   def __init__(self, vertex_data=None, color_data=None):

      self._vertex_buffer = None
      self._color_buffer = None

      if vertex_data != None:
         self.loadVertexData(vertex_data)
      if color_data != None:
         self.loadColorData(color_data)

      self._render_mode = GL_POINTS

   def loadVertexData(self, data, mode='static'):
      print ' -- loading vertex data'
      usage = GL_STATIC_DRAW if mode == 'static' else GL_DYNAMIC_DRAW 
      self._vertex_data = numpy.array(data, numpy.float32)
      self._vertex_buffer = vbo.VBO(data=self._vertex_data, usage=usage, target=GL_ARRAY_BUFFER)

   def loadColorData(self, data, mode='static'):
      print ' -- loading color data'
      usage = GL_STATIC_DRAW if mode == 'static' else GL_DYNAMIC_DRAW 
      self._color_data = numpy.array(data, numpy.float32)
      self._color_buffer = vbo.VBO(data=self._color_data, usage=usage, target=GL_ARRAY_BUFFER)

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

   def _post_draw(self):
      glPopClientAttrib()

      if self._vertex_buffer:
         self._vertex_buffer.unbind()
      
      if self._color_buffer:
         self._color_buffer.unbind()

   def draw(self):
      self._pre_draw()
      glDrawArrays(self._render_mode, 0, len(self._vertex_data))
      self._post_draw()


