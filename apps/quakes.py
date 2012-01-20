#!/usr/bin/env vroom
from vroom import *

data = open('data/earthquakes-2010.dat').readlines()[2:]

vertices = []
labels = []
colors = []
center = []

for row in data:
   elems = row.split()
   epicenter = map(float, elems[2:5]) 
   vertices.append(epicenter)

   magnitude = float(elems[5])
   if magnitude > 3.5:
      colors.append([1.0, 0.0, 0.0, 0.4])
   else:
      colors.append([0.0, 1.0, 0.0, 0.4])

   if magnitude > 4.0:
      labels.append(('{:.1f}'.format(magnitude), epicenter))

def gl_init():
   global points
   points = PointCloud(vertices, colors)
   points.sprite('share/particle.bmp')
   global center
   center = [-1.0*x for x in points.center()]

   textFont('share/fonts/DroidSans.ttf')

def draw():
   lighting(False)
   pushMatrix()
   translate(center)
   points.draw()

   for (txt, pos) in labels:
      text(txt, pos[0], pos[1], pos[2])

   popMatrix()
