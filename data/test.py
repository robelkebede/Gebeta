import numpy as np


data = np.load("data50.npy")

state = np.array([[4,4,4,4,4,4],
                  [4,4,4,4,4,4]])


state2 = np.array([[0,1,7,0,6,0],
                    [0,1,3,1,6,2]])

print(state2[0])


predicted = data[state2[0]]
print(predicted[0])

#print(data[state2].shape)


