# System imports

from OpenGL.GLU import gluNewQuadric, gluQuadricDrawStyle, GLU_LINE, GLU_FILL

# These functions and variables are used internally by vroom when rendering
# certain geometric shapes (sphere, cylinder, etc.). Generally they should not
# be used directly by the application.

_Quadric = None # global quadric object

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

