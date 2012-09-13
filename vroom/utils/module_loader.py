import os
import sys
import imp
import vroom

from vroom.utils.debug import debug, STATUS

def load_module(filename):
   app_path = os.path.dirname(filename) 
   app_path = os.path.abspath(app_path)

   vroom._App_Path = app_path

   debug(msg='setting application path', level=STATUS).flush()
   vroom._Resource_Paths = [vroom._App_Path, '/usr/local/share/vroom']

   vroom._ModuleName = os.path.basename(filename)
   vroom._ModuleName = os.path.splitext(vroom._ModuleName)[0]

   debug(msg='importing {} application'.format(vroom._ModuleName), level=STATUS).flush()

   try:
      fp, pathname, description = imp.find_module(vroom._ModuleName, [vroom._App_Path])
      mod = imp.load_module(vroom._ModuleName, fp, pathname, description)
      fp.close()
   except ImportError:
      print 'ERROR: could not import module {}'.format(vroom._ModuleName)
      sys.exit(1)

   return mod

def reload_module():
   debug(msg='reloading {} module'.format(vroom._ModuleName), level=STATUS).flush()
   fp, pathname, description = imp.find_module(vroom._ModuleName, [vroom._App_Path])
   mod = imp.load_module(vroom._ModuleName, fp, pathname, description)
   fp.close()
   return mod

