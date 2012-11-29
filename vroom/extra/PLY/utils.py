from parser import Parser
from vroom.rendering.mesh import Mesh

import numpy

def compute_normals(parser):
   print('(compute_normals BEGIN)')

   normals = numpy.array([numpy.zeros(3) for i in range(len(parser.vertices))])

   for n in range(len(parser.faces)):
      i,j,k = parser.faces[n]
      p0 = parser.vertices[i][:3]
      p1 = parser.vertices[j][:3]
      p2 = parser.vertices[k][:3]
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

def create_mesh(parser, auto_normals=True):

   vertices = [x[:3] for x in parser.vertices]

   indices = []
   for face in parser.faces:
      indices.extend(face)

   #mesh = Mesh(vertices, indices)
   mesh = Mesh(vertices)
   mesh.addIndexData(indices, 'triangles')

   if auto_normals:
      mesh.loadNormalData(compute_normals(parser))

   return mesh
