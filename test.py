import numpy as np

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



def update_holes(player_id,pos_x,pos_y):
    #acesses denied when player is trying to acsses another position
    #move starting point
    game_pos = start_pos(player_id,pos_x,pos_y)
    #x = game_pos[0][0]
    hole_value = board_position[game_pos[0][0],game_pos[0][1]]
    board_position[game_pos[0][0],game_pos[0][1]] = 0


    # done for transition to the second player
    player_id_score = 0

    for i in range(1,10000):
        
        #end game for player 1
        if hole_value == 0:
            break
        
        if game_pos[i][0] == 9:
            player_id_score +=1
            hole_value -=1
        else:
            if hole_value == 1:
                hole_value = board_position[game_pos[i][0],game_pos[i][1]] +1
                board_position[game_pos[i][0],game_pos[i][1]] =0
            else:
                print(hole_value)
                board_position[game_pos[i][0],game_pos[i][1]] +=1
                hole_value -= 1

    
    print(board_position)
    print(player_id_score)


update_holes(0,0,5)
