#!/usr/bin/env vroom
from vroom import *

# vroom callbacks

def init():

   vertices = []
   colors = []

   filename = get_resource('earthquakes-2010.dat')
   data = open(filename).readlines()[2:]

   Global.labels = []

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
         Global.labels.append(('{:.1f}'.format(magnitude), epicenter))

   Global.points = PointCloud(vertices, colors)
   Global.center = [-1.0*x for x in Global.points.center()]

def gl_init():
   spriteFile = get_resource('particle.bmp')
   Global.points.sprite(spriteFile)

   fontFile = get_resource('fonts/DroidSans.ttf')
   textFont(fontFile)

def draw():
   lighting(False)

   pushMatrix()
   translate(Global.center)

   Global.points.draw()

   for (label, pos) in Global.labels:
      text(label, pos)

   popMatrix()

