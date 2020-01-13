import numpy as np
from collections import Counter


data = np.load("data10000x.npy")

state = np.array([[4,4,4,4,4,4],
                  [4,4,4,4,4,4]])


state2 = np.array([[0,1,7,0,6,0],
                    [0,1,3,1,6,2]])


state3 = np.array([[1,5,5,5,0,0],
           [5,15,0,1,1,5]])

state4 = np.array([[0,4,1,1,1,1],
                   [8,2,3,8,1,8]])


m = [1,4,34]
print(data[m])

exit()
predicted = data[state4]

value = [np.argmax(i) for i in predicted[0]]

print(predicted[0])
print(value)
print(np.argmax(value))
"""
print(state2[0])
print(predicted[0])

#print(data[state2].shape) """


