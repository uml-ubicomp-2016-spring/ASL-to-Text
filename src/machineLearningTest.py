import os, sys, inspect, thread, time
import numpy as np

import csv, re
with open('../data/data.csv', 'rb') as dataFile:
   reader = csv.reader(dataFile)
   numCol=len(next(reader)) # Read first line and count columns
   dataFile.seek(0)              # go back to beginning of file
   numRow = len(list(reader)) # count the number of rows
   dataFile.seek(0)              # go back to beginning of file
   targets = np.empty(numRow, dtype=object)
   data = np.empty([numRow, numCol - 1], np.float64)

   rowCount = 0
   for row in reader: # make an array for each row
      column = -1
    #   target = ''
    #   rowData = np.empty(numCol - 1, np.int32)
      for col in row:
         if column is -1:
            targets[rowCount] = col
         else:
            data[rowCount, column] = col
         column = column + 1 # end of column for loop
      rowCount = rowCount + 1 # end of row for loop

   print(targets)
   print(data)




# from sklearn import datasets
# iris = datasets .load_iris()
# digits = datasets.load_digits()

import distalData as data
from sklearn import svm
import numpy as np
# myData = np.array([[1, 2, 3], [4, 5, 6]], np.int32)
# myTargets = np.array([-1, -2], np.int32)
#
# myClf = svm.SVC()
# myClf.fit(myData, myTargets)
#
# print(myClf.predict([[1, 2, 3]]))
# print(myClf.predict([[1, 2, 4]]))
# print(myClf.predict([[4, 5, 6]]))
# print(myClf.predict([[4, 5, 7]]))



# clf = svm.SVC()
# data = np.array([data.A_angles, data.B_angles, data.C_angles])
# targets = np.array(['A', 'B', 'C'])
# clf.fit(data, targets)
# # print("data")
# # print(data)
# # print("\ntargets")
# # print(targets)
# predictData = np.array(data[1]) # this is the poll from leap motion step
# # print("predictData")
# # print(predictData)
# result = str(clf.predict([predictData]))[2:-2] #predicts which letter this is
# print(result)

# class DataCompare():
#    def __init__(self, data, targets):
#       self.clf = svm.SVC() #this is the single class variable
#     #   data = np.array(angles)
#     #   targets = np.array(targets
#       self.clf.fit(data, targets)
#       print("data")
#       print(data)
#       print("targets")
#       print(targets)
#
#    def matchGesture(self, formattedData):
#       result = str(self.clf.predict([formattedData]))[2:-2] #predicts which letter this is
#     #   print(result)
#       return result #How are we handling things that shouldn't match?
#
# data = np.array([data.A_angles, data.B_angles, data.C_angles])
# targets = np.array(['A', 'B', 'C'])
# compare = DataCompare(data, targets)
# print(compare.matchGesture(np.array(data[1])))
