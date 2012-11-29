from OpenGL.GL import glColor4fv
#from Vrui import setBackgroundColor
import pyvrui
from matplotlib import pylab

red   = [1.0, 0.0, 0.0]
green = [0.0, 1.0, 0.0]
blue  = [0.0, 0.0, 1.0]
white = [1.0, 1.0, 1.0]
black = [0.0, 0.0, 0.0]

class Color:

   def __init__(self, r=1.0, g=1.0, b=1.0, a=1.0):
      self.r = r
      self.g = g
      self.b = b
      self.a = a

   def __str__(self):
      return '({}, {}, {}, {})'.format(self.r, self.g, self.b, self.a)

   def data(self):
      return [self.r, self.g, self.b, self.a]

   @staticmethod
   def helper(*args):
      num_args = len(args)

      if num_args == 1:
         if type(args[0]) == list:
            return Color.generate_from_list(args[0])
         else:
            return Color.generate_from_grey(args[0])
      elif num_args == 3:
         r, g, b = args
         return Color(r, g, b)
      elif num_args == 4:
         r, g, b, a = args
         return Color(r, g, b, a)
      else:
         raise Exception('Color.helper: invalid number of arguments')

   @staticmethod
   def generate_from_list(values):
      if len(values) == 3:
         r, g, b = values
         return Color(r, g, b)
      elif len(values) == 4:
         r, g, b, a = values
         return Color(r, g, b, a)
      else:
         raise Exception('Color.generate_from_list: invalide array size')

   @staticmethod
   def generate_from_grey(value):
      return Color(value, value, value)

def color(*args):
   ''' Set the current color.

   syntax:
      color(gray)
      color(r,g,b)
      color(r,g,b,a)
      color([r,g,b])
      color([r,g,b,a])
   '''
   c = Color.helper(*args)
   glColor4fv(c.data())

class ColorMap:

   def __init__(self, name='RdBu'):
      self.cm = pylab.cm.get_cmap(name)

   def __getitem__(self, index):
      return self.cm(index)
     
   def __call__(self, index, count, alpha=1.0):
      i = int(255.0*index/count)
      color = list(self.cm(i))
      color[3] = alpha
      return color


def background(*args):
   c = Color.helper(*args).data()
   print ' -- background(color={})'.format(c)
   # TODO: GLColor not implemented in PyVrui
   return
   bg = pyvrui.GLColor(c)
   pyvrui.setBackgroundColor(bg)

