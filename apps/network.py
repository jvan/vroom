#!/usr/bin/env vroom
from vroom import *
import networkx

graph = networkx.read_gml('data/polblogs.gml')

nodes = {}
for node in graph.nodes(data=True):
   if node[1]['value'] == 1:
      nodes.setdefault(node[0], (random_vertex(-100,0), 1))
   else:
      nodes.setdefault(node[0], (random_vertex(0, 100), 0))
   
edges = []
for (n1, n2) in graph.edges():
   edges.append(nodes[n1][0])
   edges.append(nodes[n2][0])

edge_array = GLArray(edges)
edge_array.renderMode('lines')

def draw_nodes():
   for (pos, code) in nodes.values():
      if code == 0:
         material(0,0,1)
      else:
         material(1,0,0)

      pushMatrix()
      translate(pos)
      sphere(1.0, style='solid')
      popMatrix()

def draw_edges():
   transparency(True)
   color(1,1,1,0.1)
   edge_array.draw()

def draw():
   draw_nodes()
   lighting(False)
   draw_edges()

