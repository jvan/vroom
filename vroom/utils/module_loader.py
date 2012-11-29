# System imports

import os
import sys
import imp

# Vroom imports

import vroom.core.environment as env

from debug import *

def _get_module():
   mod = imp.load_source(env._Module_Name, env._App_Fullpath)
   return mod

def load_module(filename):
   ''' Load a vroom (python) module.

   This function and the reload_module() function below are used internally by
   vroom. The application should not need to deal with these functions
   directly.
   '''

   debug(msg='setting application path').flush()

   # Get the absolute path to the application
   env._App_Fullpath = os.path.abspath(filename)

   # Get the path to the application's root directory. This path is used when
   # when (re)loading the module and when searching for resources.
   env._App_Path = os.path.dirname(env._App_Fullpath)

   debug(level=VERBOSE, indent=1).add('_App_Path', env._App_Path).flush()
   debug(level=VERBOSE, indent=1).add('_App_Fullpath', env._App_Fullpath).flush()

   # Set the directories used when searching for resources
   env._Resource_Paths = [env._App_Path, '/usr/local/share/vroom']

   # Get the name of the module (basename without file extension)
   env._Module_Name = os.path.basename(filename)
   env._Module_Name = os.path.splitext(env._Module_Name)[0]

   debug(msg='importing {} application'.format(env._Module_Name)).flush()

   try:
      mod = _get_module()
   except ImportError:
      debug(msg='could not import module {}'.format(env._Module_Name), level=ERROR).flush()
      sys.exit(1)

   return mod

def reload_module():
   ''' Reload the current vroom (python) module.'''

   return _get_module()

