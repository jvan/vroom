from OpenGL.GLU import *
from OpenGL.GL import glPushMatrix, glPopMatrix
from vroom.transform import scale, translate, translateZ

from point_cloud import *
from misc import *

from OpenGL.arrays import vbo
import numpy

_Quadric = None

def _get_quadric():
   global _Quadric
   if not _Quadric:
      _Quadric = gluNewQuadric()
   return _Quadric

def _set_draw_style(style):
   global _Quadric
   if style == 'wireframe':
      gluQuadricDrawStyle(_Quadric, GLU_LINE)
   elif style == 'solid':
      gluQuadricDrawStyle(_Quadric, GLU_FILL)

SphereRes   = { 'slices': 12, 'stacks': 12 }
CylinderRes = { 'slices': 12, 'stacks': 4 }
DiskRes = { 'slices': 12, 'loops': 4 }

class BatchRenderer:
   def __init__(self, callback):
      self._callback = callback

   def __call__(self, points, *args, **kwargs):
      for p in points:
         glPushMatrix()
         translate(p)
         self._callback(*args, **kwargs)
         glPopMatrix()

def EnableBatchMode(func):
   func.for_each = BatchRenderer(func)
   return func


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

@EnableBatchMode
def sphere(radius, **kwargs):

   quadric = _get_quadric()

   texture = kwargs.get('texture', None)
   style = kwargs.get('style', 'wireframe')

   #if style == 'wireframe':
      #glutWireSphere(radius, SphereRes['slices'], SphereRes['stacks'])
   #elif style == 'solid':
      #glutSolidSphere(radius, SphereRes['slices'], SphereRes['stacks'])
   #else:
      #raise Exception('vroom.cube: invalid style value')
   
   if texture:
      style = 'solid'
      gluQuadricTexture(quadric, True)
      texture.bind()
   else:
      gluQuadricTexture(quadric, False)
   _set_draw_style(style)

   gluSphere(quadric, radius, SphereRes['slices'], SphereRes['stacks'])

   if texture:
      texture.unbind()

def sphereDetail(*args):
   ''' Adjust resolution of sphere.

   syntax:
      sphereDetail(res)
      sphereDetail(ures, vres)
   '''
   if len(args) == 1:
      SphereRes['slices'] = args[0]
      SphereRes['stacks'] = args[0]
   else:
      SphereRes['slices'] = args[0]
      SphereRes['stacks'] = args[1]

def cylinder(radius, height, **kwargs):
   quadric = _get_quadric()
   texture = kwargs.get('texture', None)
   style = kwargs.get('style', 'wireframe')
   if texture:
      style = 'solid'
      gluQuadricTexture(quadric, True)
      texture.bind()
   else:
      gluQuadricTexture(quadric, False)
   _set_draw_style(style)
   glFrontFace(GL_CW)
   #disk(radius, texture=texture)
   gluDisk(quadric, 0, radius, DiskRes['slices'], DiskRes['loops'])
   glFrontFace(GL_CCW)
   gluCylinder(quadric, radius, radius, height, CylinderRes['slices'], CylinderRes['stacks'])
   glPushMatrix()
   translateZ(height)
   #disk(radius, texture=texture)
   gluDisk(quadric, 0, radius, DiskRes['slices'], DiskRes['loops'])
   glPopMatrix()
   if texture:
      texture.unbind()

def disk(radius, **kwargs):
   quadric = _get_quadric()
   texture = kwargs.get('texture', None)
   style = kwargs.get('style', 'wireframe')
   if texture:
      style = 'solid'
      gluQuadricTexture(quadric, True)
      texture.bind()
   else:
      gluQuadricTexture(quadric, False)
   _set_draw_style(style)
   gluDisk(quadric, 0, radius, DiskRes['slices'], DiskRes['loops'])
   if texture:
      texture.unbind()

def line(p1, p2):
   glBegin(GL_LINES)
   glVertex3fv(p1)
   glVertex3fv(p2)
   glEnd()

