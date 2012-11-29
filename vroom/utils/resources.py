# System imports

import os

# Vroom imports

import vroom.core.environment as env

from debug import *

class ResourceNotFound(Exception): 
   def __init__(self, filename):
      self.filename = filename

def get_resource(filename):
   """ Search for resource in application and global directories.

   Application resources may be stored in the following locations:

      1. In a data/ directory located in the application's root directory
      2. In the global resource directory (usually /usr/local/share/vroom/data)

   Files in these locations can be retrieved by their path relative to the data
   directory. If a files exist in both locations with the same name the local
   (application) resource will be returned. 

   Data required by the application should be placed in the application data 
   directory. Resources that will be used by multiple applications (i.e. fonts) 
   should be stored in the global directory.


   filename -- pathname of the resource relative to data directory

   return   -- the full pathname of the resource
   raises   -- A ResourceNotFound exception is raised if the file cannot be found
               in any of the resource directories.
   """

   debug(level=VERBOSE).add('filename', filename).flush()
   debug(level=VERBOSE).add('_Resource_Paths', env._Resource_Paths).flush()

   # Check for the file in the application's data directory
   path = os.path.join(env._Resource_Paths[0], 'data', filename)
   if os.path.exists(path):
      debug(msg='found application resource {}'.format(path), level=STATUS, indent=1).flush()
      return path

   # Check for the file in the global vroom resource dir
   path = os.path.join(env._Resource_Paths[1], 'data', filename)
   if os.path.exists(path):
      debug(msg='found global resource {}'.format(path), level=STATUS, indent=1).flush()
      return path

   raise ResourceNotFound(filename)

