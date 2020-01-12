
import time
import random
import joblib
import numpy as np
from gebeta import Gebeta
from tqdm import tqdm
from termcolor import colored
import matplotlib.pyplot as plt

class Agent():
    def __init__(self,num):
        self.num = num
        self.model = joblib.load("./model/gebeta_model_1")
        self.rl_model = np.load("./data/data10000x.npy")

    def action(self,player_id):
        
        if player_id==0:
            return [0,random.randint(0,5)]
        else:
            return [1,random.randint(0,5)]
    
    def neural_action(self,action):
        predicted_action = self.model.predict(action.reshape(1,-1))
        #print(action)
        return predicted_action

    def reward(self,r):
        if r == 0 :
            return -1
        else:
            return r
    
    def rl(self,gebeta):
        
        observation_space = 100
        action_space = 6
        Q = np.zeros([observation_space,action_space])
        lr = 0.3
        y = .30 #what is this thing
        num_ep = 10000
        r_list = []
        
        for i in range(num_ep):

            r_all = 0 #reward (ALL)
            j = 0
            Done = False
            board = gebeta.board()

            while not Done:

                #SELF PLAY
                #make two reinforcement learning agents play with each other
                #print(board.shape)
                s = board

                if j%2 == 0:
                    #player id is j%2
                    #save action for player 0
                    #action

                    print("AI_agent",s)
                    action = Q[s,:] + np.random.randn(1,action_space)*(1./(i+1))

                    a = np.argmax(action[:,0][0])
                    #a = a-1
                    print("Selected ",a)
                    print(action[:,0][0])
                    #print(a)
                    #print(action.shape)

                    #single play step
                    #function returns (state,reward) 
                    #print(type(a))

                    s1,r,_,_,_ = gebeta.play(s,0,0,a)

                    #update q table
                    #bellman equation
                    r = self.reward(r)
                    print("reward",r)
                    Q[s,a] = Q[s,a] + lr*(r + y*np.max(Q[s1,:]) - Q[s,a])

                    r_all+= r
                    s = s1

                    r_list.append(r_all)

                    #takes random action from rl 
                    print("++++++++++++++++++++++++++++++++++++++++++")
                else:
                    print(s)

                    action = np.random.randint(5)
                    s1,_,r,_,_ = gebeta.play(s,1,0,action)

                    print("Random",s1)
                    print("action",action)
                    print("reward",r)
                    print("++++++++++++++++++++++++++++++++++++++++++")
                    s = s1

                j+=1

                #board = s

                if gebeta.end_game(board) or j>60:
                    Done = True
                    board = gebeta.board()
                    print(colored("GAME ENDED","red"),"who won ",i,j)
                    #time.sleep(0.5)
                    break
        
        print(len(r_list))
        plt.plot(r_list)
        #np.save("data10000x",Q)

        plt.show() 
    def play_rl(self,state):

        action = self.rl_model[state] 
        value = [np.argmax(i) for i in action[0]]
        
        return np.argmax(value)

        


if __name__ == "__main__":
    
    board_position = np.array([[4,4,4,4,4,4],[4,4,4,4,4,4]])
    a = Agent(2)
    gebeta = Gebeta()
    #a.rl(gebeta);
    print(a.play_rl(board_position))


