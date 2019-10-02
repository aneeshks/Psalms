import numpy as np
X = np.array([[1, 2],[2, 1]])
Y = np.reshape(np.array([1,2]),(2,1))
W = (np.linalg.inv(X.dot(X.T))).dot(X.dot(Y))
W
