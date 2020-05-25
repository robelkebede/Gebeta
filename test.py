import matplotlib.pyplot as plt
import numpy as np

def smooth(y,box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y,box,mode='same')
    return y_smooth

y = np.load("reward.npy")
x = [i for i in range(len(y))]

y_ = smooth(y,25)

plt.xlabel('number of moves in the game')
plt.ylabel('score')

plt.plot(x,y)
plt.plot(x,y_,color="red")
plt.show()

