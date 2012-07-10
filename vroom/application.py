#################################################
# vroom Application Class
#
#################################################
import pyvrui
from OpenGL.GL import *
import sys
import os
from utils import reload_module
import pyinotify

MainMenuOptions = { 'title': 'vroom', 'items': [] }

def setMainMenuTitle(title):
   global MainMenuOptions
   MainMenuOptions['title'] = title

def addMainMenuItem(label, callback, type='button'):
   global MainMenuOptions
   MainMenuOptions['items'].append((label, callback, type))

class Application(pyvrui.Application, pyvrui.GLObject):

   LocatorCount = 0

   class DataItem(pyvrui.DataItem):
      def __init__(self):
         pyvrui.DataItem.__init__(self)

   def __init__(self, init, gl_init, draw, frame, button_press, button_release, motion, args):
      pyvrui.Application.__init__(self, sys.argv+args)
      pyvrui.GLObject.__init__(self)

      self._init = init
      self._gl_init = gl_init
      self._display = draw
      self._frame = frame
      self._button_press = button_press
      self._button_release = button_release
      self._motion = motion

      self.menu_callbacks = {} 

      if self._init:
         self._init()

      mainMenu = self.createMainMenu()
      pyvrui.setMainMenu(mainMenu)

      toolManager = pyvrui.getToolManager()
      toolManager.getToolCreationCallbacks().add(self.toolCreationCallback)
      toolManager.getToolDestructionCallbacks().add(self.toolDestructionCallback)

      #self.locatorTool = None
      self.locatorTools = []
       
   def initContext(self, contextData):
      dataItem = Application.DataItem() 
      contextData.addDataItem(self, dataItem)

      if self._gl_init:
         self._gl_init()

   def display(self, context):
      if not self._display:
         return

      dataItem = context.retrieveDataItem(self)

      glPushAttrib(GL_ALL_ATTRIB_BITS)
      self._display()
      glPopAttrib()

   def frame(self):
      if not self._frame:
         return

      self._frame()
      pyvrui.requestUpdate()

   def createMainMenu(self):
      widgetManager = pyvrui.getWidgetManager()
      mainMenuPopup = pyvrui.PopupMenu("MainMenuPopup", widgetManager)
      mainMenuPopup.setTitle(MainMenuOptions['title'])
      mainMenu = pyvrui.Menu("MainMenu", mainMenuPopup, False)

      for (label, callback, type) in MainMenuOptions['items']:
         if type == 'button': 
            button = pyvrui.Button(label.lower(), mainMenu, label)
         elif type == 'toggle':
            button = pyvrui.ToggleButton(label.lower(), mainMenu, label)

         self.menu_callbacks[button.getName()] = callback
         button.getSelectCallbacks().add(self.main_menu_callback)
      
      mainMenu.manageChild()

      return mainMenuPopup

   @pyvrui.Button.SelectCallback
   def main_menu_callback(self, cbData):
      self.menu_callbacks[cbData.button.getName()]()

   @pyvrui.LocatorTool.ButtonPressCallback
   def buttonPressCallback(self, data, additional_data):
      if self._button_press:
         origin = data.currentTransformation.getTranslation()
         pos = [origin[0], origin[1], origin[2]]
         self._button_press(pos, additional_data)

   @pyvrui.LocatorTool.ButtonReleaseCallback
   def buttonReleaseCallback(self, data, additional_data):
      if  self._button_release:
         origin = data.currentTransformation.getTranslation()
         pos = [origin[0], origin[1], origin[2]]
         self._button_release(pos, additional_data)
         
   @pyvrui.LocatorTool.MotionCallback
   def motionCallback(self, data, additional_data):
      if  self._motion:
         origin = data.currentTransformation.getTranslation()
         pos = [origin[0], origin[1], origin[2]]
         self._motion(pos, additional_data)

   @pyvrui.ToolManager.ToolCreationCallback
   def toolCreationCallback(self, data):
      if isinstance(data.tool, pyvrui.LocatorTool):
         self.locatorTools.append(data.tool)
         # Assign callbacks
         data.tool.getButtonPressCallbacks().add(self.buttonPressCallback, Application.LocatorCount)
         data.tool.getButtonReleaseCallbacks().add(self.buttonReleaseCallback, Application.LocatorCount)
         data.tool.getMotionCallbacks().add(self.motionCallback, Application.LocatorCount)
         Application.LocatorCount += 1

   @pyvrui.ToolManager.ToolDestructionCallback
   def toolDestructionCallback(self, data):
      pass

import traceback
import StringIO

def genTraceback():
    fp = StringIO.StringIO()
    traceback.print_exc(file=fp)
    message = fp.getvalue()
    
    print message
    print "\nFix application source to continue.\n"

class LiveCoding:

   @staticmethod
   def no_update(func):
      func.do_not_update = True
      return func

class LiveCodingApplication(Application):

   def __init__(self, init, gl_init, draw, frame, button_press, button_release, motion, args):
      Application.__init__(self, init, gl_init, draw, frame, button_press, button_release, motion, args)
      self.broken = False
      self.force_reload = []

   def monitor(self, path, filename):

      class EventHandler(pyinotify.ProcessEvent):
         def __init__(self, app, files):
            self.app = app
            self.watch_list = files
            print 'EventHandler.watch_list={}'.format(self.watch_list)

         def process_IN_CLOSE_WRITE(self, event):
            f = event.name and os.path.join(event.path, event.name) or event.path
            print ' !! processing event {}, {}'.format(event.path, event.name)
            if event.name in self.watch_list:
               mod = reload_module() 
               self.app._display = mod.__dict__['draw']
               self.app.broken = False

               self.app.force_reload = []

               func_exists = lambda x: x in mod.__dict__
               skip_update = lambda x: getattr(mod.__dict__[x], 'do_not_update', False)
               do_update = lambda x: func_exists(x) and not skip_update(x)

               if 'frame' in mod.__dict__: 
                  self.app._frame = mod.__dict__['frame']

               if 'button_press' in mod.__dict__: 
                  self.app._button_press = mod.__dict__['button_press']
               
               if 'button_release' in mod.__dict__: 
                  self.app._button_release = mod.__dict__['button_release']

               if 'motion' in mod.__dict__:
                  self.app._motion = mod.__dict__['motion']

               if do_update('gl_init'):
                  self.app._gl_init = mod.__dict__['gl_init']
                  #self.app._gl_init()
                  self.app.force_reload.append(self.app._gl_init)

               if 'init' in mod.__dict__:
                  if not getattr(mod.__dict__['init'], 'do_not_update', False):
                     print ' -- reloading init()'
                     self.app._init = mod.__dict__['init']
                     #self.app._init()
                     self.app.force_reload.append(self.app._init)

      print ' -- monitoring path={}'.format(path)
      self.wm = pyinotify.WatchManager()
      self._Notifier = pyinotify.Notifier(self.wm, EventHandler(self, [filename]), timeout=10)
      self.wm.add_watch(path, pyinotify.IN_CLOSE_WRITE)

   def frame(self):

      try:
         self._Notifier.process_events()
         while self._Notifier.check_events():
            self._Notifier.read_events()
            self._Notifier.process_events()

      except Exception, e:
         print 'LiveCodingApplication.frame: error reloading module'
         print e
         pass

      Application.frame(self)
 
   def display(self, context):
      
      if self.broken:
         return

      try:
         while len(self.force_reload):
            self.force_reload.pop(0)()

         Application.display(self, context)
      except Exception, e:
         print '!' * 60
         print 'LiveCodingApplication.display error'
         print
         genTraceback()
         print '!' * 60

         self.broken = True
