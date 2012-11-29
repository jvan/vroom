# System imports

from OpenGL.GLU import gluQuadricTexture, gluDisk

# Vroom imports

from quadric import _get_quadric, _set_draw_style
from settings import DiskRes

def disk(radius, **kwargs):
   ''' Draw a disk with given radius. '''

   # Get any keyword arguments 
   style   = kwargs.get('style', 'wireframe')
   texture = kwargs.get('texture', None)

   quadric = _get_quadric()

   # Setup texture if specified
   if texture:
      style = 'solid'
      gluQuadricTexture(quadric, True)
      texture.bind()
   
   # Set the quadric draw style (line or fill)
   _set_draw_style(style)

   # Draw the disk
   gluDisk(quadric, 0, radius, DiskRes['slices'], DiskRes['loops'])

   # Clean up texture data if specified
   if texture:
      texture.unbind()
      gluQuadricTexture(quadric, False)

