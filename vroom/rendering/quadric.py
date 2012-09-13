from OpenGL.GLU import gluNewQuadric, gluQuadricDrawStyle, GLU_LINE, GLU_FILL

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

