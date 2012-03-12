from OpenGL.GLUT import *
from OpenGL.GL import glPushMatrix, glPopMatrix
from vroom.transform import scale, translate

from point_cloud import *
from misc import *

HasContext = False

SphereRes = { 'slices': 12, 'stacks': 12 }

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

@EnableBatchMode
def cube(*args, **kwargs):
   global HasContext
   if not HasContext:
      glutInit()
      HasContext = True

   glPushMatrix()
   scale(*args)

   style = kwargs.get('style', 'wireframe')
   texture = kwargs.get('texture', None)

   if texture: 
      style = 'solid'

   if style == 'wireframe':
      glutWireCube(1.0)
   elif style == 'solid':
      #glutSolidCube(1.0)

      if type(texture) == dict:
         # top
         texture['top'].bind()
         glBegin(GL_QUADS)

         glNormal3f( 0.0, 0.0, 1.0)
         glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5,  0.5)
         glTexCoord2f(1.0, 0.0); glVertex3f( 0.5, -0.5,  0.5)
         glTexCoord2f(1.0, 1.0); glVertex3f( 0.5,  0.5,  0.5)
         glTexCoord2f(0.0, 1.0); glVertex3f(-0.5,  0.5,  0.5)

         glEnd()

         # bottom
         texture['bottom'].bind()
         glBegin(GL_QUADS)

         glNormal3f( 0.0, 0.0,-1.0)
         glTexCoord2f(1.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
         glTexCoord2f(1.0, 1.0); glVertex3f(-0.5,  0.5, -0.5)
         glTexCoord2f(0.0, 1.0); glVertex3f( 0.5,  0.5, -0.5)
         glTexCoord2f(0.0, 0.0); glVertex3f( 0.5, -0.5, -0.5)

         glEnd()
         
         # sides
         texture['sides'].bind()
         glBegin(GL_QUADS)

         # back
         glNormal3f( 0.0, 1.0, 0.0)
         glTexCoord2f(1.0, 0.0); glVertex3f(-0.5,  0.5, -0.5)
         glTexCoord2f(1.0, 1.0); glVertex3f(-0.5,  0.5,  0.5)
         glTexCoord2f(0.0, 1.0); glVertex3f( 0.5,  0.5,  0.5)
         glTexCoord2f(0.0, 0.0); glVertex3f( 0.5,  0.5, -0.5)

         # front
         glNormal3f( 0.0, -1.0, 0.0)
         glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
         glTexCoord2f(1.0, 0.0); glVertex3f( 0.5, -0.5, -0.5)
         glTexCoord2f(1.0, 1.0); glVertex3f( 0.5, -0.5,  0.5)
         glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, -0.5,  0.5)

         # right
         glNormal3f( 1.0, 0.0, 0.0)
         glTexCoord2f(0.0, 0.0); glVertex3f( 0.5, -0.5, -0.5)
         glTexCoord2f(1.0, 0.0); glVertex3f( 0.5,  0.5, -0.5)
         glTexCoord2f(1.0, 1.0); glVertex3f( 0.5,  0.5,  0.5)
         glTexCoord2f(0.0, 1.0); glVertex3f( 0.5, -0.5,  0.5)

         # left
         glNormal3f(-1.0, 0.0, 0.0)
         glTexCoord2f(1.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
         glTexCoord2f(1.0, 1.0); glVertex3f(-0.5, -0.5,  0.5)
         glTexCoord2f(0.0, 1.0); glVertex3f(-0.5,  0.5,  0.5)
         glTexCoord2f(0.0, 0.0); glVertex3f(-0.5,  0.5, -0.5)

         glEnd()


      else:
         if texture:
            texture.bind()

         glBegin(GL_QUADS)

         # top
         glNormal3f( 0.0, 0.0, 1.0)
         glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5,  0.5)
         glTexCoord2f(1.0, 0.0); glVertex3f( 0.5, -0.5,  0.5)
         glTexCoord2f(1.0, 1.0); glVertex3f( 0.5,  0.5,  0.5)
         glTexCoord2f(0.0, 1.0); glVertex3f(-0.5,  0.5,  0.5)

         # bottom
         glNormal3f( 0.0, 0.0,-1.0)
         glTexCoord2f(1.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
         glTexCoord2f(1.0, 1.0); glVertex3f(-0.5,  0.5, -0.5)
         glTexCoord2f(0.0, 1.0); glVertex3f( 0.5,  0.5, -0.5)
         glTexCoord2f(0.0, 0.0); glVertex3f( 0.5, -0.5, -0.5)
         
         # sides

         # back
         glNormal3f( 0.0, 1.0, 0.0)
         glTexCoord2f(1.0, 0.0); glVertex3f(-0.5,  0.5, -0.5)
         glTexCoord2f(1.0, 1.0); glVertex3f(-0.5,  0.5,  0.5)
         glTexCoord2f(0.0, 1.0); glVertex3f( 0.5,  0.5,  0.5)
         glTexCoord2f(0.0, 0.0); glVertex3f( 0.5,  0.5, -0.5)

         # front
         glNormal3f( 0.0, -1.0, 0.0)
         glTexCoord2f(0.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
         glTexCoord2f(1.0, 0.0); glVertex3f( 0.5, -0.5, -0.5)
         glTexCoord2f(1.0, 1.0); glVertex3f( 0.5, -0.5,  0.5)
         glTexCoord2f(0.0, 1.0); glVertex3f(-0.5, -0.5,  0.5)

         # right
         glNormal3f( 1.0, 0.0, 0.0)
         glTexCoord2f(0.0, 0.0); glVertex3f( 0.5, -0.5, -0.5)
         glTexCoord2f(1.0, 0.0); glVertex3f( 0.5,  0.5, -0.5)
         glTexCoord2f(1.0, 1.0); glVertex3f( 0.5,  0.5,  0.5)
         glTexCoord2f(0.0, 1.0); glVertex3f( 0.5, -0.5,  0.5)

         # left
         glNormal3f(-1.0, 0.0, 0.0)
         glTexCoord2f(1.0, 0.0); glVertex3f(-0.5, -0.5, -0.5)
         glTexCoord2f(1.0, 1.0); glVertex3f(-0.5, -0.5,  0.5)
         glTexCoord2f(0.0, 1.0); glVertex3f(-0.5,  0.5,  0.5)
         glTexCoord2f(0.0, 0.0); glVertex3f(-0.5,  0.5, -0.5)

         glEnd()

         if texture:
            texture.unbind()
         
   else:
      raise Exception('vroom.cube: invalid style value')

   glPopMatrix()

@EnableBatchMode
def sphere(radius, **kwargs):
   global HasContext
   if not HasContext:
      glutInit()
      HasContext = True

   style = kwargs.get('style', 'wireframe')

   if style == 'wireframe':
      glutWireSphere(radius, SphereRes['slices'], SphereRes['stacks'])
   elif style == 'solid':
      glutSolidSphere(radius, SphereRes['slices'], SphereRes['stacks'])
   else:
      raise Exception('vroom.cube: invalid style value')

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


def line(p1, p2):
   glBegin(GL_LINES)
   glVertex3fv(p1)
   glVertex3fv(p2)
   glEnd()

