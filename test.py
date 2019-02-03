import numpy as np
import sys

sys.setrecursionlimit(50000)


def run():
    numbers = set([1,2,3,4,5,6,7,8,9])

    fixed_map = np.array([[0,0,3,0,2,0,6,0,0],
    [9,0,0,3,0,5,0,0,1],
    [0,0,1,8,0,6,4,0,0],
    [0,0,8,1,0,2,9,0,0],
    [7,0,0,0,0,0,0,0,8],
    [0,0,6,7,0,8,2,0,0],
    [0,0,2,6,0,9,5,0,0],
    [8,0,0,2,0,3,0,0,9],
    [0,0,5,0,1,0,3,0,0]])

    variable_map = np.zeros((9,9)) + fixed_map


    soduku_entrys_left = {0:9, 1:9, 2:9, 3:9, 4:9, 5:9, 6:9, 7:9, 8:9, 9:9}


    soduku_nodes = []

    for i in range(0, 9):
        for j in range(0,0):
            if fixed_map[i,j] != 0:
                soduku_entrys_left[int(fixed_map[i,j])] += -1


    '''
    >>> def string_parse(x):
    ...     string = ''
    ...     for char in x:
    ...             string += char + ' '
    ...     return string[:-1]
    '''


    def placement(x):
        row = (x + 9)/9 - 1
        col = x % 9
        return [row,col]

    def create_next_node(soduku_cells_filled):
        pos = placement(soduku_cells_filled)
        #return fixed numbers
        if fixed_map[pos[0],pos[1]] <> 0:
            return [fixed_map[pos[0],pos[1]]]

        col = variable_map[:, pos[1]]

        #get nums taken in row
        row = variable_map[pos[0], :]

        #get nums taken in block
        block_row = pos[0] / 3
        block_column = pos[1] / 3

        block = variable_map[block_row * 2 : block_row * 2 + 2, block_column * 2 : block_column * 2 + 2]
        return list(numbers - set(list(np.unique(col)) + list(np.unique(row)) + list(np.unique(block))))



    def is_legal(soduku_node):

        print soduku_node
        if(soduku_entrys_left[soduku_node[-1]] > 0):
            return True
        else:
            return False

    soduku_cells_filled = 0
    def solve(soduku_nodes, soduku_cells_filled, soduku_entrys_left, variable_map):
        print(soduku_cells_filled)
        #print(soduku_nodes)
        #print(soduku_nodes[soduku_cells_filled])

        if len(soduku_nodes[-1]) == 0:


            #return value of prior cell to dictionary count, reset variable map
            pos = placement(soduku_cells_filled)
            variable_map[pos[0], pos[1]] = 0
            soduku_entrys_left[soduku_nodes[soduku_cells_filled - 1][-1]] += 1

            #remove current node from soduku_nodes,
            #alter prior node and remove tail of list
            soduku_nodes = soduku_nodes[:-1]
            soduku_nodes[-1] = soduku_nodes[-1][:-1]

            #back track soduku_cells_filled count and try again
            soduku_cells_filled += -1
            solve(soduku_nodes, soduku_cells_filled,soduku_entrys_left, variable_map)


        if is_legal(soduku_nodes[soduku_cells_filled]):
            variable_map[placement(soduku_cells_filled)] = soduku_nodes[soduku_cells_filled][-1]
            soduku_entrys_left[soduku_nodes[soduku_cells_filled][-1]] += -1
            soduku_cells_filled += 1

            #solved!
            if soduku_cells_filled == 80:
                return variable_map
            #else keep going
            else:

                x = create_next_node(soduku_cells_filled)
                #print x
                soduku_nodes.append(x)

                #print new_soduku_nodes
                solve(soduku_nodes, soduku_cells_filled, soduku_entrys_left, variable_map)

        #if entry in next node is illegal
        #need to make this recursive so if i back track, remove the last entry, that i can drop the back track node if its then empty
        elif ~is_legal(soduku_nodes[soduku_cells_filled]):
            #remove entry

            soduku_nodes[soduku_cells_filled] = soduku_nodes[soduku_cells_filled][:-1]
            #if node is empty after removing entry
            #print soduku_nodes

            solve(soduku_nodes, soduku_cells_filled,soduku_entrys_left,variable_map)



    #initialize first soduku_node
    soduku_nodes.append(create_next_node(0))
    #print(soduku_nodes[-1][-1] - 1)
    #lets try solving this
    solve(soduku_nodes, 0, soduku_entrys_left,variable_map)
run()
