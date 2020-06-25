import numpy as np
import keras
from kears.layers import Dense
from keras.activation import relu


class QLearningModel(keras.model):

    def __init__(self,):
        super(QLearningModel,self).__init__()
        self.dense1 = Dense(4, activation=relu)
        self.dense2 = Dense(4, activation=relu)


