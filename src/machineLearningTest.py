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



clf = svm.SVC()
data = np.array([data.A_angles, data.B_angles, data.C_angles])
targets = np.array(['A', 'B', 'C'])
clf.fit(data, targets)
# print("data")
# print(data)
# print("\ntargets")
# print(targets)
predictData = np.array(data[1])
# print("predictData")
# print(predictData)
print(clf.predict([predictData]))
