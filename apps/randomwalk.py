#!/usr/bin/env vroom

from vroom import *

# vroom callbacks

def gl_init():
   Global.MAX_POINTS = 500

   Global.points = [[0.0, 0.0, 0.0] for i in range(Global.MAX_POINTS)] 

   color_map = ColorMap()
   Global.colors = [color_map(Global.MAX_POINTS-i, Global.MAX_POINTS) 
         for i in range(Global.MAX_POINTS)]
   
   Global.buffer = GLArray(Global.points)
   Global.buffer.renderMode(GL_LINE_STRIP)

def draw():
   lighting(False)
   lineWidth(3.0)
   Global.buffer.draw()
   
def frame():
   current_pos = Global.points[-1]
   
   random_step = lambda: -1 if random() < 0.5 else 1
   steps = [random_step() for i in range(3)]

   next_pos = [pos+step for (pos, step) in zip(current_pos, steps)]

   Global.points.append(next_pos)

   if len(Global.points) > Global.MAX_POINTS:
      Global.points.pop(0)

   Global.buffer = GLArray(Global.points, Global.colors[:len(Global.points)])
   Global.buffer.renderMode(GL_LINE_STRIP)
   
