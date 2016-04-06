import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
sys.path += ["/../lib/Leap", "../lib/x64", "../lib"]

import Leap
#from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

def get_angles(vector_array):
   return_array = []
   i = 0
   while (i < 5):
      j = 0
      while (j < 5):
         return_array.append(vector_array[i].angle_to(vector_array[j]))
         j = j + 1
      i = i + 1
   return return_array

#a subclass of Leap.Listener based on Sample.py
class aslListener(Leap.Listener):
   finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
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
      distal_directions = []
      for hand in frame.hands:
         handType = "Left hand" if hand.is_left else "Right hand"
         #print "\nhand_type: %s" % (handType)
         #print "pointables:"
         #pointable_directions = []
         #for pointable in hand.pointables:
         #   pointable_directions.append(pointable.direction)
            #print "   Leap.Vector%s," % (pointable.direction)

         print "distal directions:"
         distal_directions = []
         for finger in hand.fingers:
            distal_directions.append(finger.bone(3).direction)
            print "   Leap.Vector%s," % (finger.bone(3).direction)

      if distal_directions:
         print "distal_directions angle set"
         retrieved_angles = get_angles(distal_directions)
         for angle in retrieved_angles[:-1]:
            print "   %s," % (angle)
         else:
            print "   %s" % (angle)

def main():
  listener = aslListener()
  controller = Leap.Controller()
  controller.add_listener(listener)
  print "Press Enter to quit..."
  #need to replace this block with some input from View to trigger exit and so on
  try:
     sys.stdin.readline()
  except KeyboardInterrupt:
     pass
  finally:
  # Remove the sample listener when done
     controller.remove_listener(listener)


if __name__ == '__main__':
    main()

#refs:
#  Leap:
#     https://developer.leapmotion.com/documentation/python/devguide/Sample_Tutorial.html
