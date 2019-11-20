import numpy as np

class Gebeta():
    def __init__(self):

        self.score_player_0 = 0
        self.score_player_1 = 0
        self.board_position = None

    def board(self):
        
        self.board_position = np.array([[4,4,4,4,4,4],
                [4,4,4,4,4,4]])
        
        return self.board_position

    def moves(self,player_id):

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


    def end_game(self,board):

        board = self.board()
        p0 = all(1 ==i for i in board[0])
        p1 = all(1 ==i for i in board[1])

        if p0 or p1 is True:
            print("Score p0 {} p2 {}".format(self.score_player_0,self.score_player_1))
            return p0 


    def start_pos(self,player_id,pos_x,pos_y):
        
        move = self.moves(player_id)
        pos = [pos_x,pos_y]
        start_ = None
        for i in range(12):
            if move[i] == pos:
                start_ = i

        move = move[start_:-1]
        return move


    def play(self,player_id,pos_x,pos_y):
        #acesses denied when player is trying to acsses another position
        #move starting point
        game_pos = self.start_pos(player_id,pos_x,pos_y)
        #x = game_pos[0][0]
        hole_value = self.board_position[game_pos[0][0],game_pos[0][1]]
        self.board_position[game_pos[0][0],game_pos[0][1]] = 0


        # done for transition to the second player
        player_id_score = 0

        for i in range(1,10000):
            
            #end game for player 1
            if hole_value == 0:
                break
            
            if game_pos[i][0] == 9:

                if player_id == 0:
                    self.score_player_0 += 1
                    hole_value -=1
            else:
                if hole_value == 1:
                    hole_value = self.board_position[game_pos[i][0],game_pos[i][1]] +1
                    self.board_position[game_pos[i][0],game_pos[i][1]] =0
                else:
                    #print(hole_value)
                    self.board_position[game_pos[i][0],game_pos[i][1]] +=1
                    hole_value -= 1

        
        print(self.board_position)
        #rint(self.score_player_0)

    
    
def main():
    ge = Gebeta()
    board = ge.board()
    
    while True:
        if ge.end_game(board):
            break

        player_input = input()
        print(player_input[0])
        ge.play(player_input[0],player_input[1],player_input[2])
          

    #ge.board()
    #ge.play(0,0,5) 

if __name__ == "__main__":
    main()
