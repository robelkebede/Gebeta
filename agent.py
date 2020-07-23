#! /usr/bin/env python

import os
import time
import random
import joblib
import numpy as np
from gebeta import Gebeta
from termcolor import colored
import matplotlib.pyplot as plt

TORCH = os.getenv("TORCH")

if TORCH is not None:
    import torch
    from torch_dqn.agent import Agent
    print("running pytorch")
else:
    from tensor_dqn.agent import Agent
    print("running tensorflow")

import argparse

np.random.seed(0)
agent_dqn = Agent(state_size=12, action_size=6, seed=0)

class Agent():
    def __init__(self,num):
        self.num = num
        self.eps_start =1.0
        self.eps_end=0.01
        self.eps = self.eps_start

    def play_deep_torch(self,state):
        action = agent_dqn.act(state)
        return action
   
    def play_deep_tensor(self,state):
        action = agent_dqn.act(state)
        return action

    def deep_rl(self,gebeta):

        parser = argparse.ArgumentParser()
        parser.add_argument('--episodes',type=int
              ,help='number of episodes'
              ,default=10)
 
        args = parser.parse_args()
        print("EPISODES ",args.episodes)

        num_ep = args.episodes
        r_list = []
        
        for i in range(num_ep):

                r_all = 0 #reward all from a single episode
                j = 0 # turn counter
                Done = False
                board = gebeta.board()

                while not Done:

                    state = board
                    #self play with random agent
                    if j%2 == 0:

                        action = agent_dqn.act(state.reshape(-1), self.eps)
                        #(state,reward,point_p1,iter,pos)
                        s1,reward,p1,it,pos = gebeta.play(state,0,0,action)
                        
                        agent_dqn.step(state.reshape(-1), action, reward, s1.reshape(-1),Done)
                        state = s1
                        r_all+= reward
                        board = s1
                        
                    else:
                        action = np.random.randint(6)
                        s1,_,r,_,_ = gebeta.play(state,1,1,action)
                        board = s1
                        state = s1

                    j+=1
                    self.eps = max(self.eps_end, 0.99*self.eps) #eps decay

                    if gebeta.end_game(board) or j>60:
                        Done = True
                        board = gebeta.board()
                        print(colored("GAME ENDED","red"),i)
                        break

                r_list.append(r_all)

        print(len(r_list))
        plt.plot(r_list)
        np.save("reward.npy",r_list)
        """
        if TORCH is not None:
            torch.save(agent_dqn.qnetwork_local.state_dict(), './models/model_torch.pth')
        else:
            #save model for tensorflow
            agent_dqn.target_model.save("./models/model_tensor.h5") """

        plt.show() 

if __name__ == "__main__":
    
    board_position = np.array([[4,4,4,4,4,4],[4,4,4,4,4,4]])
    agent = Agent(2)
    gebeta = Gebeta()
    agent.deep_rl(gebeta)
