import numpy as np
import time
import os


start = time.time()

#create subdirectory to house solutions
if not os.path.exists('solutions'):
    os.makedirs('solutions')

#read in sodukus from textfile
def read_euluer_sodukus(filepath):

    def reader(filepath):
        f = open(filepath, 'r')
        raw_file = f.read()

        file_split = raw_file.split('\n')
        return file_split

    def string_parse(x):
        string = ''
        for char in x:
            string += char + ','
        return string[:-1]

    file = reader(filepath)

    sodukus = []
    for i in range(0, len(file) + 1, 10):
        sodukus.append(file[i : i + 10])

    #chop off last empty list
    sodukus = sodukus[:-1]

    #chop off first entry of every list; corresponds to Grid1,...,Grid50
    numbers_of_sodukus = len(sodukus)
    for i in range(0, numbers_of_sodukus, 1):
        sodukus[i] = sodukus[i][1:]

    numpy_friendly_soduku = []

    #process sublists in sodukus into numpy friendly lists, list of strings -> list of ints
    for soduku in sodukus:
        soduku_lines = []
        for line in soduku:

            line_as_string = string_parse(line)
            line_as_nums = [int(x) for x in line_as_string.split(',')]

            soduku_lines.append(line_as_nums)
        numpy_friendly_soduku.append(soduku_lines)
    return numpy_friendly_soduku

#return x,y coordinates of ith soduku node
def placement(x):
    row = (x + 9)/9 - 1
    col = x % 9
    return [row,col]

#returns child node based off of available soduku moves available; these are not necessarily "legal"
#because they dont take into account how times tail element is used already
def create_next_node(soduku_cells_filled):
    pos = placement(soduku_cells_filled)

    #handle special case of fixed soduku entry
    if fixed_map[pos[0],pos[1]] <> 0:
        return [fixed_map[pos[0],pos[1]]]

    #get numbers already present in column,row,block associated with soduku node
    col = variable_map[:, pos[1]]
    row = variable_map[pos[0], :]

    block_row = pos[0] / 3
    block_column = pos[1] / 3

    block = variable_map[block_row * 3 : block_row * 3 + 3, block_column * 3 : block_column * 3 + 3]
    return list(numbers - set(list(np.unique(col)) + list(np.unique(row)) + list(np.unique(block))))

#returns boolean based off of whether or not tail element in child node is a legal move based off of how many times
#tail element appears in soduku puzzle
def is_legal(soduku_node):
    if len(soduku_node) == 0:
        return False
    elif(soduku_entrys_left[soduku_node[-1]] >= 0):
        return True
    else:
        return False

#read in sodukus
soduku_puzzles = read_euluer_sodukus('soduku_puzzles.txt')

#keep count of puzzle number for solution outputs
puzzle_number = 1

for soduku_puzzle in soduku_puzzles:


    numbers = set([1,2,3,4,5,6,7,8,9])

    #fixed map keeps account of original soduku entries given, variable map is nonstatic and keeps track of
    #current state of soduku puzzle
    fixed_map = np.array(soduku_puzzle)
    variable_map = np.zeros((9,9)) + fixed_map

    #keeps account of how many times in puzzle any element is used.
    soduku_entrys_left = {1:9, 2:9, 3:9, 4:9, 5:9, 6:9, 7:9, 8:9, 9:9}

    #initialize array corresponding to soduku tree
    soduku_nodes = []

    #Subtract entries present from tally of how many times said entries have been used in soduku
    for i in range(0, 9):
        for j in range(0,9):
            if fixed_map[i,j] != 0:
                soduku_entrys_left[int(fixed_map[i,j])] += -1

    #initialize first soduku entry
    soduku_nodes.append(create_next_node(0))
    soduku_cells_filled = 0

    #start solving soduku in iterative python friendly way
    while soduku_cells_filled < 81:

        #BREAK IF SOLVED SOLVED.
        #HANDLES SPECIAL CASE OF FILLING IN LAST SODUKU ENTRY
        #ANNOYING BUT IT WORKS
        if soduku_cells_filled == 80:
            for key, value in soduku_entrys_left.items():
                if value > 0:

                    variable_map[8,8] = key
            break

        if is_legal(soduku_nodes[soduku_cells_filled]):

            #if tail element in ith soduku node is legal from tally perspective, we place tail element in x,y coordinates
            #corresponding to ith soduku node
                pos = placement(soduku_cells_filled)

                variable_map[pos[0], pos[1]] = soduku_nodes[soduku_cells_filled][-1]

            #make sure you dont substract fixed entries from tallies as we've already done that
                if fixed_map[pos[0], pos[1]] == 0:
                    soduku_entrys_left[soduku_nodes[soduku_cells_filled][-1]] += -1

            #increment soduku cells filled and create new node based off current variable_map
                soduku_cells_filled += 1

                x = create_next_node(soduku_cells_filled)
                soduku_nodes.append(x)

        elif ~is_legal(soduku_nodes[soduku_cells_filled]):
            #if tail element of ith node is illegal from tally persepctive, remove tail element from ith
            soduku_nodes[soduku_cells_filled] = soduku_nodes[soduku_cells_filled][:-1]

            #if removing tail element creates empty node, remove empty node from soduku node tree and
            #and remove tail element of parent. Use while statement to handle case where removing tail element
            #from parent node causes parent node to become empty
            while len(soduku_nodes[-1]) == 0:
                #back track nodes if child node is empty
                soduku_nodes = soduku_nodes[:-1]
                soduku_cells_filled += -1

                #get coordinates of placement
                pos = placement(soduku_cells_filled)

                if fixed_map[pos[0], pos[1]] == 0:

                    variable_map[pos[0], pos[1]] = 0
                    soduku_entrys_left[soduku_nodes[soduku_cells_filled][-1]] += 1


                soduku_nodes[-1] = soduku_nodes[-1][:-1]
    np.savetxt('solutions/Grid{}_solution.txt'.format(puzzle_number),variable_map.astype(int), fmt='%i', delimiter=",")
    puzzle_number += 1
print (time.time() - start)
