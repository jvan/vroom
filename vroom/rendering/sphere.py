# System imports

from OpenGL.GLU import gluSphere, gluQuadricTexture

# Vroom imports

from batch_mode import EnableBatchMode
from quadric import _get_quadric, _set_draw_style
from settings import SphereRes

@EnableBatchMode
def sphere(radius, **kwargs):
   ''' Draw a sphere with the given radius.'''

   # Get any keyword arguments
   style = kwargs.get('style', 'wireframe')
   texture = kwargs.get('texture', None)

   quadric = _get_quadric()

   # Setup texture if specified
   if texture:
      style = 'solid'
      gluQuadricTexture(quadric, True)
      texture.bind()
   
   # Setup the quadric draw style (line or fill)
   _set_draw_style(style)

   # Draw the sphere
   gluSphere(quadric, radius, SphereRes['slices'], SphereRes['stacks'])

   # Clean up texture data if specified
   if texture:
      texture.unbind()
      gluQuadricTexture(quadric, False)

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

