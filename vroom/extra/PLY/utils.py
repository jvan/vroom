from parser import Parser
from vroom.rendering.mesh import Mesh, compute_normals

import numpy


def create_mesh(filename, auto_normals=True):

   parser = Parser(filename)

   vertices = [x[:3] for x in parser.vertices]

   indices = []
   for face in parser.faces:
      indices.extend(face)

   #mesh = Mesh(vertices, indices)
   mesh = Mesh(vertices)
   mesh.addIndexData(indices, 'triangles')

   if auto_normals:
      mesh.loadNormalData(compute_normals(parser.vertices, parser.faces))

   return mesh


Mesh.register_initializer('from_ply', create_mesh)
