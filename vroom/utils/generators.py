# System imports

from random import random, randrange

def random_vertex(start, stop):
   ''' Return a random [x,y,z] value in the range (start, stop).'''

   return [randrange(start, stop, _int=float) for i in range(3)] 

def random_color():
   ''' Return a random [r,g,b] value in the range (0, 1).'''

   return [random() for i in range(3)]

def random_vertex_generator(n, start=-1.0, stop=1.0):
   ''' Generator for creating n random vertices.

   Returns a generator that creates vertex values randomly distributed inside
   a cube. For example, the following code will generate 10,000 random vertices
   with values from -100.0 to 100.0:

      vertices = list(random_vertex_generator(10000, -100.0, 100.0))
   
   n      -- number of vertices
   start  -- minimum value for vertex elements
   stop   -- maximum value for vertex elements
   
   return -- generator object
   '''

   for i in range(n):
      yield random_vertex(start, stop)

def random_color_generator(n, type='rgb'):
   ''' Generator for creating n random color values.
   
   Returns a generator that creates random color values. Both RGB and greyscale
   colors can be returned depending on the type specified.

   To generate 500 RGB color values:

      colors = list(random_color_generator(500))

   To generate 500 greyscale values:
      
      colors = list(random_color_generator(500, type='greyscale'))

   n      -- number of color values 
   type   -- type of color values (must be either 'RGB' or 'greyscale')

   return -- generator object
   '''

   if type == 'rgb':
      for i in range(n):
         yield random_color()
   elif type == 'greyscale':
      for i in range(n):
         yield random()
