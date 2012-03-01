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
   def buttonPressCallback(self, data):
      if self._button_press:
         origin = data.currentTransformation.getTranslation()
         pos = [origin[0], origin[1], origin[2]]
         self._button_press(pos)

   @pyvrui.LocatorTool.ButtonReleaseCallback
   def buttonReleaseCallback(self, data):
      if  self._button_release:
         origin = data.currentTransformation.getTranslation()
         pos = [origin[0], origin[1], origin[2]]
         self._button_release(pos)
         
   @pyvrui.LocatorTool.MotionCallback
   def motionCallback(self, data):
      if  self._motion:
         origin = data.currentTransformation.getTranslation()
         pos = [origin[0], origin[1], origin[2]]
         self._motion(pos)

   @pyvrui.ToolManager.ToolCreationCallback
   def toolCreationCallback(self, data):
      if isinstance(data.tool, pyvrui.LocatorTool):
         self.locatorTool = data.tool
         # Assign callbacks
         data.tool.getButtonPressCallbacks().add(self.buttonPressCallback)
         data.tool.getButtonReleseCallbacks().add(self.buttonReleaseCallback)
         data.tool.getButtonMotionCallbacks().add(self.buttonMotionCallback)

   @pyvrui.ToolManager.ToolDestructionCallback
   def toolDestructionCallback(self, data):
      pass


class LiveCodingApplication(Application):

   def __init__(self, init, gl_init, draw, frame, button_press, button_release, motion, args):
      Application.__init__(self, init, gl_init, draw, frame, button_press, button_release, motion, args)

   def monitor(self, path, filename):

      class EventHandler(pyinotify.ProcessEvent):
         def __init__(self, app, files):
            self.app = app
            self.watch_list = files

         def process_IN_CLOSE_WRITE(self, event):
            f = event.name and os.path.join(event.path, event.name) or event.path
            if event.name in self.watch_list:
               mod = reload_module() 
               self.app._display = mod.__dict__['draw']
               if 'frame' in mod.__dict__:
                  self.app._frame = mod.__dict__['frame']

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
 
