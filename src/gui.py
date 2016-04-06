

from Tkinter import *
from leapASL import *

### begin MVC GUI implementation ###

class Ctrl:
   def __init__(self, root):
      self.root = root
      self.view = View(root)
      self.model = Model(self)
      self.view.setSubtitle("ASL to Text")
      listener = aslListener()
      controller = Leap.Controller()
      controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
      controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)
      controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
      controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)

      listener.extraUtils(self.model) #ensure the listener can send changes to the model

      controller.add_listener(listener)
      self.root.mainloop()
      print "Press Enter to quit..."
      #need to replace this block with some input from View to trigger exit and so on
      try:
         sys.stdin.readline()
      except KeyboardInterrupt:
         pass
      finally:
      # Remove the sample listener when done
         controller.remove_listener(listener)
   #do thing when model updated

   def gotTxtUpdate(self):
      self.view.setSubtitle(self.model.getText())
      #print "ctrl got: " + self.model.getText()

class Model():

   def __init__(self, ctrl):
      self.ctrl = ctrl
      self.txt = "ASL to Text"

   def getText(self):
      return self.txt

   def textChanged(self, text):
      if len(self.txt) < 12:
         self.txt = self.txt + text
      else:
         self.txt = text
      self.ctrl.gotTxtUpdate()  #signal controller of change

class View:
   def loadView(self):
      self.subtitle = Label(self.ctrl, font=('Helvetica','36'), fg='gray23', bg='gray30', anchor=S, pady=50)
      self.subtitle.master.wm_attributes("-topmost", True)
      self.subtitle.master.wm_attributes("-transparentcolor", "gray30")
      self.subtitle.pack(fill=BOTH, expand=1, side=BOTTOM)

   def __init__(self, ctrl):
     self.ctrl = ctrl
     self.loadView()

   def setSubtitle(self, txt):
      self.subtitle.configure(text = txt)
      #print "model updating"

def go():
   root = Tk()
   root.title('ASL-to-Text')
   root.attributes("-fullscreen", True) #for fullscreen
   app = Ctrl(root)

### end MVC GUI implementation ###
