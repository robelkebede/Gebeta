#from torch_dqn.Tensor.model import QLearningModel
#from model import QLearningModel
import random
from keras.callbacks import TensorBoard
from keras.layers import Dense,Input,Activation
from keras.models import Sequential,Model
from keras.optimizers import Adam
from collections import deque,namedtuple
import time
import numpy as np

UPDATE_EVERY = 4
BUFFER_SIZE = int(1e5)
GAMMA = 0.99
BATCH_SIZE = 64
MODEL_NAME = "model_name"


class Agent:
    
    def __init__(self, state_size, action_size, seed):

        self.state_size = state_size
        self.action_size = action_size
        self.seed = random.seed(seed)

        # main model (fit)
        self.model = self.create_model(state_size,action_size)

        # Target model (predict)
        self.target_model = self.create_model(state_size,action_size)
        self.target_model.set_weights(self.model.get_weights())

        #self.replay_memory = deque(maxlen=BUFFER_SIZE)
        self.memory = ReplayBuffer(self.action_size, BUFFER_SIZE, BATCH_SIZE, 0)
        self.tensorboard = TensorBoard(log_dir="logs/{}-{}".format(MODEL_NAME,int(time.time())))

        self.t_step = 0 # time step
        self.target_update_counter = 0

    
    def step(self, state, action, reward, next_state, done):
        
        self.memory.add(state, action, reward, next_state, done)

        self.t_step = (self.t_step + 1) % UPDATE_EVERY #what is this
        if self.t_step == 0:
            if len(self.memory) > BATCH_SIZE:
                experiences = self.memory.sample()
                self.learn(experiences, GAMMA)

    def act(self, state, eps=0.):
        
        state = np.array([state])

        action_values = self.target_model.predict(state)

        if random.random() > eps:
            return np.argmax(action_values)
        else:
            return random.choice(np.arange(self.action_size))

    
    def learn(self, experiences, gamma):

        states, actions, rewards, next_states, dones = experiences
        

        Q_targets_next = self.target_model.predict(np.array(next_states))
        Q_expected = self.model.predict(np.array(states))

        Q_targets = rewards + (gamma * Q_targets_next * (1 - dones))

        actions = [i[0] for i in actions]

        Q_expected[actions] = Q_targets
        
        self.model.fit(np.array(states),np.array(Q_expected),
                batch_size=64,verbose=0,shuffle=False)

        """
        # Compute loss
        loss = F.mse_loss(Q_expected, Q_targets)
        # Minimize the loss
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step() """

        # ------------------- update target network ------------------- # Tensorflow
        self.soft_update(self.model, self.target_model)

    def get_qs(self,state,step):
        return self.model_predict(np.array(state.reshape(-1)))


    def soft_update(self, local_model, target_model):

        self.target_model.set_weights(self.model.get_weights())


    def create_model(self,state_size,action_size):

        inputs = Input(name='inputs',shape=(state_size,))
        layer = Dense(64,name='FC1')(inputs)
        layer = Activation('relu')(layer)
        layer = Dense(64,name='FC2')(layer)
        layer = Activation('relu')(layer)

        layer = Dense(action_size,activation="linear")(layer)
        model = Model(inputs=inputs,outputs=layer)
        model.compile(loss="mse",optimizer=Adam(lr=0.001),metrics=['accuracy'])

        return model

                
class ReplayBuffer:

    def __init__(self, action_size, buffer_size, batch_size, seed):
        
        self.action_size = action_size
        self.memory = deque(maxlen=buffer_size)
        self.batch_size = batch_size
        self.experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])
        self.seed = random.seed(seed)

    def add(self, state, action, reward, next_state, done):
        e = self.experience(state, action, reward, next_state, done)
        self.memory.append(e)

    def sample(self):
        experiences = random.sample(self.memory, k=self.batch_size)

        states = np.vstack([e.state for e in experiences if e is not None])
        actions = np.vstack([e.action for e in experiences if e is not None])
        rewards = np.vstack([e.reward for e in experiences if e is not None])
        next_states = np.vstack([e.next_state for e in experiences if e is not None])
        dones = np.vstack([e.done for e in experiences if e is not None])

        return (states, actions, rewards, next_states, dones)

    def __len__(self):
        return len(self.memory)


if __name__ == "__main__":

    agent = Agent(12,6,0)
    state = np.array([[4,4,4,4,4,4],[4,4,4,4,4,4]])
    state = state.reshape(-1)
    print(state.shape)
    print(state)
    m = agent.act(state.reshape((12,)))

    print(m)

    


