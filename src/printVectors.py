# ASL-to-Text
# Ubiquitous Computing final project, Spring 2016
# Authors: Kevin Dibble, Jasmine Moran, Susan Souza
# File description:
#   This is a data-gathering file that is used for debug and new gesture
#   creation purposes. Modeled after leapASL.py
#

import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
sys.path += ["/../lib/Leap", "../lib/x64", "../lib"]

import Leap

# Get the data from the vector and add it to the buffer
def crunch_vector(vector_item, buf):
   buf += '%f,%f,%f,' % (vector_item.x, vector_item.y, vector_item.z)
   return buf

# Get the data from the vector and add it to the buffer, making sure to not
# add in a superflouous comma
def crunch_vector_last(vector_item, buf):
   buf += '%f,%f,%f' % (vector_item.x, vector_item.y, vector_item.z)
   return buf

# Get the data from the vector array and add them as cells in the buffer
def extract_coords(vector_array, buf):
   for item in vector_array:
      buf += '%f,%f,%f,' % (item.x, item.y, item.z)
   return buf


#a subclass of Leap.Listener based on Sample.py
class aslListener(Leap.Listener):
   #allows the listener to communicate with the model
   #listener instantiated in Ctrl
   startYet = 0
   buf = ""

   # returh the current data buffer with an appended newline character
   def getBuf(self):
      self.buf = self.buf[:-1]
      self.buf += '\n'
      return self.buf

   # set the target (what this data set will match to) and initialize the data
   # buffer
   def addTarget(self, target):
      self.buf = "%s," % target.strip()

   # Set the start flag to signal the data gathering to begin
   def extraUtils(self):
      self.startYet = 1

   # From the sample
   def on_init(self, controller):
      print "Initialized"

   # From the sample
   def on_connect(self, controller):
      print "Connected"

   # From the sample
   def on_disconnect(self, controller):
      print "Disconnected"

   # From the sample
   def on_exit(self, controller):
      print "Exited"

   # This is "where the magic happens." This is where we have access to the
   # data and where the data is pulled
   def on_frame(self, controller):
      frame = controller.frame()
      # don't actually do anything with the data until it's time
      if self.startYet == 1:
          distal_directions = []
          inter_directions = []
          proximal_directions = []
          wrist_angle = 0
          # Add data from each hand into the buffer
          for hand in frame.hands:
             handType = "Left hand" if hand.is_left else "Right hand"
             activeHand =  frame.hands.frontmost
             activeArm = activeHand.arm
             arm_direction = activeArm.direction
             hand_direction = activeHand.direction

             # get the finger bone directions (all three bones)
             for finger in activeHand.fingers:
                distal_directions.append(finger.bone(3).direction)
                #print "   Leap.Vector%s," % (finger.bone(3).direction)
                inter_directions.append(finger.bone(2).direction)
                proximal_directions.append(finger.bone(1).direction)

             # Add those finger directions to the buffer
             if distal_directions:
                self.buf = extract_coords(distal_directions, self.buf)
             if inter_directions:
                self.buf =extract_coords(inter_directions, self.buf)
             if proximal_directions:
                self.buf =extract_coords(proximal_directions, self.buf)
                self.buf =crunch_vector(hand_direction, self.buf)
                #crunch_vector_last(arm_direction)
                self.buf =crunch_vector(arm_direction, self.buf)
                time.sleep(5)

# this is the main hook into the data gathering. It opens up the data file
# sets up the leapMotion controller and handles the user interaction
def main():
   f = open('../data/gestureData.csv','a')
   listener = aslListener()
   controller = Leap.Controller()
   controller.add_listener(listener)
   #read in a letter, add to buffer (fcn)
   print "Enter the target for the samples"
   currentTarget = sys.stdin.readline()
   listener.addTarget(currentTarget)
   print "Press <Enter> to start recording data... and <Enter> again to quit"
   sys.stdin.readline()
   listener.extraUtils();

   try:
      sys.stdin.readline()
      f.write(listener.getBuf()) #append the data buffer to the file

   except KeyboardInterrupt:
      pass
   finally:
   # Remove the sample listener when done
      controller.remove_listener(listener)

# run the program!
if __name__ == '__main__':
   main()

#refs:
#  Leap:
#     https://developer.leapmotion.com/documentation/python/devguide/Sample_Tutorial.html
