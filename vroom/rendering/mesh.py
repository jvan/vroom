# System imports

from OpenGL.GL import *

# Vroom imports

from vroom.utils.debug import *

from buffers import IndexedBuffer

import numpy

def compute_normals(vertices, faces):
   print('(compute_normals BEGIN)')

   normals = numpy.array([numpy.zeros(3) for i in range(len(vertices))])

   for n in range(len(faces)):
      i,j,k = faces[n]
      p0 = vertices[i][:3]
      p1 = vertices[j][:3]
      p2 = vertices[k][:3]
      v1 = numpy.array(p1) - numpy.array(p0)
      v2 = numpy.array(p2) - numpy.array(p0)
      norm = numpy.cross(v1, v2)
      normals[i] += norm
      normals[j] += norm
      normals[k] += norm
   
   print('  (normalizing vectors)')

   lengths = numpy.sqrt(normals[:,0]**2 + normals[:,1]**2 + normals[:,2]**2)

   normals[:,0] /= lengths
   normals[:,1] /= lengths
   normals[:,2] /= lengths 

   print('(compute_normals END)')
   return numpy.nan_to_num(normals)

class Mesh(IndexedBuffer):

   def __init__(self, vertex_data):
      IndexedBuffer.__init__(self, vertex_data=vertex_data)

      self.renderMode('triangles')

   @staticmethod
   def register_initializer(name, func):
       setattr(Mesh, name, staticmethod(func))

   @staticmethod
   def from_gridded_data(vertices):
      
      # Compute indices for surface faces.
      #
      # In order to use the existing mesh support in vroom we need to generate
      # indices for gridded data. For each cell two triangles are generated,
      # basically mimicing a triangle strip. This data can then be combined with
      # the vertex data to automatically generate normal vectors.
      def initialize_face_data(nx, ny):
         data = [] # list containing the index indices

         for row in range(ny-1):
            for col in range(nx-1):
               a = nx * row + col
               b = a + nx

               # Each cell is defined by two triangles.
               data.append([a, b, b+1])
               data.append([a, b+1, a+1])

         return data

      # Compute grid dimensions.
      # NOTE: This should be moved into the vroom initialization code.
      ny = len([x for x in vertices if x[0] == vertices[0][0]])
      nx = len(vertices) / ny

      # TODO: The code below for initializing the Mesh object should be moved
      # into vroom. Eventually the code should be reduced to something like this:
      #
      #    Global.surface = Mesh.from_gridded_data(vertices, nx, ny)
      #    Global.surface.compute_normals()
      #

      # The faces (index data) of the surface can be automatically generated from
      # the grid dimensions.
      # TODO: Move initialize_face_data function to vroom library. See below for 
      # details about Mesh object initialization.
      faces = initialize_face_data(nx, ny)

      # The index data needs to be flattened before adding to the buffer object.
      # NOTE: Ideally this step would not be necessary and would be handled by
      # the Mesh contructor.
      indices = []
      for face in faces:
          indices.extend(face)

      # Use a Mesh (IndexedBuffer) to model the surface.
      surface = Mesh(vertices)
      surface.addIndexData(indices, 'triangles')

      # Compute normal vectors and add it to the buffer object.
      # TODO: Move compute_normals() function to Mesh class. Ideally creating a
      # Mesh object would look something like the following:
      #
      #    Global.surface = Mesh(vertices, indices)
      #    Global.surface.compute_normals()
      #
      # Alternatively, the normal vector calculation could be passed as a 
      # parameter to the constructor.
      #
      #    Global.surface = Mesh(vertices, indices, compute_normals=True)
      #
      # Gridded data could be initialized by a static method on the Mesh class.
      # 
      #    Global.surface = Mesh.from_gridded_data(vertices, nx, ny)
      #
      surface.loadNormalData(compute_normals(vertices, faces))

      return surface
