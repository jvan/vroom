from core import Element, Property

class Parser:

   def __init__(self, filename):
      self.file = open(filename)
      print('(Parser:__init__ filename={})'.format(filename))

      self._callbacks = {
            'vertex': self._process_vertex_data,
            'face':   self._process_face_data
            }

      self.elements = []

      self._parse_header()
      self._parse_body()

      print('(Parser:__init__ END)') 

   def __str__(self):
      return '\n'.join('{}'.format(elem) for elem in self.elements)

   def _parse_header(self):
      print('(Parser:_parse_header BEGIN)')
      element = None
      while True:
         line = self.file.readline().strip()
         print('  [header] {}'.format(line))
         if line == 'end_header':
            break
         elems = line.split()
         if elems[0] == 'format':
            self.format = elems[1]
         elif elems[0] == 'element':
            if element:
               self.elements.append(element)
            name, size = elems[1:3]
            element = Element(name, int(size))
         elif elems[0] == 'property':
            prop_type, prop_name = ' '.join(elems[1:-1]), elems[-1]
            element.add_property(Property(prop_type, prop_name))
      self.elements.append(element)
      print('(PLYParser:_parse_header END)')

   def _parse_body(self):
      print('(Parser:_parse_body BEGIN)')
      for elem in self.elements:
         print('  [body] parsing {}'.format(elem.name))
         try:
            self._callbacks[elem.name](elem) 
         except KeyError:
            print('  !! WARNING: no callback for \'{}\' element !!'.format(elem.name))
      print('(Parser:_parse_body END)')

   def _process_vertex_data(self, elem):
      print('(Parser:_process_vertex_data BEGIN)')
      self.vertices = []
      if self.format == 'ascii':
         for row in range(elem.size):
            self.vertices.append(elem.get(self.file.readline()))
      elif self.format == 'binary_big_endian':
         for row in range(elem.size):
            vertex = elem.get_binary(self.file)
            self.vertices.append(vertex)
      print('(Parser:_process_vertex_data END)')

   def _process_face_data(self, elem):
      print('(Parser:_process_face_data BEGIN)')
      self.faces = []
      if self.format == 'ascii':
         for row in range(elem.size):
            indices = elem.get(self.file.readline())
            #print(' ** indices={} **'.format(indices))
            self.faces.extend(indices)
      elif self.format == 'binary_big_endian':
         for row in range(elem.size):
            indices = elem.get_binary(self.file)
            #print('indices={}'.format(indices))
            #self.faces.extend(indices[0])
            self.faces.append(*indices)
      print('(Parser:_process_face_data END)')
      print('===== FACES ==============================') 
      for i in range(6):
         print self.faces[i]
      print('==========================================')

