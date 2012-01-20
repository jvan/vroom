#################################################
# vroom Application Class
#
#################################################
import pyvrui
from OpenGL.GL import *
import sys

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

   def __init__(self, init, gl_init, draw, frame, button_press, button_release, motion):
      pyvrui.Application.__init__(self, sys.argv)
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
