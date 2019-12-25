
import random
import joblib
import numpy as np

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
        print(action)
        return predicted_action

if __name__ == "__main__":
    
    board_position = np.array([[4,4,4,4,4,4],[4,4,4,4,4,4]])
    a = Agent(2)
    print(np.argmax(a.neural_action(board_position)))





