from OpenGL.GLUT import *
from vroom.transform import scale

from point_cloud import *

HasContext = False

SphereRes = { 'slices': 12, 'stacks': 12 }

def cube(*args, **kwargs):
   global HasContext
   if not HasContext:
      glutInit()
      HasContext = True

   scale(*args)

   style = kwargs.get('style', 'wireframe')

   if style == 'wireframe':
      glutWireCube(1.0)
   elif style == 'solid':
      glutSolidCube(1.0)
   else:
      raise Exception('vroom.cube: invalid style value')

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
