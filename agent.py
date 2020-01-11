
import time
import random
import joblib
import numpy as np
from gebeta import Gebeta
from tqdm import tqdm
from termcolor import colored

class Agent():
    def __init__(self,num):
        self.num = num
        self.model = joblib.load("./model/gebeta_model_1")

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
        num_ep = 10
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

                    print("s",s)
                    action = Q[s,:] + np.random.randn(1,action_space)*(1./(i+1))

                    a = np.argmax(action[:,0][0])
                    #a = a-1
                    print(action[0])
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
                    s,r,_,_,_ = gebeta.play(board,1,0,self.action(j%2))   
                    #takes random action from random() method

                j+=1

                #board = s

                if gebeta.end_game(board):
                    Done = True
                    board = gebeta.board()
                    print(colored("GAME ENDED","red"),"who won ",i)
                    time.sleep(0.5)
                    break
        
        #print(gebeta.board())
        print(len(r_list))
        import matplotlib.pyplot as plt
        plt.plot(r_list)
        #np.save("data100",Q)

        plt.show() 


if __name__ == "__main__":
    
    board_position = np.array([[4,4,4,4,4,4],[4,4,4,4,4,4]])
    a = Agent(2)
    gebeta = Gebeta()
    a.rl(gebeta);


