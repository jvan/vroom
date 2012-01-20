#!/usr/bin/env vroom
from vroom import *

NUM_CUBES = 1000

vertices = list(random_vertex_generator(NUM_CUBES, -100.0, 100.0))

colors = list(random_color_generator(NUM_CUBES))

UseLighting = False
UseColor = False

def init():
   addMainMenuItem('Lighting', toggleLighting, type='toggle')
   addMainMenuItem('Color', toggleColor, type='toggle')

def toggleLighting():
   global UseLighting
   UseLighting = not UseLighting

def toggleColor():
   global UseColor
   UseColor = not UseColor

def draw():
   lighting(UseLighting)
   
   cube_style = 'solid' if UseLighting else 'wireframe'

   for (v,c) in zip(vertices,colors):
      pushMatrix()
      translate(v)

      if UseColor:
         color_value = c
      else:
         color_value = c[0]

      if UseLighting:
         material(color_value)
      else:
         color(color_value)
         
      cube(1.0, style=cube_style)

      popMatrix()

