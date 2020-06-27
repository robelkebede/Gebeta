#! /usr/bin/env python

import time
import random
import torch
import joblib
import numpy as np
from gebeta import Gebeta
from termcolor import colored
import matplotlib.pyplot as plt
#from dqn import DQN
from torch_dqn.agent import Agent
#from torch_dqn.Tensor.agent import Agent
import argparse

np.random.seed(0)
agent_torch = Agent(state_size=12, action_size=6, seed=0)

class Agent():
    def __init__(self,num):
        self.num = num
        #self.model = agent_torch.qnetwork_local.load_state_dict(torch.load('checkpoint.pth'))
        self.model = None

    def action(self,player_id):
        
        if player_id==0:
            return [0,random.randint(0,5)]
        else:
            return [1,random.randint(0,5)]
    
    # fix this shit
    def reward(self,r,j):
        if r == 0 :
            return -1
        else:
            if j>30:
                return 10
            return r
    
    def play_deep(self,state):
        action = agent_torch.act(state)
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
        #dqn_agent = DQN()
        eps_start =1.0
        eps_end=0.01
        eps = eps_start
        for i in range(num_ep):

                r_all = 0 #reward (ALL)
                j = 0
                Done = False
                board = gebeta.board()

                while not Done:

                    s = board
                    #self play
                    if j%2 == 0:

                        a = agent_torch.act(s.reshape(-1), eps)
                        s1,r,p1,it,pos = gebeta.play(s,0,0,a)
                        #r = self.reward(r,j)
                        agent_torch.step(s.reshape(-1), a, r, s1.reshape(-1),Done)
                        s = s1
                        #print("next state ",s1)
                        r_all+= r
                        board = s1
                        
                    else:
                        action = np.random.randint(6)
                        s1,_,r,_,_ = gebeta.play(s,1,1,action)
                        board = s1
                        s = s1

                    j+=1
                    eps = max(eps_end, 0.99*eps)

                    if gebeta.end_game(board) or j>60:
                        Done = True
                        board = gebeta.board()
                        print(colored("GAME ENDED","red"),i)
                        break

                r_list.append(r_all)

        print(len(r_list))
        plt.plot(r_list)
        torch.save(agent_torch.qnetwork_local.state_dict(), './models/model.pth')
        np.save("reward_torch.npy",r_list)
        plt.show() 


if __name__ == "__main__":
    
    board_position = np.array([[4,4,4,4,4,4],[4,4,4,4,4,4]])
    agent = Agent(2)
    gebeta = Gebeta()
    agent.deep_rl(gebeta)
