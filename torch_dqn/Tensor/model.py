import numpy as np
import keras
from keras.layers import Dense
from keras.activations import relu

class QLearningModel(keras.Model):

    def __init__(self,state_size,action_size,seed,fc1_units=64,fc2_units=64):
        super(QLearningModel,self).__init__()
        self.dense1 = Dense(state_size, activation=relu)
        self.dense2 = Dense(fc1_units, activation=relu)
        self.dense3 = Dense(fc2_units, activation=relu)

    def call(self,inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        return self.dense3(x)



if __name__ == "__main__":
    q = QLearningModel(12,5,0)
    #print(q.evaluate())
    print(dir(q))
