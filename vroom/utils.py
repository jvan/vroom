import os
import sys
import imp
import vroom

def load_module(filename):
   app_path = os.path.dirname(filename) 
   app_path = os.path.abspath(app_path)

   vroom._App_Path = app_path

   print ' -- setting application path'
   vroom._Resource_Paths = [vroom._App_Path, '/usr/local/share/vroom']

   vroom._ModuleName = os.path.basename(filename)
   vroom._ModuleName = os.path.splitext(vroom._ModuleName)[0]

   print ' -- importing {} application'.format(vroom._ModuleName)

   try:
      fp, pathname, description = imp.find_module(vroom._ModuleName, [vroom._App_Path])
      mod = imp.load_module(vroom._ModuleName, fp, pathname, description)
      fp.close()
   except ImportError:
      print 'ERROR: could not import module {}'.format(vroom._ModuleName)
      sys.exit(1)

   return mod

def reload_module():
   print ' -- reloading {} module'.format(vroom._ModuleName)
   fp, pathname, description = imp.find_module(vroom._ModuleName, [vroom._App_Path])
   mod = imp.load_module(vroom._ModuleName, fp, pathname, description)
   fp.close()
   return mod

