from OpenGL.GLU import gluSphere, gluQuadricTexture

from batch_mode import EnableBatchMode
from quadric import _get_quadric, _set_draw_style
from settings import SphereRes

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


