import numpy as np
import keras
from keras.layers import Dense,Input
from keras.activations import relu
from keras.optimizers import Adam




class QLearningModel(keras.Model):

    def __init__(self,state_size,action_size,seed,fc1_units=64,fc2_units=64):
        super(QLearningModel,self).__init__()
        self.dense1 = Input(state_size,(1,)) # this should be Input
        self.dense2 = Dense(fc1_units, activation=relu)
        self.dense3 = Dense(fc2_units, activation=relu)
        

    def call(self,inputs):
        x = self.dense1(inputs)
        x = self.dense2(x)
        x = self.dense3(x)
        x = x.compile(loss="mse",batch_size=2,optimizer=Adam(lr=0.001),metrics=["accuracy"])
        return x



if __name__ == "__main__":

    state = np.array([[4,4,4,4,4,4],[4,4,4,4,4,4]]).reshape(-1)
    #state = np.array([4,4,4,4,4,4,4,4,4,4,4,4])
    #state = [4,4,4,4,4,4,4,4,4,4,4,4]
    #print(state.shape)
    q = QLearningModel(12,5,0)
    #q(state)
    print(dir(q))
