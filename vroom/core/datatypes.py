import numpy

class BooleanOption:
   def __init__(self, state=False):
      self.state = state
   def toggle(self):
      self.state = not self.state
   def __nonzero__(self):
      return self.state

class DynamicArray:
    @staticmethod
    def from_list(data):
        return numpy.array(data, dtype=numpy.float32).reshape(len(data)*len(data[0]))

    @staticmethod
    def function(func):
        def wrapper(data, *args):
            x = data[0::3]
            y = data[1::3]
            z = data[2::3]
            x,y,z = func(x, y, z, *args)
            return numpy.dstack((x,y,z)).reshape(data.shape[0],)
        return wrapper
