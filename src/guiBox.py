from Tkinter import *
import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))

import Leap
#from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

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
     print "got to end of View init"

     
   def setSubtitle(self, txt):
      self.subtitle.configure(text = txt)
      #print "model updating"

### end MVC GUI implementation ###    
      
      
#a subclass of Leap.Listener based on Sample.py
class aslListener(Leap.Listener):
   #allows the listener to communicate with the model
   #listener instantiated in Ctrl
   def extraUtils(self, model):
      self.report = model
   
   def on_init(self, controller):
      print "Initialized"
      
   def on_connect(self, controller):
      print "Connected"

   def on_disconnect(self, controller):
      print "Disconnected"

   def on_exit(self, controller):
      print "Exited"

   def on_frame(self, controller):
      frame = controller.frame()
      #print "got a frame"
      for gesture in frame.gestures():
         if gesture.type is Leap.Gesture.TYPE_CIRCLE:
            #print "circle"
            self.report.textChanged("circle")
         elif gesture.type is Leap.Gesture.TYPE_SWIPE:
            #print "swipe"
            self.report.textChanged("swipe")
         elif gesture.type is Leap.Gesture.TYPE_KEY_TAP:
            #print "key tap"
            self.report.textChanged("key tap")
         elif gesture.type is Leap.Gesture.TYPE_SCREEN_TAP:
            #print "screen tap"
            self.report.textChanged("screen tap")
         
   
def main():
   root = Tk()
   root.title('GUI Box Test')
   root.attributes("-fullscreen", True) #for fullscreen
   app = Ctrl(root)
   
 
if __name__ == '__main__':
    main()  
    
#refs: 
#  Leap:
#     https://developer.leapmotion.com/documentation/python/api/Leap.Gesture.html#Leap.Gesture.html
#     https://developer.leapmotion.com/documentation/python/devguide/Sample_Tutorial.html
#  Tkinter & MVC:
#     https://tkinter.unpythonic.net/wiki/ToyMVC
#     http://ygchan.blogspot.com/2012/05/python-stop-watch-timer-source-code.html
#     http://www.science.smith.edu/dftwiki/index.php/File:TkInterColorCharts.png
