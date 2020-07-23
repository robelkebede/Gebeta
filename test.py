import matplotlib.pyplot as plt
import numpy as np

def smooth(y,box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y,box,mode='same')
    return y_smooth

y = np.load("reward.npy")
x = [i for i in range(len(y))]
y_ = smooth(y,25)


plt.xlabel('number of games')
plt.ylabel('score')
plt.plot(x,y)
plt.plot(x[:-24],y_[:-24],color="red")
plt.show()

