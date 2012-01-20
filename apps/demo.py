#!/usr/bin/env vroom
from vroom import * 

modelAngles = [0.0, 0.0, 0.0]
rotationalSpeeds = [9.0, -31.0, 19.0]
animate = True

def init():
   setMainMenuTitle('Vroom Demo')
   addMainMenuItem('Reset ResetNavigation', centerDisplay)
   addMainMenuItem('Toggle Rotate', toggleRotate, type='toggle')

def toggleRotate():
   global animate
   animate = not animate 

def draw():
   lighting(False);
   color(1.0)

   pushMatrix()
   rotate(modelAngles)
   cube(3.0)
   popMatrix()

def frame():
   if not animate:
      return

   time = elapsedTime()

   global modelAngles
   modelAngles = [(angle+speed*time)%360.0 
                     for (angle, speed) in zip(modelAngles, rotationalSpeeds)]

