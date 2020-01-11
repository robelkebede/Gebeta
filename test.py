import numpy as np
import time
import tkinter as tk

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

class display(tk.Tk,object):

    def __init__(self):
        super(display,self).__init__()
        self.action_space = [1,2,3,4,5,6]
        self.num_actions = len(self.action_space)
        self.n_features = 2
        self.title('Gebeta')
        self.geometry('{0}x{1}'.format(m_h * 120, m_w * unit))
        self._build_maze()


    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                             height=m_h * unit,
                             width=m_w * unit)

        
        for c in range(0, m_w * unit, unit):
            x0, y0, x1, y1 = c, 0, c, m_h * unit
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, m_h * unit, unit):
            x0, y0, x1, y1 = 0, r, m_w * unit, r
            self.canvas.create_line(x0, y0, x1, y1)

        origin = np.array([20, 20])

        score0 = tk.Label(self, text="score0 is x ") # Create a text label
        score0.pack(padx=20, pady=10) # Pack it into the window

        score1 = tk.Label(self, text="score1 is x ") # Create a text label
        score1.pack(padx=10, pady=0) # Pack it into the window

        #change this into number

        """ 
        oval_center = origin + unit * 2
        self.oval = self.canvas.create_oval(
            oval_center[0] - 15, oval_center[1] - 15,
            oval_center[0] + 15, oval_center[1] + 15,
            fill='yellow')

        """
         # create oval
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')

        # pack all
        self.canvas.pack()



    def reset(self):
         self.update()
         time.sleep(0.1)
         self.canvas.delete(self.rect)
         origin = np.array([20, 20])
         #initial point
         self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15,
            fill='red')
         # return observation
         return (np.array(self.canvas.coords(self.rect)[:2]) - 
              np.array(self.canvas.coords(self.oval)[:2]))/(    m_h*unit)

    
    def step(self):
        if action == 0:   # zero
            if s[1] >unit :
                base_action[1] -= unit
        elif action == 1:   #one 
            if s[1] < (m_h - 1) * unit:
                base_action[1] += unit
        elif action == 2:   # two
            if s[0] < (m_w - 1) * unit:
                base_action[0] += unit
        elif action == 3:   # three
            if s[0] > unit:
                base_action[0] -= unit
        elif action == 4:   # four
            if s[0] > unit:
                base_action[0] -= unit
        elif action == 5:   # five
            if s[0] > unit:
                base_action[0] -= unit

        
        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent

        next_coords = self.canvas.coords(self.rect)  # next state





    
    def render(self):
        self.update()




def main():
    te = display()
    for i in range(40):
        te.reset()
        for x in range(30):
            te.render()


if __name__ == "__main__":
    main()








