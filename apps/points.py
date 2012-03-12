#!/usr/bin/env vroom

from vroom import *

# vroom callbacks

def gl_init():
   NUM_POINTS = 10000
   vertices = list(random_vertex_generator(NUM_POINTS, -100.0, 100.0))
   colors = list(random_color_generator(NUM_POINTS))

   Global.points = PointCloud(vertices, colors)

   textureFile = get_resource('particle.bmp')
   Global.points.sprite(textureFile)

def draw():
   lighting(False)
   Global.points.draw()

