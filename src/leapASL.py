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
   with open('../data/gestureData.csv', 'rb') as dataFile:
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
      getGestureDataFromFile()
    #   print compareMachine.getTargets()
      print(compareMachine.matchGesture(np.array([0.016544,0.585044,0.810833,0.385159,0.407326,-0.828093,0.332061,0.225169,-0.915988,0.391403,-0.07429,-0.917216,0.270478,-0.228206,-0.935288,-0.525087,0.29067,0.799872,-0.028097,0.803404,-0.594771,-0.10491,0.632666,-0.767286,-0.050476,0.386983,-0.920704,-0.233421,0.168204,-0.957717,-0.841405,-0.063797,0.536626,-0.657718,0.673434,0.337481,-0.709145,0.663856,0.237506,-0.711803,0.68565,0.15238,-0.772741,0.61125,0.171012,0.336056,0.284464,-0.897857,0.456954,0.484899,-0.745698,-0.957288,0.286704,0.037424,-0.560178,0.819887,0.118266,-0.219649,0.937734,-0.26909,-0.330514,0.926873,-0.177953,-0.451178,0.71583,0.53294,-0.935946,0.337671,0.099915,-0.715386,0.651304,0.253032,-0.503229,0.864011,0.0157,-0.497377,0.863416,0.084432,-0.424219,0.577608,0.697429,-0.944975,0.318234,0.075824,-0.845347,0.34404,0.408687,-0.75164,0.523797,0.400842,-0.667157,0.510347,0.54263,-0.304735,0.206448,0.929794,0.767677,-0.082086,-0.635557,0.815705,-0.046598,-0.576588,0.536915,0.538118,0.649732,0.244048,0.462205,0.85253,0.055661,0.458013,0.887201,-0.139644,0.616739,0.774682,-0.231612,0.861665,0.451542,0.442959,0.595914,0.669832,0.237693,0.292092,0.926382,0.018807,0.297858,0.954425,-0.177069,0.520311,0.835418,-0.339131,0.767399,0.54414,0.342833,0.64649,0.681554,0.222211,0.102678,0.969577,-0.009731,0.169261,0.985523,-0.216553,0.40148,0.889898,-0.408651,0.688053,0.599656,0.002234,-0.246388,-0.969169,-0.31214,-0.058547,-0.94823,0.329915,0.413073,0.848838,-0.281201,0.16364,-0.945594,-0.169131,0.200353,-0.965015,0.003954,0.281106,-0.959669,0.048308,0.873865,0.483763,0.305292,0.418067,0.855579,-0.295906,0.621556,-0.725333,-0.12939,0.644741,-0.75337,0.033226,0.719623,-0.693569,0.01276,0.820329,0.571749,0.512074,0.365136,0.777467,-0.10209,0.973365,0.205274,0.031934,0.988066,0.150683,0.060082,0.964248,0.258101,-0.037783,0.727944,0.684594,-0.180447,0.00875,-0.983546,-0.362178,0.495448,-0.789531])))

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
