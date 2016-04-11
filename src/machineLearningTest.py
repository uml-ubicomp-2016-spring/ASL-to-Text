from sklearn import datasets
iris = datasets .load_iris()
digits = datasets.load_digits()

from sklearn import svm
import numpy as np
myData = np.array([[1, 2, 3], [4, 5, 6]], np.int32)
myTargets = np.array([-1, -2], np.int32)

myClf = svm.SVC()
myClf.fit(myData, myTargets)

print(myClf.predict([[1, 2, 3]]))
print(myClf.predict([[1, 2, 4]]))
print(myClf.predict([[4, 5, 6]]))
print(myClf.predict([[4, 5, 7]]))
