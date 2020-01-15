from tkinter import Tk, Text, BOTH, W, N, E, S, ttk
from tkinter.ttk import Frame, Button, Label, Style, Entry

#|----------------------------|
#|		      GRID	   		  |
#|----------------------------|
#|	   	 |toplb1|toplb2|toplb3|
#|leftlb1|entry1|entry2|entry3|
#|leftlb2|entry4|entry5|entry6|
#|----------------------------|


#Adding mesh into table
def command_add_col(self):
	#Create new mesh
	#Find needful element, checkout on row
	
	for i in range(self.row_count):
		mesh_cnt = len(self.mesh_entries)
		mesh_row = self.mesh_entries[mesh_cnt-1][i].grid_info()['row']
		mesh_col = self.mesh_entries[mesh_cnt-1][i].grid_info()['column']+1
		self.mesh_entries[mesh_cnt-1].append(Entry(self))
		self.mesh_entries[mesh_cnt-1][i].grid( row = mesh_row, column = mesh_col)		
		print(self.mesh_entries)
	self.col_count += 1
	#Create new label
	label_cnt = len(self.top_labels)
	label_row = self.top_labels[label_cnt-1].grid_info()['row']
	label_col = self.top_labels[label_cnt-1].grid_info()['column'] + 1
	label_txt = self.top_labels[label_cnt-1]['text']
	self.top_labels.append(Label(self, text = chr(ord(label_txt)+1), font = "Arial 12"))
	self.top_labels[label_cnt].grid( row = label_row, column = label_col)
	#Regrid button
	btn_row = self.add_buttons[0].grid_info()['row']#replace static index to iterable index
	btn_col = self.add_buttons[0].grid_info()['column']#replace static index to iterable index
	self.add_buttons[0].grid(row = btn_row, column = btn_col+1)


#Adding row
def command_add_row(self):
	#Create new label
	label_cnt = len(self.left_labels)
	label_row = self.left_labels[label_cnt-1].grid_info()['row'] + 1
	label_col = self.left_labels[label_cnt-1].grid_info()['column']
	label_txt = self.left_labels[label_cnt-1]['text']
	self.left_labels.append(Label(self, text = chr(ord(label_txt)+1), font = "Arial 12"))
	self.left_labels[label_cnt].grid( row = label_row, column = label_col)
	#Regrid button
	btn_row = self.add_buttons[1].grid_info()['row']#replace static index to iterable index
	btn_col = self.add_buttons[1].grid_info()['column']#replace static index to iterable index
	self.add_buttons[1].grid(row = btn_row + 1, column = btn_col)
	#Create entries
	#rows = [[meshes][meshes]]
	# row 1 meshseh = row[0] and etc.
	for i in range(0, self.row_count):
			mesh_cnt = len(self.mesh_entries)
			mesh_row = self.mesh_entries[i][mesh_cnt-1].grid_info()['row'] + 1
			mesh_col = self.mesh_entries[i][mesh_cnt-1].grid_info()['column']
			self.mesh_entries.append(Entry(self))
			self.mesh_entries[mesh_cnt].grid( row = mesh_row, column = mesh_col)
			self.col_count += 1
	

'''
Table::option example 
'addin'  - Allow adding new columns and rows
'addout' - Deny adding new columns and rows	
'''	
#TODO:
#Endure class Table to another module
class Table(Frame):
	def __init__(self, parent, row_count = 1, col_count = 1, options = None, matrix = None):
		Frame.__init__(self, parent)
		self.parent = parent
		#List of labels
		self.top_labels = []
		self.left_labels = []
		#List of entries
		self.mesh_entries = [[]]
		#List of buttons
		self.add_buttons = []
		self.init_markup()
		#Table param: row counter, column counter
		self.row_count = row_count
		self.col_count = col_count
		#Table param: options, matrix
		self.options = options
		self.matrix = matrix#?
		
	def init_markup(self):
		self.parent.title("Table")
		self.pack(fill = BOTH, expand = True)
		
		#set columns
		self.columnconfigure(1)#, weight = 1)
		self.columnconfigure(2)#, weight = 1)
		#est rows
		self.rowconfigure(1)#, weight = 1)
		self.rowconfigure(2)#, weight = 1)
		#set labels
		self.left_labels.append(Label(self, text = "1", font = "Arial 12")) 
		self.left_labels[0].grid(row = 2, column = 1)
		self.top_labels.append(Label(self, text = "A", font = "Arial 12"))
		self.top_labels[0].grid(row = 1, column = 2)
		#set entries
		self.mesh_entries[0].append(Entry(self))
		self.mesh_entries[0][0].grid(row = 2, column = 2)
		#self.mesh_entries.append([Entry(self)])
		#self.mesh_entries[0][0].grid(row = 2, column = 2)
		#set buttons
		self.add_buttons.append(Button(self, text = "+", command = lambda: command_add_col(self)))
		self.add_buttons[0].grid(row = 2, column = 3)
		self.add_buttons.append(Button(self, text = "+", command = lambda: command_add_row(self)))
		self.add_buttons[1].grid(row = 3, column = 2)
		
class Window(Frame):
	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		Table(self.parent)
				
		


if __name__ == "__main__":
	root = Tk()
	root.geometry("480x300+300+300")
	master = Window(root)
	root.mainloop()
