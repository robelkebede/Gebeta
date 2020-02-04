#import gym
import numpy as np
import random
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import Adam
from collections import deque

class DQN:
    def __init__(self):
        
        self.memory  = deque(maxlen=2000)
        
        self.gamma = 0.85
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.005
        self.tau = .125
        self.action_space = 6

        self.model = self.create_model()
        self.target_model = self.create_model()
        self.observation_space = 100

    def create_model(self):
        model   = Sequential()
        #state_shape  = self.env.observation_space.shape
        model.add(Dense(24, input_shape=(1,), activation="relu"))
        model.add(Dense(8, activation="relu"))
        model.add(Dense(16, activation="relu"))
        model.add(Dense(self.action_space,activation="sigmoid"))
        model.compile(loss="mean_squared_error",
            optimizer=Adam(lr=self.learning_rate))
        return model

    def act(self, state):
        self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon_min, self.epsilon)
        if np.random.random() < self.epsilon:
            return np.random.randint(6)

        print("STATE SHAPE",state.reshape(-1).shape)
        return np.argmax(self.model.predict(state.reshape(-1))[0])
        

    def remember(self, state, action, reward, new_state, done):
        self.memory.append([state, action, reward, new_state, done])

    def replay(self):
        batch_size = 32
        if len(self.memory) < batch_size: 
            return

        samples = random.sample(self.memory, batch_size)
        for sample in samples:
            state, action, reward, new_state, done = sample
            target = self.target_model.predict(state.reshape(-1))
            #target = 2
            if done:
                target[0][action] = reward
            else:
                Q_future = max(self.target_model.predict(new_state.reshape(-1))[0])
                target[0][action] = reward + Q_future * self.gamma
            self.model.fit(state.reshape(-1), target, epochs=1, verbose=0)

    def target_train(self):
        weights = self.model.get_weights()
        target_weights = self.target_model.get_weights()
        for i in range(len(target_weights)):
            target_weights[i] = weights[i] * self.tau + target_weights[i] * (1 - self.tau)
        self.target_model.set_weights(target_weights)

    def save_model(self, fn):
        self.model.save(fn)

def main():
    observation_space = 50
    action_space = 6
    Q = np.zeros([observation_space,action_space])
    lr = 0.8
    y = .33
    num_ep = 500
    r_list = []

        


if __name__ == "__main__":

    main()
