import struct
import sys

class Property:
   types = { 'float': float, 'int': int, 'uchar': int }

   def __init__(self, prop_type, prop_name):
      self._type = prop_type
      self.name = prop_name

   def __str__(self):
      return '(property type={}; name={})'.format(self._type, self.name)

   def get_type(self):
      return Property.types[self._type]

   def convert(self, data):
      #print('(Property.convert data={})'.format(data))
      if self._type.startswith('list'):
         count = int(data.pop(0))
         ptype = self._type.split()[-1]
         vals = []
         for i in range(count):
            vals.append(Property.types[ptype](data.pop(0)))
         #return map(Property.types[ptype], data)
         return vals
      else:
         return Property.types[self._type](data.pop(0))

   def convert_binary(self, file):
      if self._type.startswith('list'):
         count = struct.unpack('<B', file.read(1))[0]
         ptype = self._type.split()[-1]
         fmt_string = '>'
         size = 0
         if ptype == 'float':
            fmt_string += 'f' * count
            size = 4 * count
         elif ptype == 'int':
            fmt_string += 'i' * count
            size = 4 * count
         return struct.unpack(fmt_string, file.read(size))
      else:
         if self._type == 'float':
            fmt_string = '>f'
            size = 4
            return struct.unpack(fmt_string, file.read(size))[0]


class Element:

   def __init__(self, name, size):
      self.properties =[]
      self.name = name
      self.size = size

   def add_property(self, prop):
      self.properties.append(prop)

   def __str__(self):
      s = '(element name={}; size={}; properties={})\n'.format(self.name, self.size, len(self.properties))
      for prop in self.properties:
         s += '  {}\n'.format(prop)
      return s

   def get(self, row):
      elems = row.split()
      return [p.convert(elems) for p in self.properties]

   def get_binary(self, file):
      #return [p.convert_binary(file)[0] for p in self.properties] 
      return [p.convert_binary(file) for p in self.properties] 

