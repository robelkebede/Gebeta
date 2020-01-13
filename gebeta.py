#! /usr/bin/env python3

import numpy as np

class Gebeta():
    def __init__(self):

        self.score_player_0 = 0
        self.score_player_1 = 0
        self.board_position = None 

    def board(self):
                
        self.board_position = np.array([[4,4,4,4,4,4],[4,4,4,4,4,4]])
        return self.board_position

    def moves(self,player_id):

        #Legal moves
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


    def end_game(self,board):

        p0 = all(0 ==i for i in board[0])
        p1 = all(0 ==i for i in board[1])

        if p0 or p1 == True:
             
            return True
        else:
            return False

    def start_pos(self,player_id,pos_x,pos_y):
        
        move = self.moves(player_id)
        pos = [pos_x,pos_y]
        start_ = None
        for i in range(12):
            if move[i] == pos:
                start_ = i

        move = move[start_:-1]
        return move

    #   move
    def play(self,board_position,player_id,pos_x,pos_y,p0s=0,p1s=0):

        game_pos = self.start_pos(player_id,pos_x,pos_y)
        hole_value = board_position[game_pos[0][0],game_pos[0][1]]
        board_position[game_pos[0][0],game_pos[0][1]] = 0

        num_iter = 0

        for i in range(1,10000):
            num_iter += 1 
            if hole_value == 0:
                #end game
                break 
            
            if game_pos[i][0] == 9:

                if player_id == 0:
                    p0s += 1
                    hole_value -=1
                else:
                    p1s += 1
                    hole_value -=1

            else:

                if hole_value == 1:
                    hole_value = board_position[game_pos[i][0],game_pos[i][1]] +1
                    board_position[game_pos[i][0],game_pos[i][1]] = 0
                else:
                    board_position[game_pos[i][0],game_pos[i][1]] +=1
                    hole_value -= 1

        return  board_position,p0s,p1s,num_iter,game_pos


def main():

    from agent import Agent

    ge = Gebeta()
    agent = Agent(2)

    board = ge.board()
    Done = False
    
    p0s = 0
    p1s = 0

    total_score_p0 = 0
    total_score_p1 = 0
    x=0

    while not Done:

        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++") 
        if x%2==0:
            #AI

            #action = agent.neural_action(board)
            action = agent.play_rl(board)
            board_position,p0s,p1s,num_iter,pos = ge.play(board,0,0,action)
            print("action =>",action)
            print(board_position)
        else:
            #HUMAN
            player_input = input()
            board_position,p0s,p1s,num_iter,pos = ge.play(board,1,1,int(player_input[0])) 

            print("action =>",player_input[0])
            print(board_position)

        
        if x%2 == 0:
            total_score_p0 += p0s
        else:
            score = p1s
            total_score_p1 += p1s

        print("Player 0={} Player 1={}".format(total_score_p0,total_score_p1)) 

        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++") 
        
        
        board = board_position

        if ge.end_game(board):
            Done = True
            print(" GAME_ENDED ")
            board = ge.board()
            break

        x+=1


if __name__ == "__main__":
    main()
