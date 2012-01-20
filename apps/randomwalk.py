#!/usr/bin/env vroom
from vroom import *

MAX_POINTS = 500

points = [[0.0, 0.0, 0.0]]
buffer = None

colors = []
color_map = ColorMap()

def gl_init():
   global points
   global buffer
   
   buffer = GLArray(points)
   buffer.renderMode(GL_LINE_STRIP)

def draw():
   lighting(False)
   glEnable(GL_BLEND)
   glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
   lineWidth(3.0)
   buffer.draw()
   
def frame():
   global points
   global buffer

   current_pos = points[-1]
   random_step = lambda: -1 if random() < 0.5 else 1
   steps = [random_step() for i in range(3)]
   next_pos = [pos+step for (pos, step) in zip(current_pos, steps)]

   points.append(next_pos)
   if len(points) > MAX_POINTS:
      points.pop(0)

   global colors
   count = len(points)
   colors = [color_map(i, count) for i in range(count)]
   
   buffer = GLArray(points, colors)
   buffer.renderMode(GL_LINE_STRIP)
   
