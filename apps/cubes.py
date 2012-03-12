#!/usr/bin/env vroom

from vroom import *

# Functions

def toggleLighting():
   Global.UseLighting = not Global.UseLighting

def toggleColor():
   Global.UseColor = not Global.UseColor

def setColor(c):
   c = c if Global.UseColor else c[0]
   material(c) if Global.UseLighting else color(c)

# vroom callbacks

def init():
   setMainMenuTitle('Cubes')
   addMainMenuItem('Lighting', toggleLighting, type='toggle')
   addMainMenuItem('Color', toggleColor, type='toggle')

   Global.UseLighting = False
   Global.UseColor = False

   NUM_CUBES = 1000
   Global.vertices = list(random_vertex_generator(NUM_CUBES, -100.0, 100.0))
   Global.colors = list(random_color_generator(NUM_CUBES))
   
def draw():
   lighting(Global.UseLighting)
   
   cube_style = 'solid' if Global.UseLighting else 'wireframe'

   for (v,c) in zip(Global.vertices, Global.colors):
      pushMatrix()
      translate(v)
      setColor(c)
      cube(3.0, style=cube_style)
      popMatrix()

