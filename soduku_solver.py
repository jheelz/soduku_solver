import numpy as np

'''
class entry(row, col):

    self.row = row
    self.col = col

    self.legal_moves = soduku.
'''
#inspired by depth search algorithm

def soduku_board(filename):

    fixed_map = np.read(filename)
    variable_map = np.zeros((9,9)) + fixed_map

    soduku_entrys_left = {0:9, 1:9, 2:9, 3:9, 4:9, 5:9, 6:9, 7:9, 8:9, 9:9}

    soduku_nodes = {}

    #helper function to get matrix position of integer (0 -> [0,0], 9 -> [1,0])
    def placement(x):
        row = (x + 9)/9 - 1
        col = x % 9
        return [row,col]

    def create_next_node(soduku_cells_filled):
        pos = placement(soduku_cells_filled)

        #return fixed numbers
        if fixed_map[pos] <> 0:
            return [fixed_map[pos]]

        col = variable_map[:, pos[1]]

        #get nums taken in row
        row = variable_map[pos[0], :]

        #get nums taken in block
        block_row = pos[0] / 3
        block_column = pos[1] / 3

        block = variable_map[block_row * 2 : block_row * 2 + 2, block_column * 2 : block_column * 2 + 2]

        soduku_nodes.append(list(set(list(np.unique(col)) + list(np.unique(row)) + list(np.unique(block)))))

    def is_legal(soduku_nodes):
        if (soduku_nodes[-1][-1] - 1) >= 0:
            return True
        else:
            return False


    def solve(soduku_nodes):

        if is_legal(soduku_nodes[soduku_cells_filled]):
            variable_map[node cell] = node[-1]
            soduku_entry_left[soduku_nodes[soduku_cells_filled][-1]] += -1
            soduku_cells_filled += 1

            #solved!
            if soduku_puzzle_size == 80:
                return variable_map
            #else keep going
            else:
                solve(create_next_node(soduku_nodes[soduku_cells_filled]))

        #if entry in next node is illegal
        if !is_legal(node):
            #remove entry

            node = node[:-1]
            #if node is empty after removing entry
            if len(node) == 0:


                #return value of prior cell to dictionary count, reset variable map
                variable_map[placement(soduku_cells_filled)] = 0
                soduku_entry_left[soduku_nodes[soduku_cells_filled - 1][-1]] += 1

                #remove current node from soduku_nodes,
                #alter prior node and remove tail of list
                soduku_nodes = soduku_nodes[:-1]
                soduku_nodes[-1] = soduku_nodes[:-1]

                #back track soduku_cells_filled count and try again
                soduku_cells_filled += -1
                solve(soduku_nodes)


            else:
                solve(soduku_nodes)

    soduku_cells_filled = 0

    #initialize first soduku_node
    first_node = create_next_node(0)

    #lets try solving this
    solve(first_node)

    
