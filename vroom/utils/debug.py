__all__ = ['debug', 'Debug', 'ERROR', 'WARNING', 'STATUS', 'VERBOSE', 'DEBUG'] 
# System imports

import inspect

# Vroom imports

from inspect_utils import get_caller_name

# Debug levels
#
# Debugging messages are assigned a level. Additionally, the program has an 
# assigned debug level. If the program level is greater than or equal to the 
# level of the message the text is displayed. Otherwise the message is 
# suppressed. The levels are ordered with the most critical messages having 
# the lowest values. The lowest possible level would display only error 
# messages. A brief discription of the levels follows:
#
#   ERROR   -- a critical error has occurred a program crash is a likely result
#   WARNING -- the program has encountered something unexpected
#   STATUS  -- used for basic reporting (connected to network, data loaded,
#              etc.)
#   VERBOSE -- additional information generally related to status reports
#              (size of data array, values of varibales, etc.)
#   DEBUG   -- output needed to help during application development
#
# The default program level is STATUS meaning all ERROR, WARNING, and STATUS
# messages will be displayed. If more detailed messages are required the level
# can be changed by calling the set_level function (see below).

(ERROR, WARNING, STATUS, VERBOSE, DEBUG) = range(5)


# Terminal colors

escape = lambda code: '\033[{}m'.format(code)
color  = lambda code: lambda s: escape(code) + s + escape(0)
black  = color(30)
red    = color(31)
green  = color(32)
yellow = color(33)
blue   = color(34)
purple = color(35)
cyan   = color(36)


def debug(msg=None, level=STATUS, indent=0):
   """ Create a debug message.

   Debug messages are created with a level (default STATUS). If the program
   level is greater than or equal to this level the message will be displayed.
   The module, class, and function names are automatically added to the 
   message.

   NOTE: This function returns a Debug object initialized with the specified 
   values; it does not automatically print the message. To print the message
   (conditional on the program's debug level) you must call the flush() method
   of the returned debug object (see examples below):
   
   There are several general patterns for debug messages:

   1. Printing a status message

      debug(msg='loading data from file').flush() # uses default STATUS level

   2. Displaing error or warning messages

      debug(msg='This should not have happened', level=ERROR).flush()

   3. Displaying varibales

      debug(level=VERBOSE).add('filename', filename).flush()

   4. Multiple values can be chained together.

      debug(level=VERBOSE).add('x', x).add('y', y).add('z', z).flush()

   See the Debug class below for more information.

   msg    -- debug message 
   level  -- message debug level (see above)
   indent -- indentation level

   return -- Debug object
   """

   caller_name = get_caller_name(2)
   d = Debug(caller_name, msg, level, indent)
   return d

class Debug:
   """ Debugging message and data object.

   This class is not meant to be used directly. Instead the debug() function 
   above should be called. 
   """

   # Program debug level
   LEVEL = STATUS 

   @staticmethod
   def set_level(level):
      """ Set the program debug level.

      level -- debug level for the program (see above).
      """

      Debug.LEVEL = level


   def __init__(self, caller, msg, level, indent):
      self.caller = caller
      self.msg    = msg
      self.level  = level
      self.indent = indent

      self.args = [] 

   def __str__(self):
      template = '{indent}({caller}{message}{args})'
      s = template.format(indent=self._indentation_text(),
                          caller=self.caller, 
                          message=self._message_text(),
                          args=self._args_text())
      return self._colorize(s)

   # Public interface

   def add(self, label, obj):
      """ Add a variable and label to the argument list.

      label  -- text label (usually the variable name)
      obj    -- data object

      return -- the Debug object (enables chaining) 
      """

      self.args.append((label, obj))
      return self

   def flush(self):
      """ Conditionally print the debug message and data.
      """

      if self.level > Debug.LEVEL:
         return
      print(self)
   
      # Clear the argument list so the object could be re-used
      self.args = []

   # Internal methods

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
      elif self.level == VERBOSE:
         return green(text)
      elif self.level == DEBUG:
         return blue(text)

