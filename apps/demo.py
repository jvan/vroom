#!/usr/bin/env vroom

from vroom import * 

# Functions

def toggleRotate():
   Global.animate = not Global.animate

# vroom callbacks

def init():
   setMainMenuTitle('Vroom Demo')
   addMainMenuItem('Reset ResetNavigation', centerDisplay)
   addMainMenuItem('Toggle Rotate', toggleRotate, type='toggle')

   Global.animate = False
   Global.modelAngles = [0.0, 0.0, 0.0]

def draw():
   lighting(False);
   color(1.0)

   pushMatrix()
   rotate(Global.modelAngles)
   cube(4.0)
   popMatrix()

def frame():
   if not Global.animate:
      return

   time = elapsedTime()
   rotationalSpeeds = [9.0, -31.0, 19.0]

   Global.modelAngles = [(angle+speed*time)%360.0 
                     for (angle, speed) in zip(Global.modelAngles, rotationalSpeeds)]

