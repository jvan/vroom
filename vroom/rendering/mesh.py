# System imports

from OpenGL.GL import *

# Vroom imports

from vroom.utils.debug import *

from buffers import IndexedBuffer

class Mesh(IndexedBuffer):

   def __init__(self, vertex_data):
      IndexedBuffer.__init__(self, vertex_data=vertex_data)

      self.renderMode('triangles')


