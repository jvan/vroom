import inspect

(ERROR, WARNING, STATUS, DEBUG, VERBOSE) = range(5)

escape = lambda code: '\033[{}m'.format(code)
color  = lambda code: lambda s: escape(code) + s + escape(0)
black  = color(30)
red    = color(31)
green  = color(32)
yellow = color(33)
blue   = color(34)
purple = color(35)
cyan   = color(36)

from inspect_utils import get_caller_name

def debug(indent=0, msg=None, level=STATUS):
   caller_name = get_caller_name(2)
   d = Debug(caller_name, indent, msg, level)
   return d

class Debug:

   LEVEL = STATUS

   @staticmethod
   def set_level(level):
      Debug.LEVEL = level

   def __init__(self, caller, indent=0, msg=None, level=STATUS):
      self.indent = indent
      self.caller = caller
      self.msg = msg
      self.args = [] 
      self.level = level

   def add(self, label, obj):
      self.args.append((label, obj))
      return self

   def __str__(self):
      s = '{}({}{}{})'.format(self._indentation_text(),
                               self.caller, 
                               self._message_text(),
                               self._args_text())

      return self._colorize(s)

   def flush(self):
      if self.level > Debug.LEVEL:
         return
      print(self)
      self.args = []

   def _indentation_text(self):
      tab = '  '
      return tab * self.indent

   def _message_text(self):
      if not self.msg:
         return ''
      return ':{}'.format(self.msg)

   def _args_text(self):
      if len(self.args) == 0:
         return ''
      return ' ' + '; '.join('{}={}'.format(k,v) for k,v in self.args)

   def _colorize(self, text):
      if self.level == ERROR:
         return red(text)
      elif self.level == WARNING:
         return yellow(text)
      elif self.level == STATUS:
         return cyan(text)
      elif self.level == DEBUG:
         return green(text)
      elif self.level == VERBOSE:
         return blue(text)

