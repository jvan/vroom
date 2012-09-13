from OpenGL.GL import *
from OpenGL.arrays import vbo
import numpy

from batch_mode import EnableBatchMode
from vroom.transform import scale

class Cube:

   vertices = [
      [0.0, 0.0, 0.0],
      [1.0, 0.0, 0.0],
      [1.0, 1.0, 0.0],
      [0.0, 1.0, 0.0],
      [0.0, 0.0, 1.0],
      [1.0, 0.0, 1.0],
      [1.0, 1.0, 1.0],
      [0.0, 1.0, 1.0]
   ]

   normals = [
       [ 1.0,  0.0,  0.0], 
       [-1.0,  0.0,  0.0],
       [ 0.0,  1.0,  0.0],
       [ 0.0, -1.0,  0.0],
       [ 0.0,  0.0,  1.0],
       [ 0.0,  0.0, -1.0]
   ]

   texcoords = [
      [0.0, 0.0],
      [1.0, 0.0],
      [1.0, 1.0],
      [0.0, 1.0]
   ]

   vertex_indices = [
      0, 1, 5, 4, # front
      1, 2, 6, 5, # right  
      2, 3, 7, 6, # back
      3, 0, 4, 7, # left
      4, 5, 6, 7, # top
      1, 0, 3, 2  # bottom
   ]

   normal_indices = [
      3, 3, 3, 3,
      0, 0, 0, 0,
      2, 2, 2, 2,
      1, 1, 1, 1,
      4, 4, 4, 4,
      5, 5, 5, 5
   ]

   texcoord_indices = [
      0, 1, 2, 3,
      0, 1, 2, 3,
      0, 1, 2, 3,
      0, 1, 2, 3,
      0, 1, 2, 3,
      0, 1, 2, 3
   ]

   def __init__(self):

      def generate_data(data, indices):
         output = []
         for i in indices:
            output.extend(data[i])
         return output

      create_vbo = lambda x: vbo.VBO(data=numpy.array(x, dtype=numpy.float32), usage=GL_STATIC_DRAW, target=GL_ARRAY_BUFFER)
      create_ibo = lambda x: vbo.VBO(data=numpy.array(x, dtype=numpy.short),   usage=GL_STATIC_DRAW, target=GL_ELEMENT_ARRAY_BUFFER)

      vertex_data = generate_data(Cube.vertices, Cube.vertex_indices)
      normal_data = generate_data(Cube.normals, Cube.normal_indices)
      texture_data = generate_data(Cube.texcoords, Cube.texcoord_indices)

      self.vertex_buffer = create_vbo(vertex_data)
      self.normal_buffer = create_vbo(normal_data)
      self.texture_buffer = create_vbo(texture_data)

   def _pre_render(self):
      glPushClientAttrib(GL_CLIENT_VERTEX_ARRAY_BIT)

      glEnableClientState(GL_VERTEX_ARRAY)
      glEnableClientState(GL_NORMAL_ARRAY)
      glEnableClientState(GL_TEXTURE_COORD_ARRAY)

      self.normal_buffer.bind()
      glNormalPointer(GL_FLOAT, 0, None)

      self.texture_buffer.bind()
      glTexCoordPointer(2, GL_FLOAT, 0, None)

      self.vertex_buffer.bind()
      glVertexPointer(3, GL_FLOAT, 0, None)

   def _post_render(self):
      self.normal_buffer.unbind()
      self.texture_buffer.unbind()
      self.vertex_buffer.unbind()

      glPopClientAttrib()
      
   def render_function(f):
      def wrapper(self):
         self._pre_render()
         f(self)
         self._post_render()
      return wrapper

   @render_function
   def draw_sides(self):
      glDrawArrays(GL_QUADS, 0, 16) 

   @render_function
   def draw_top(self):
      glDrawArrays(GL_QUADS, 16, 4)

   @render_function
   def draw_bottom(self):
      glDrawArrays(GL_QUADS, 20, 24)

   @render_function
   def draw(self):
      glDrawArrays(GL_QUADS, 0, len(self.vertex_buffer)/3)

_Cube = Cube()

@EnableBatchMode
def cube(*args, **kwargs):

   glPushMatrix()
   scale(*args)

   style = kwargs.get('style', 'wireframe')
   texture = kwargs.get('texture', None)

   if texture: 
      style = 'solid'

   if style == 'wireframe':      
      glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
      glDisable(GL_CULL_FACE)
      _Cube.draw()
      glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
      glEnable(GL_CULL_FACE)

   elif style == 'solid':

      if type(texture) == dict:
         texture['top'].bind()
         _Cube.draw_top()

         texture['bottom'].bind()
         _Cube.draw_bottom()

         texture['sides'].bind()
         _Cube.draw_sides()

      else:
         if texture:
            texture.bind()

         _Cube.draw()

         if texture:
            texture.unbind()
         
   else:
      raise Exception('vroom.cube: invalid style value')

   glPopMatrix()


