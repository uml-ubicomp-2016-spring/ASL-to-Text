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

data = np.array([data.A_angles, data.B_angles, data.C_angles])
targets = np.array(['A', 'B', 'C'])
compare = DataCompare(data, targets)
print(compare.matchGesture(np.array(data[1])))
