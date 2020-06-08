#! /usr/bin/env python

import time
import random
import joblib
import numpy as np
from gebeta import Gebeta
from termcolor import colored
import matplotlib.pyplot as plt
from dqn import DQN
import argparse

class Agent():
    def __init__(self,num):
        self.num = num
        self.rl_model = np.load("./data/data10000x.npy")

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
        dqn = DQN()      
        return dqn.predict(state)

    def deep_rl(self,gebeta):

        parser = argparse.ArgumentParser()
        parser.add_argument('--episodes',type=int
              ,help='number of episodes'
              ,default=10)
 
        args = parser.parse_args()
        print("EPISODES ",args.episodes)

        num_ep = args.episodes
        r_list = []
        dqn_agent = DQN()
        for i in range(num_ep):

                r_all = 0 #reward (ALL)
                j = 0
                Done = False
                board = gebeta.board()

                while not Done:

                    s = board

                    if j%2 == 0:

                        a = dqn_agent.act(s)

                        #print(s)
                        s1,r,p1,it,pos = gebeta.play(s,0,0,a)

                        r = self.reward(r,j)
                        #print(r)
                        new_state = s1
                        dqn_agent.remember(new_state, a,r, s1, Done)

                        r_list.append(r_all)
                        r_all+= r


                        dqn_agent.replay()
                        dqn_agent.target_train()
                        board = new_state

                        
                    else:
                        action = np.random.randint(6)
                        s1,_,r,_,_ = gebeta.play(s,1,1,action)
                        board = new_state
                        s = s1

                    j+=1


                    if gebeta.end_game(board) or j>60:
                        Done = True
                        board = gebeta.board()
                        print(colored("GAME ENDED","red"),"who won ",i,j)
                        break

        print(len(r_list))
        plt.plot(r_list)
        #np.save("reward_500.npy",r_list)
        #dqn_agent.save_model("./models/model_new_v1.h5")
        plt.show() 


if __name__ == "__main__":
    
    board_position = np.array([[4,4,4,4,4,4],[4,4,4,4,4,4]])
    agent = Agent(2)
    gebeta = Gebeta()
    agent.deep_rl(gebeta)
