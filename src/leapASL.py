# ASL-to-Text
# Ubiquitous Computing final project, Spring 2016
# Authors: Kevin Dibble, Jasmine Moran, Susan Souza
# File description:
#   This is the back end of the project. This file interfaces with the
#   LeapMotion and the machine learning algorithm.
# Useful nomenclature:
#   targets: the representation of a row of data in the machine learning
#       algorithm. In our project, the targets are the english letter that the
#       hand motion corresponds to
#

import os, sys, inspect, thread, time
src_dir = os.path.dirname(inspect.getfile(inspect.currentframe()))
arch_dir = '../lib/x64' if sys.maxsize > 2**32 else '../lib/x86'
sys.path.insert(0, os.path.abspath(os.path.join(src_dir, arch_dir)))
sys.path += ["/../lib/Leap", "../lib/x64", "../lib"]
import Leap

# ML imports
from sklearn import svm
import numpy as np

# this is the machine learning wrapper class
class DataCompare():
   def __init__(self):
      self.clf = svm.SVC() #this is the single class variable

   # set up the machine learning algorithm with the specified data
   def setData(self, data, targets):
      self.data = data
      self.targets = targets
      self.clf.fit(data, targets)

   # assuming the machine has been set up, match the given data
   def matchGesture(self, formattedData):
      #predicts which letter this is
      result = str(self.clf.predict([formattedData]))[2:-2]
      return result #How are we handling things that shouldn't match?

   # Get the array of targets
   def getTargets(self):
      return self.targets

# initialize the machine
compareMachine = DataCompare()

# this grabs the data from the csv data file and sets up the machine
import csv, re
def getGestureDataFromFile():
   with open('../data/gestureDataLong.csv', 'rb') as dataFile:
      reader = csv.reader(dataFile)
      numCol = len(next(reader)) # Read first line and count columns
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
               data[rowCount, column] = col # save the next piece of data
            column = column + 1 # end of column for loop
         rowCount = rowCount + 1 # end of row for loop
      # end data file reading

      # init the compare machine
      global compareMachine
      compareMachine.setData(data, targets)

# Get the data from the vector and append it to the buffer
def vector_extract(vector_item, buf):
   buf.append(vector_item.x)
   buf.append(vector_item.y)
   buf.append(vector_item.z)
   return buf

# Get the data from the vector_array and append them to the buffer
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
   frameCount = 0
   resultCount = 0
   passedThree = 0
   previousResult = " "
   previousPrintChar = ""
   printedSpace = False
   staticLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v','w', 'x', 'y']

   def extraUtils(self, model):
      self.report = model

   def on_init(self, controller):
      print "Initialized"
      getGestureDataFromFile()

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
   # data and where the data is pulled and sent to the machine
   def on_frame(self, controller):
      frame = controller.frame()
      distal_directions = []
      inter_directions = []
      proximal_directions = []
      wrist_angle = 0
      if not frame.hands.is_empty:
         # attempt to match every hand in view
         for hand in frame.hands:
            handType = "Left hand" if hand.is_left else "Right hand"
            activeHand =  frame.hands.frontmost
            activeArm = activeHand.arm
            arm_direction = activeArm.direction
            hand_direction = activeHand.direction

            # get the finger bone directions (all three bones)
            for finger in activeHand.fingers:
               distal_directions.append(finger.bone(3).direction)
               inter_directions.append(finger.bone(2).direction)
               proximal_directions.append(finger.bone(1).direction)

            # Add those finger directions to the buffer
            if distal_directions:
               self.buf = multi_vector_extract(distal_directions, self.buf)
            if inter_directions:
               self.buf = multi_vector_extract(inter_directions, self.buf)
            if proximal_directions:
               self.buf = multi_vector_extract(proximal_directions, self.buf)
               self.buf = vector_extract(hand_direction, self.buf)
               self.buf = vector_extract(arm_direction, self.buf)

               # match the data, print the result, and update the gui with the result
               result = ""
              # print("testing frame:")
               if len(self.buf) == 1479: #this is unstable. should find away to save the row length when we get the data
                  result = compareMachine.matchGesture(np.array(self.buf))
                  if not result ==' ' and not result == '':
                       print(result)
                  self.frameCount = 0
               else:
                  print "not enough data to match yet"
                  #self.buf = [] # don't forget to reset this!
               if len(self.buf) >= 1479:
                  self.buf = self.buf[51:]

               if result == self.previousResult:
                  self.resultCount += 1
               else:
                  self.resultCount = 0
                  self.previousResult = result
               if result in self.staticLetters:
                   if self.resultCount == 10:
                      self.printedSpace = False
                      self.report.textChanged(result)
                      #self.resultCount = 0
               else:
                  if not self.previousPrintChar == result:
                     self.printedSpace = False
                     self.report.textChanged(result)
                     self.previousPrintChar = result

            print "\n"
         #time.sleep(2.2) #how long to wait between matchings
      else:
         #append an entire frame of 0.0 to the buffer and shift the buffer as usual
        # print "invalid frame " + (str)(self.frameCount)
         iList = [0.0] * 51
         self.buf = self.buf + iList;
         del iList[:]
         self.buf = self.buf[51:]
         self.frameCount += 1

         #37 frames is about a second
         if self.frameCount == 37:
            self.passedThree += 1
            self.frameCount = 0
            print self.passedThree
            #it's been three seconds, so clear the text displayed in view
            if self.passedThree == 15:
               self.passedThree = 0
               #print "clearing text"
               self.report.clearText()
            #if we go an entire second with invalid data
            if self.printedSpace == False and self.passedThree == 2:
               self.printedSpace = True
               self.report.textChanged(' ')#print a space
               self.previousPrintChar = ' '
            else:
               self.previousResult = ''
               self.previousPrintChar = ''
