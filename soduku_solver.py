import numpy as np


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

    block = variable_map[block_row * 3 : block_row * 3 + 3, block_column * 3 : block_column * 3 + 3]
    return list(numbers - set(list(np.unique(col)) + list(np.unique(row)) + list(np.unique(block))))

def is_legal(soduku_node):
    if len(soduku_node) == 0:
        return False
    elif(soduku_entrys_left[soduku_node[-1]] >= 0):
        return True
    else:
        return False

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

soduku_entrys_left = {1:9, 2:9, 3:9, 4:9, 5:9, 6:9, 7:9, 8:9, 9:9}


soduku_nodes = []

for i in range(0, 9):
    for j in range(0,9):
        if fixed_map[i,j] != 0:
            soduku_entrys_left[int(fixed_map[i,j])] += -1

print soduku_entrys_left
soduku_nodes.append(create_next_node(0))
soduku_cells_filled = 0


while soduku_cells_filled < 81:

    #FIX BUG THAT DOESNT LET [8,8] GET POPULATED
    #ANNOYING BUT IT WORKS
    if soduku_cells_filled == 80:
        for key, value in soduku_entrys_left.items():
            if value > 0:

                variable_map[8,8] = key
        print variable_map
        break

    if is_legal(soduku_nodes[soduku_cells_filled]):
            pos = placement(soduku_cells_filled)

            variable_map[pos[0], pos[1]] = soduku_nodes[soduku_cells_filled][-1]

            #print variable_map
            if fixed_map[pos[0], pos[1]] == 0:
                soduku_entrys_left[soduku_nodes[soduku_cells_filled][-1]] += -1

            soduku_cells_filled += 1

            x = create_next_node(soduku_cells_filled)
            soduku_nodes.append(x)

    elif ~is_legal(soduku_nodes[soduku_cells_filled]):
        #remove entry
        soduku_nodes[soduku_cells_filled] = soduku_nodes[soduku_cells_filled][:-1]

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
