import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
sys.path += ["/../lib/Leap", "../lib/x64", "../lib"]
import Leap

from sklearn import svm
import numpy as np
class DataCompare():
   def __init__(self):
      self.clf = svm.SVC() #this is the single class variable

   def setData(self, data, targets):
      self.data = data
      self.targets = targets
      self.clf.fit(data, targets)
    #   print("data")
    #   print(data)
    #   print("targets")
    #   print(targets)

   def matchGesture(self, formattedData):
      #predicts which letter this is
      result = str(self.clf.predict([formattedData]))[2:-2]
    #   print(result)
      return result #How are we handling things that shouldn't match?

   def getTargets(self):
      return self.targets

compareMachine = DataCompare()

import csv, re
def getGestureDataFromFile():
   with open('../data/gestureDataSimple.csv', 'rb') as dataFile:
      reader = csv.reader(dataFile)
      numCol=len(next(reader)) # Read first line and count columns
      dataFile.seek(0)              # go back to beginning of file
      numRow = len(list(reader)) # count the number of rows
      dataFile.seek(0)              # go back to beginning of file
      targets = np.empty(numRow, dtype=object)
      # numCol - 1 because target is not stored in the data array
      data = np.empty([numRow, numCol - 1], np.float64)

      # begin data file reading
      rowCount = 0
      for row in reader: # make an array for each row
         column = -1 # initial value at -1 to allow for easy indexing
         for col in row:
            if column is -1: # first cell/target cell
               targets[rowCount] = col # this is the first cell, save the target
            else: # data cell
            #    print(col)
               data[rowCount, column] = col # save the next piece of data
            column = column + 1 # end of column for loop
         rowCount = rowCount + 1 # end of row for loop
      # end data file reading

    #   print(targets)
    #   print(data)
      # init the compare machine
      global compareMachine
      compareMachine.setData(data, targets)

import printVectors

def vector_extract(vector_item, buf):
   buf.append(vector_item.x)
   buf.append(vector_item.y)
   buf.append(vector_item.z)
   return buf

def multi_vector_extract(vector_array, buf):
   for item in vector_array:
      buf.append(item.x)
      buf.append(item.y)
      buf.append(item.z)
   return buf
#a subclass of Leap.Listener based on Sample.py
class aslListener(Leap.Listener):

   #allows the listener to communicate with the model
   #listener instantiated in Ctrl
   buf = []
   sample = [0.538109,-0.68696,0.48839,-0.560825,0.719204,-0.410147,-0.509568,0.733951,-0.449062,-0.386425,0.775132,-0.499846,-0.2683,0.802056,-0.533592,0.717797,-0.654975,0.236168,-0.253205,0.957649,0.137099,-0.137588,0.99033,0.017771,0.020345,0.998759,-0.045456,0.218458,0.969222,-0.113513,0.834387,-0.547252,-0.065674,0.530824,0.182306,0.827642,0.621974,0.235733,0.746712,0.651065,0.166717,0.740486,0.724168,0.066919,0.686369,-0.292726,0.924451,-0.24434,-0.344353,0.558389,-0.754734]
   # def getBuf(self):
   #    self.buf = self.buf[:-1]
   #    self.buf += '\n'
   #    return self.buf

   # def addTarget(self, target):
   #    self.buf = "%s," % target.strip()

   def extraUtils(self, model):
      self.report = model

   def on_init(self, controller):
      print "Initialized"
      getGestureDataFromFile()
      #debug to make sure that the machine matches with itself
      print(compareMachine.matchGesture(np.array(self.sample)))

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
      inter_directions = []
      proximal_directions = []
      wrist_angle = 0

      for hand in frame.hands:
         handType = "Left hand" if hand.is_left else "Right hand"
         activeHand =  frame.hands.frontmost
         activeArm = activeHand.arm
         arm_direction = activeArm.direction
         hand_direction = activeHand.direction

         for finger in activeHand.fingers:
            distal_directions.append(finger.bone(3).direction)
            #print "   Leap.Vector%s," % (finger.bone(3).direction)
            inter_directions.append(finger.bone(2).direction)
            proximal_directions.append(finger.bone(1).direction)

         if distal_directions:
            self.buf = multi_vector_extract(distal_directions, self.buf)
         if inter_directions:
            self.buf =multi_vector_extract(inter_directions, self.buf)
         if proximal_directions:
            self.buf =multi_vector_extract(proximal_directions, self.buf)
            self.buf =vector_extract(hand_direction, self.buf)
            self.buf =vector_extract(arm_direction, self.buf)

         # buf needs to be a python array
         print("testing frame")
        #  print("length ")
        #  print(len(self.buf))
        #  print(len(self.sample))
         myFile = open("../data/sample.csv", "wb")
         for item in self.buf:
            myFile.write("%s," % item)
         result = compareMachine.matchGesture(np.array(self.buf))
         self.buf = []
         print(result)
         self.report.textChanged(result)
# ---------------------------------------------------------
# Old way of doing things:
# ---------------------------------------------------------
        #  current_vectors = []
        #  for finger in hand.fingers:
        #     current_vectors.append(finger.bone(3).direction)
        #     # print "%s" % (finger.bone(3).direction)
        #  letter_index = 0
        #  all_match = False
        #  for letter in data.all_letter_angles:
        #     all_match = compare_angles_thumb(letter, current_vectors)
        #     if all_match:
        #        break
        #     letter_index = letter_index + 1
         #
        #  if all_match:
        #     print "match %s!" % (data.letter_names[letter_index])
        #     self.report.textChanged(data.letter_names[letter_index])
        #     #self.prev_letter = letter_names[letter_index]
# ---------------------------------------------------------
#end old way of doing things
# ---------------------------------------------------------

         print "\n\n"
         time.sleep(2.2)
