#! /usr/bin/env python

import pygame
import numpy as np
import time
from gebeta import Gebeta
from agent import Agent
 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
 
WIDTH = 50
HEIGHT = 50
MARGIN = 5

grid = []
for row in range(2):
    grid.append([])
    for column in range(6):
        grid[row].append(0) 
 
#numpy array and chenge values for test
grid = np.array(grid)
grid[0][0] = 4
grid[1][1] =1
 
pygame.init()

#TODO score p0,p1 display on the screen
#TODO num_itration
#TODO legal and illagal moves
#TODO tera (the main problem) (MAX_PRIORITY)

screen = pygame.display.set_mode([350, 260])
font = pygame.font.SysFont("Courier New", 24)
pygame.display.set_caption("Gebeta-ገበጣ")

done = False
clock = pygame.time.Clock()

#game classes
gebeta = Gebeta()
agent = Agent(2)

grid = gebeta.board()

x=0
player_0 = 0
player_1 = 0

score_0 =[]
score_1 = []


while not done:

       
    for event in pygame.event.get():  # User did something
        print(grid) 
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop

        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (WIDTH + MARGIN)
            row = pos[1] // (HEIGHT + MARGIN)
            #how to 
            try:
                                     
                board_position,p0s,p1s,num_iter,pos = gebeta.play(grid,1,1,int(column)) 
                print("in grid ",[p0s,p1s])

                player_0+=p0s
                score_0.append(p0s)
                score_1.append(p1s)

                grid = board_position

                #THIS IS AI
                time.sleep(1)
                print("score 0 => ",p0s)
                action = agent.play_rl(grid)
                board_position,p0s,p1s,num_iter,pos = gebeta.play(grid,0,0,action)
                player_1+=p1s

                score_1.append(p1s)
                score_0.append(p0s)

                print("in grid ",[p0s,p1s])
                
                print("score 1 =>",p1s)
                grid = board_position

                print("player_value ",[score_0,score_1])
                print("player_final ",[sum(score_0),sum(score_1)])


                
            except IndexError:
                pass


    screen.fill(WHITE)

    if gebeta.end_game(grid):
            done = True
            print(" GAME_ENDED ")
            board = gebeta.board()
            break

    x+=1
    
    # Draw the grid and values inside
    for row in range(2):
        for column in range(6):
            rect = pygame.Rect([(MARGIN + WIDTH) * column + MARGIN,
                (MARGIN + HEIGHT) * row + MARGIN,WIDTH,HEIGHT])
            color = BLACK
            pygame.draw.rect(screen,
                             color,
                             rect,2)
            
            text = font.render(str(grid[row][column]), True, RED) 
            screen.blit(text, (rect.right-35, rect.top+10))

            num_iter = font.render("num of iter : "+str(x), True, RED) 
            screen.blit(num_iter, (10,150))

            num_iter = font.render("player_0 : "+str(sum(score_0)), True, RED) 
            screen.blit(num_iter, (10,190))

            num_iter = font.render("player_1 : "+str(sum(score_1)), True, RED) 
            screen.blit(num_iter, (10,210))


    
     
 
    clock.tick(60)
    pygame.display.flip()
