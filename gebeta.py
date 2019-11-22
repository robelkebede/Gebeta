import numpy as np

class Gebeta():
    def __init__(self):

        self.score_player_0 = 0
        self.score_player_1 = 0
        self.board_position = None 

    def board(self):
        
        #self.board_position = np.array([[4-3,4-3,4-3,4-3,4-3,4-3],[4-3,4-3,4-3,4-3,4-3,4-3]])
        self.board_position = np.array([[4,4,4,4,4,4],[4,4,4,4,4,4]])
        return self.board_position

    def update(self,board):
        self.board_position = board

    def moves(self,player_id):

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


    def play(self,board_position,player_id,pos_x,pos_y,p0s=0,p1s=0):
        #acesses denied when player is trying to acsses another position
        #move starting point
        game_pos = self.start_pos(player_id,pos_x,pos_y)
        hole_value = board_position[game_pos[0][0],game_pos[0][1]]
        board_position[game_pos[0][0],game_pos[0][1]] = 0

        #print([hole_value,board_position])
        num_iter = 0

        for i in range(1,10000):
            num_iter += 1 
            if hole_value == 0:
                break #end game
            
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
                    board_position[game_pos[i][0],game_pos[i][1]] =0
                else:
                    board_position[game_pos[i][0],game_pos[i][1]] +=1
                    hole_value -= 1

        return  board_position,p0s,p1s,num_iter,game_pos


    
    
def main():

    from agent import Agent

    ge = Gebeta()
    board = ge.board()

    s0 = 0
    s1 = 0

    agent = Agent(2)
    x=1

    for i in range(10): #num of games 

        while True: 
            #player_input = input()
            """ 
            board_position,p0s,p1s,num_iter,pos = ge.play(board,int(player_input[0]),
                    int(player_input[1]),int(player_input[2]),s0,s1) """


            print("#######################################################################") 

            action = agent.action(x%2)
            board_position,p0s,p1s,num_iter,pos = ge.play(board,x%2,action[0],action[1])

            s0 = p0s
            s1 = p1s
            #print("Player ",int(player_input[0])) 
            #print("num Iter",num_iter)
            #print("Pos",pos )
            board = board_position

            score = None
            if x%2 == 0:
                score = s0
            else:
                score = s1

            print([board_position,x%2])
            print("Score is {}".format(score))
            print("num Iter {}".format(num_iter))
            
            
            ls0 = s0
            ls1 = s1
            
            #print({"score player 0 ":ls0,"score player 1 ":ls1})

            x+=1

            if ge.end_game(board):
                print("Game {} ended".format(i))
                board = ge.board()
                break

            print("########################################################################")
            



if __name__ == "__main__":
    main()
