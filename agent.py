
import random

class Agent():
    def __init__(self,num):
        self.num = num

    def action(self,player_id):
        #legal moves        
        if player_id==0:
            return [0,random.randint(0,5)]
        else:
            return [1,random.randint(0,5)]


