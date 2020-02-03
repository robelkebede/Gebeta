
import time
import random
import joblib
import numpy as np
from gebeta import Gebeta
from termcolor import colored
import matplotlib.pyplot as plt
from dqn import DQN

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
            return r


    def rl(self,gebeta):
        
        observation_space = 50
        action_space = 6
        Q = np.zeros([observation_space,action_space])
        lr = 0.8
        y = .33#what is this thing
        num_ep = 10
        r_list = []
        
        for i in range(num_ep):

            r_all = 0 #reward (ALL)
            j = 0
            Done = False
            board = gebeta.board()

            while not Done:

                s = board

                if j%2 == 0:
                    print("AI_agent",s)
                    action = Q[s,:] + np.random.randn(1,action_space)*(1./(i+1))

                    a = np.argmax(action[:,0][0])
                    
                    print("Selected ",a)
                    print(action[:,0][0])

                    s1,r,_,_,_ = gebeta.play(s,0,0,a)
                    
                    r = self.reward(r,j)
                    print("reward",r)
                    
                    Q[s,a] = Q[s,a] + lr*(r + y*np.max(Q[s1,:]) - Q[s,a])

                    r_all+= r
                    s = s1

                    r_list.append(r_all)

                    print("++++++++++++++++++++++++++++++++++++++++++")
                else:
                    print(s)
                    action = np.random.randint(5)
                    s1,_,r,_,_ = gebeta.play(s,1,1,action)

                    print("Random",s1)
                    print("action",action)
                    print("reward",r)
                    print("++++++++++++++++++++++++++++++++++++++++++")
                    s = s1

                j+=1

                if gebeta.end_game(board) or j>60:
                    Done = True
                    board = gebeta.board()
                    print(colored("GAME ENDED","red"),"who won ",i,j)
                    #time.sleep(0.5)
                    break
        
        print(len(r_list))
        plt.plot(r_list)
        #np.save("data100000x",Q)
        plt.show() 

   
    def play_rl(self,state):

        action = self.rl_model[state] 
        value = [np.argmax(i) for i in action[0]]
        
        return np.argmax(value)


    def play_deep_rl(self,gebeta):

        num_ep = 100
        r_list = []
        for i in range(num_ep):

                r_all = 0 #reward (ALL)
                j = 0
                Done = False
                board = gebeta.board()
                dqn_agent = DQN()

                while not Done:

                    s = board


                    if j%2 == 0:

                        action = dqn_agent.act(s)

                        s1,r,p1,_,_ = gebeta.play(s,0,0,a)


                        r = self.reward(r,j)
                        print(r)
                        new_state = s1.reshape(2,6)
                        dqn_agent.remember(new_state, action,r, s1, Done)

                        r_all+= r

                        r_list.append(r_all)

                        dqn_agent.replay()
                        dqn_agent.target_train()
                        board = new_state

                        print("AI",new_state)
                        print("action",action)
                        print("reward",r)
                        print("#########################################")


                    else:
                        action = np.random.randint(5)
                        s1,_,r,_,_ = gebeta.play(s,1,1,action)
                        board = new_state

                        print("Random",s1)
                        print("action",action)
                        print("reward",r)
                        print("++++++++++++++++++++++++++++++++++++++++++")
                        s = s1

                    j+=1

                    if gebeta.end_game(board) or j>60:
                        Done = True
                        board = gebeta.board()
                        print(colored("GAME ENDED","red"),"who won ",i,j)
                        #time.sleep(0.5)
                        break

        print(len(r_list))
        plt.plot(r_list)
        #np.save("data100000x",Q)
        plt.show() 



if __name__ == "__main__":
    
    board_position = np.array([[4,4,4,4,4,4],[4,4,4,4,4,4]])
    a = Agent(2)
    gebeta = Gebeta()
    #a.rl(gebeta)
    #print(a.play_rl(board_position))

    a.play_deep_rl(gebeta) 


