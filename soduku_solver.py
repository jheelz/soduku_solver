import numpy as np

'''
class entry(row, col):

    self.row = row
    self.col = col

    self.legal_moves = soduku.
'''
#inspired by depth search algorithm
class soduku:

    #need to get available moves that satisfy rules; each number can be used 9 times
    #rules: number can 1) only appear once across 1x9 row, 2) once across 9x1 column, and 3) once in 3x3 section
    def __init__(self):

        #initialize matrix of zeroes and a matrix containing fixed values
        self.variable_map = np.zeros((9,9))
        self.fixed_map = np.array(file)

        #initialize dictionary containing how many times a soduku entry (1,2,...) is left
        self.soduku_entrys_left = {0:9, 1:9, 2:9, 3:9, 4:9, 5:9, 6:9, 7:9, 8:9, 9:9}

        #initialize tree nodes
        self.soduku_nodes = []




    def legal_numbers(self, cell):
        
