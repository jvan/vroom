#!/usr/bin/env vroom

from vroom import *
import math

# Functions

def hit(cursor):
   dist = sum([(a-b)*(a-b) for a,b in zip(Global.position, cursor)])
   return math.sqrt(dist) < Global.size

# vroom callbacks

def init():
   Global.position = [0.0, 0.0, 0.0]
   Global.size = 1.5

   Global.dragging = False
   Global.hover = False

def draw():
   lighting(False)

   if Global.dragging:
      color(red)
   elif Global.hover:
      color(green)
   else:
      color(blue)
   
   pushMatrix()
   translate(Global.position)
   sphere(Global.size)
   popMatrix()

def button_press(cursor):
   print 'button_press: pos={}'.format(cursor)
   if hit(cursor):
      print '!!!!! HIT !!!!!'
      Global.dragging = True
    
def button_release(cursor):
   print 'button_release: pos={}'.format(cursor)
   Global.dragging = False

def motion(cursor):
   if Global.dragging:
      Global.position = cursor
   else:
      Global.hover = hit(cursor) 

