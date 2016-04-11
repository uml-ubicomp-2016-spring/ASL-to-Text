import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
sys.path += ["/../lib/Leap", "../lib/x64", "../lib"]
import Leap
import distalData as data

from sklearn import svm
import numpy as np

import csv, re

def getGestureDataFromFile():
   with open('../data/gestureData.csv', 'rb') as dataFile:
      reader = csv.reader(dataFile))
      for row in reader:
         print(row)
         matcher = re.match(r'target (\w+) data (.+)$',  row, re.I | re.M) #then match the second group
         print(matcher.group(1))
         print(matcher.group(2))



#get the data
#get the targets
compareMachine = DataCompare()

class DataCompare():
   def __init__(self, data, targets):
      self.clf = svm.SVC() #this is the single class variable
    #   data = np.array(angles)
    #   targets = np.array(targets
      self.clf.fit(data, targets)
      print("data")
      print(data)
      print("targets")
      print(targets)

   def matchGesture(self, formattedData):
      result = str(self.clf.predict([formattedData]))[2:-2] #predicts which letter this is
    #   print(result)
      return result #How are we handling things that shouldn't match?

COMPARISON_PERCENT = 30

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

def compare(base_letter, compare_letter):
   # loop through each finger and compare the two letters together
   i = 0
   all_match = True
   while (i < 5):
    #   print "\ni = %d" % (i)
      j = 0
      while (j < 5):
        #  print "\tj = %d" % (j)
        # compare this i/j pairing
        #  print "%s and %s" % (base_letter[i], base_letter[j])
         base_dot = base_letter[i].angle_to(base_letter[j])
         compare_dot = compare_letter[i].angle_to(compare_letter[j])
        #  print ""
         print "%s and %s" % (base_dot, compare_dot)
         if (base_dot < 0.001 and base_dot > -0.001):
            comparison = 0
         else:
            comparison = 100 * (compare_dot - base_dot) / base_dot
         #print "percentage comparison %s" % (comparison)
         if comparison < COMPARISON_PERCENT and comparison > (COMPARISON_PERCENT * -1):
            all_match = all_match and True
         else:
            all_match = False
         j = j + 1
      i = i + 1
      print ""
   print "all_match: %s\n" % (all_match)
   return all_match

def compare_angles_thumb(base_angles, compare_vectors):
   all_match = True
   compare_angles = get_angles(compare_vectors)
   i = 0
   while (i < 5):
    #   print "%s and %s" % (base_angles[i], compare_angles[i])
      comparison = 100 * (compare_angles[i] - base_angles[i]) / (base_angles[i] + 0.00000001)
      #print "percentage comparison %s" % (comparison)
      if abs(comparison) < COMPARISON_PERCENT:
         all_match = all_match and True
      else:
         all_match = False
      i = i + 1

   print "all_match: %s\n" % (all_match)
   return all_match

def compare_angles(base_angles, compare_vectors):
   all_match = True
   compare_angles = get_angles(compare_vectors)
   i = 0
   while (i < len(base_angles)):
    #   print "%s and %s" % (base_angles[i], compare_angles[i])
      comparison = 100 * (compare_angles[i] - base_angles[i]) / (base_angles[i] + 0.00000001)
      #print "percentage comparison %s" % (comparison)
      if comparison < COMPARISON_PERCENT and comparison > (COMPARISON_PERCENT * -1):
         all_match = all_match and True
      else:
         all_match = False
      i = i + 1

   #print "all_match: %s\n" % (all_match)
   return all_match

#a subclass of Leap.Listener based on Sample.py
class aslListener(Leap.Listener):
   finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
   #prev_letter = "B"
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
    #  finger_vectors = [Leap.Vector(0.260498, -0.677901, 0.687452),
    #     Leap.Vector(-0.393398, 0.827915, -0.399743),
    #     Leap.Vector(-0.39042, 0.813348, -0.431321),
    #     Leap.Vector(-0.286566, 0.8197, -0.495956),
    #     Leap.Vector(-0.216815, 0.854775, -0.47154)]


      frame = controller.frame()
      #print "got a frame"

      for hand in frame.hands:
         handType = "Left hand" if hand.is_left else "Right hand"
        #  print "%s" % (hand.pointables[1].direction)
         # Get fingers
         #for finger in hand.fingers:
            #print "    %s finger, id: %d, length: %fmm, width: %fmm" % (
            #   self.finger_names[finger.type],
            #   finger.id,
            #   finger.length,
            #   finger.width)
         #print "\n"

        #  for finger in hand.fingers:
        #     distal_direction = finger.bone(3).direction
        #     print "direction %s" % (distal_direction)
         current_vectors = []
         for finger in hand.fingers:
            current_vectors.append(finger.bone(3).direction)
            # print "%s" % (finger.bone(3).direction)
         letter_index = 0
         all_match = False
         for letter in data.all_letter_angles:
            all_match = compare_angles_thumb(letter, current_vectors)
            if all_match:
               break
            letter_index = letter_index + 1
        #  all_match = compare(finger_vectors, current_vectors)
        #  all_match = compare(finger_vectors, hand.pointables)
        #  for pointable in hand.pointables:
        #      #print " direction %s" % (pointable.direction)
        #      dot_product = pointable.direction.dot(finger_vectors[i])
        #      #print "dot product %s" % (dot_product)
        #      if dot_product > 0.94:
        #         all_match = all_match and True
        #      else:
        #         all_match = False
        #      #print "%s all_match" % (all_match)
        #      i = i + 1
         if all_match:
            print "match %s!" % (data.letter_names[letter_index])
            self.report.textChanged(data.letter_names[letter_index])
            #self.prev_letter = letter_names[letter_index]

         print "\n\n"
         time.sleep(.2)

    #   for gesture in frame.gestures():
    #
    #      if gesture.type is Leap.Gesture.TYPE_CIRCLE:
    #         #print "circle"
    #         self.report.textChanged("circle")
    #      elif gesture.type is Leap.Gesture.TYPE_SWIPE:
    #         #print "swipe"
    #         self.report.textChanged("swipe")
    #      elif gesture.type is Leap.Gesture.TYPE_KEY_TAP:
    #         #print "key tap"
    #         self.report.textChanged("key tap")
    #      elif gesture.type is Leap.Gesture.TYPE_SCREEN_TAP:
    #         #print "screen tap"
    #         self.report.textChanged("screen tap")
