#!/usr/bin/env vroom
from vroom import *

Lighting = True

points = []

def init():
   addMainMenuItem('clear', clearPoints)

def clearPoints():
   global points
   points = []

def draw():
   if not Lighting:
      lighting(False)
      color(0,1,0)
   else:
      material(0,1,0)

   for p in points:
      pushMatrix()
      translate(p)
      if Lighting:
         sphere(1.0, style='solid')
      else:
         sphere(1.0)
      popMatrix()

def button_press(pos):
   print ' -- button_press (pos={})'.format(pos)
   points.append(pos)
