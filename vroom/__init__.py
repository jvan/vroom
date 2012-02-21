from application import *
from environment import *
from color import *
from lighting import *
from transform import *
from rendering import *
from typography import *

_App = None

pushMatrix = glPushMatrix
popMatrix = glPopMatrix
pointSize = glPointSize
lineWidth = glLineWidth

from random import random, randrange

def random_vertex(start, stop):
   return [randrange(start, stop) for i in range(3)] 

def random_color():
   return [random() for i in range(3)]

def random_vertex_generator(n, start=-1.0, stop=1.0):
   for i in range(n):
      yield random_vertex(start, stop)

def random_color_generator(n):
   for i in range(n):
      yield random_color()
