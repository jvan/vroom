#!/usr/bin/env vroom
from vroom import *

NUM_POINTS = 10000

vertices = list(random_vertex_generator(NUM_POINTS, -100.0, 100.0))
colors = list(random_color_generator(NUM_POINTS))

points = None

def gl_init():
   global points
   points = PointCloud(vertices, colors)
   points.sprite('share/particle.bmp')

def draw():
   lighting(False)
   points.draw()
