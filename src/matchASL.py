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
