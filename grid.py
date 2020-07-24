#! /usr/bin/env python

import os
import pygame
import numpy as np
import time
from gebeta import Gebeta
from agent import Agent

model = None

TORCH = os.getenv("TORCH")

if TORCH is not None:
    import torch
    model = torch.load("./models/model.pkl")
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

else:
    from keras.models import load_model
    model = load_model('./models/model.h5')

class GameUI():

    def __init__(self):

        pygame.init()

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
         
        self.WIDTH = 50
        self.HEIGHT = 50
        self.MARGIN = 5

        self.grid = []

        self.screen = pygame.display.set_mode([350, 260])
        self.font = pygame.font.SysFont("Courier New", 24)
        pygame.display.set_caption("Gebeta-ገበጣ")

        self.clock = pygame.time.Clock()
        
        #game engine and ai agent classes
        self.gebeta = Gebeta()
        self.agent = Agent(2)

    
    def init_board(self):

        for row in range(2):
            self.grid.append([])
            for column in range(6):
                self.grid[row].append(0) 
         
        return self.grid

    def model_predict(self,state):

        state = state.reshape(-1)
        
        if TORCH is not None:

            state = torch.from_numpy(state).float().unsqueeze(0).to(device)
            action_values = model(state)
            return np.argmax(action_values.cpu().data.numpy())
        else:

            return np.argmax(model.predict([[state]]))


    
    def render(self):

        
        score_0 =[] # player 0
        score_1 = []# player 1
        iter_ = 0
        act = None
        done = False

        self.grid = self.gebeta.board()

        while not done:
               
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    done = True  

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    column = pos[0] // (self.WIDTH + self.MARGIN)
                    row = pos[1] // (self.HEIGHT + self.MARGIN)
                    try:
                        
                        print(self.grid) 
                        if row == 1:

                            #HUMAN PLAYER
                            board_position,p0s,p1s,num_iter,pos = self.gebeta.play(self.grid,1,1,int(column)) 
                            print("in grid ",[row,column])

                            score_0.append(p0s)
                            score_1.append(p1s)

                            self.grid = board_position

                            iter_ = num_iter

                            #THIS IS AI
                            time.sleep(1)
                            action = self.model_predict(self.grid)
                            board_position,p0s,p1s,num_iter,pos = self.gebeta.play(self.grid,0,0,action)
                            
                            score_1.append(p1s)
                            score_0.append(p0s)

                            iter_ = num_iter
                            act = action

                            #LOGS
                            self.grid = board_position
                            print("scores ",[sum(score_0),sum(score_1)])
                        else:
                            print("ILLAGAL MOVE")
                            
                    except IndexError:
                        pass


            self.screen.fill(self.WHITE)

            if self.gebeta.end_game(self.grid):
                    done = True
                    print(" GAME_ENDED ")
                    board = self.gebeta.board()
                    break

            
            # Draw the grid 
            for row in range(2):
                for column in range(6):
                    rect = pygame.Rect([(self.MARGIN + self.WIDTH) * column + self.MARGIN,
                        (self.MARGIN + self.HEIGHT) * row + self.MARGIN,self.WIDTH,self.HEIGHT])
                    color = self.BLACK
                    pygame.draw.rect(self.screen,
                                     color,
                                     rect,2)
                    
                    text = self.font.render(str(self.grid[row][column]), True, self.RED) 
                    self.screen.blit(text, (rect.right-35, rect.top+10))

                    num_iter = self.font.render("AI iter : "+str(iter_), True, self.BLUE) 
                    self.screen.blit(num_iter, (10,150))

                    num_iter = self.font.render("AI action : "+str(act), True, self.BLUE) 
                    self.screen.blit(num_iter, (10,170))


                    num_iter = self.font.render("AI score: "+str([sum(score_0)]), True, self.BLUE) 
                    self.screen.blit(num_iter, (10,190))

                    num_iter = self.font.render("player_1: "+str([sum(score_1)]), True, self.RED) 
                    self.screen.blit(num_iter, (10,220))

         
            self.clock.tick(60)
            pygame.display.flip()



def main():

    gameui = GameUI()
    gameui.render()


if __name__ == "__main__":
    main()
