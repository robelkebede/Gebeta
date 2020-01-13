import numpy as np
import time
import tkinter as tk
from tkinter import ttk

board_position = np.array([[4,4,4,4,4,4],
            [4,4,4,4,4,4]])

p0_score = 0
p1_score = 0

def counter_clockwise():

    #12 if all the holes are filled with stones
    moves = []
    for i in range(12): # 12+score
        if i<6:
            moves.append([0,(i-5)*-1])

        else:

            moves.append([1,i-6])

    return moves


def moves(player_id):

    #score player 0 after [0][0] 
    #score player 1 after [1][5] 
    #update score when you see [9,9]

    moves1 = None
    final_move = []
    if player_id ==0:

        moves1 = [[0, 5], [0, 4], [0, 3], [0, 2], [0, 1], [0, 0],[9,9],
                [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5]]

    else:

        moves1 = [[0, 5], [0, 4], [0, 3], [0, 2], [0, 1], [0, 0], 
                [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5],[9,9]]

    done = 0
    while done<5000:
            for m in moves1:
                final_move.append(m)
            done+=1

    return final_move

def start_pos(player_id,pos_x,pos_y):
    
    move = moves(player_id)
    pos = [pos_x,pos_y]
    start_ = None
    for i in range(12):
        if move[i] == pos:
            start_ = i

    move = move[start_:-1]
    return move


unit = 40
m_h = 2
m_w = 6


def learn():

    win = tk.Tk()

    win.title("BOARD")
    win.resizable(False,False)

    
    ttk.Label(win,text='the lable').grid(column=0,row=0)

    win.mainloop()



if __name__ == "__main__":
    learn()








