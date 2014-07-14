from OpenGL.GL import *
from OpenGL.arrays import vbo
import numpy

from vroom.core.environment import pushMatrix, popMatrix
from vroom.core.transform import translate

from vroom.core.tracking import add_tracked_object, compute_bounding_region

from vroom.utils.debug import debug, STATUS, DEBUG, VERBOSE

from time import time

class Buffer:

   RenderModes = { 
      'points':          GL_POINTS,
      'lines':           GL_LINES,
      'lines:strip':     GL_LINE_STRIP,
      'lines:loop':      GL_LINE_LOOP,
      'triangles':       GL_TRIANGLES,
      'triangles:strip': GL_TRIANGLE_STRIP,
      'triangles:fan':   GL_TRIANGLE_FAN
      }

   UsageModes = {
      'static':       GL_STATIC_DRAW,
      'static:draw':  GL_STATIC_DRAW,
      'static:read':  GL_STATIC_READ,
      'static:copy':  GL_STATIC_COPY,
      'dynamic':      GL_DYNAMIC_DRAW,
      'dynamic:draw': GL_DYNAMIC_DRAW,
      'dynamic:read': GL_DYNAMIC_READ,
      'dynamic:copy': GL_DYNAMIC_COPY,
      'stream':       GL_STREAM_DRAW,
      'stream:draw':  GL_STREAM_DRAW,
      'stream:read':  GL_STREAM_READ,  
      'stream:copy':  GL_STREAM_COPY
   }

   DType = numpy.float32

   def __init__(self, vertex_data=None, color_data=None, normal_data=None, index_data=None):

      self._vertex_buffer = None
      self._color_buffer = None
      self._normal_buffer = None
      self._texcoord_buffer = None
      self._index_buffer = None
      
      self._index_buffers = []

      if vertex_data != None:
         self.loadVertexData(vertex_data)
      if color_data != None:
         self.loadColorData(color_data)
      if normal_data != None:
         self.loadNormalData(normal_data)
      if index_data != None:
         self.loadIndexData(index_data)
   
      self._render_mode = GL_POINTS

      self.origin = [0.0, 0.0, 0.0]

   def loadVertexData(self, data, mode='static'):
      #debug(msg='loading vertex data', level=VERBOSE).flush()
      #usage = GL_STATIC_DRAW if mode == 'static' else GL_DYNAMIC_DRAW 
      usage = Buffer.UsageModes[mode]
      vertex_data = numpy.array(data, Buffer.DType)
      self._vertex_buffer = vbo.VBO(data=vertex_data, usage=usage, target=GL_ARRAY_BUFFER)
      #self._num_vertices = len(vertex_data)/3
      self._num_vertices = len(vertex_data)

   def updateVertexData(self, data):
      #start = time()
      #vertex_data = numpy.array(data, Buffer.DType)
      #print('\t -- convert: {} (s)'.format(time()-start))
      #start =time()
      #self._vertex_buffer.set_array(vertex_data)
      #print('\t -- upload: {} (s)'.format(time()-start))
      self._vertex_buffer.set_array(data)

   def loadColorData(self, data, mode='static'):
      #debug(msg='loading color data', level=VERBOSE).flush()
      #usage = GL_STATIC_DRAW if mode == 'static' else GL_DYNAMIC_DRAW 
      usage = Buffer.UsageModes[mode]
      color_data = numpy.array(data, Buffer.DType)
      self._color_buffer = vbo.VBO(data=color_data, usage=usage, target=GL_ARRAY_BUFFER)

   def loadNormalData(self, data, mode='static'):
      #debug(msg='loading normal data', level=VERBOSE).flush()
      usage = GL_STATIC_DRAW if mode == 'static' else GL_DYNAMIC_DRAW 
      normal_data = numpy.array(data, Buffer.DType)
      self._normal_buffer = vbo.VBO(data=normal_data, usage=usage, target=GL_ARRAY_BUFFER)

   def loadIndexData(self, data, mode='static'):
      #debug(msg='loading index data', level=VERBOSE).flush()
      usage = GL_STATIC_DRAW if mode == 'static' else GL_DYNAMIC_DRAW 
      index_data = numpy.array(data, numpy.uint32)
      self._index_buffer = vbo.VBO(data=index_data, usage=usage, target=GL_ELEMENT_ARRAY_BUFFER)

   def loadTexCoordData(self, data, mode='static'):
      usage = GL_STATIC_DRAW if mode == 'static' else GL_DYNAMIC_DRAW 
      texcoord_data = numpy.array(data, Buffer.DType)
      self._texcoord_buffer = vbo.VBO(data=texcoord_data, usage=usage, target=GL_ARRAY_BUFFER)

   def renderMode(self, mode):
      if isinstance(mode, str):
         self._render_mode = Buffer.RenderModes[mode]
      else:
         self._render_mode = mode

   def _pre_draw(self):
      glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)

      if self._vertex_buffer:
         glEnableClientState(GL_VERTEX_ARRAY)
         self._vertex_buffer.bind()
         glVertexPointer(3, GL_FLOAT, 0, None)
         
      if self._color_buffer:
         glEnableClientState(GL_COLOR_ARRAY)
         self._color_buffer.bind()
         glColorPointer(4, GL_FLOAT, 0, None)

      if self._normal_buffer:
         glEnableClientState(GL_NORMAL_ARRAY)
         self._normal_buffer.bind()
         glNormalPointer(GL_FLOAT, 0, None)

      if self._texcoord_buffer:
         glEnableClientState(GL_TEXTURE_COORD_ARRAY)
         self._texcoord_buffer.bind()
         glTexCoordPointer(2, GL_FLOAT, 0, None)

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

      if self._texcoord_buffer:
         self._texcoord_buffer.unbind()

      if self._index_buffer:
         self._index_buffer.unbind()

   def draw(self, **kwargs):
      style = kwargs.get('style', 'wireframe')

      glPushAttrib(GL_POLYGON_BIT)
      if style == 'wireframe':
         glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

      self._pre_draw()

      pushMatrix()
      translate(self.origin)

      if self._index_buffer:
         glDrawElements(self._render_mode, len(self._index_buffer), GL_UNSIGNED_INT, None)
      else:
         glDrawArrays(self._render_mode, 0, self._num_vertices)

      popMatrix()

      self._post_draw()

      glPopAttrib()

   def enable_tracking(self, **kwargs):
      debug().flush()
      cache = kwargs.get('cache', None)
      if cache:
         debug(msg='loading bounding region from cache')
      else:
         self.region = compute_bounding_region(self._vertex_buffer)
         debug(indent=1).add('region', self.region).flush()
         debug(indent=1).add('region.center', self.region.center()).flush()
         add_tracked_object(self)

   def move_to(self, position):
      debug().add('position', position)

      dx = position[0] - self.origin[0]
      dy = position[1] - self.origin[1]
      dz = position[2] - self.origin[2]

      self.origin = position

      if not hasattr(self, 'region'):
         return

      self.region.bounds['x'].min += dx 
      self.region.bounds['x'].max += dx 

      self.region.bounds['y'].min += dy 
      self.region.bounds['y'].max += dy 

      self.region.bounds['z'].min += dz 
      self.region.bounds['z'].max += dz 

class IndexedBuffer(Buffer):

   class Patch:
      def __init__(self, ibo, mode):
         self.ibo = ibo
         self.mode = mode
      def draw(self):
         self.ibo.bind()
         glDrawElements(self.mode, len(self.ibo), GL_UNSIGNED_INT, None)
         self.ibo.unbind()

   def __init__(self, vertex_data=None, color_data=None, normal_data=None):
      Buffer.__init__(self, vertex_data, color_data, normal_data)
      self._index_buffers = []

   def addIndexData(self, data, mode):
      #debug(msg='loading index data', level=VERBOSE).flush()
      index_data = numpy.array(data, numpy.uint32)
      ibo = vbo.VBO(data=index_data, usage=GL_STATIC_DRAW, target=GL_ELEMENT_ARRAY_BUFFER)
      self._index_buffers.append([ibo, Buffer.RenderModes[mode]])

   def patches(self):
      return [IndexedBuffer.Patch(ibo, mode) for (ibo, mode) in self._index_buffers]

   def draw(self, **kwargs):
      style = kwargs.get('style', 'wireframe')

      glPushAttrib(GL_POLYGON_BIT)
      if style == 'wireframe':
         glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

      self._pre_draw()

      pushMatrix()
      translate(self.origin)

      for ibo, mode in self._index_buffers:
         ibo.bind()
         glDrawElements(mode, len(ibo), GL_UNSIGNED_INT, None)
         ibo.unbind()

      popMatrix()

      self._post_draw()

      glPopAttrib()

   def batch_render(self, func):
      self._pre_draw()
      func()
      self._post_draw()

