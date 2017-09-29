assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [r+c for r in A for c in B]



boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123','456','789')]
diag_units_left = [r+c for r,c in zip(rows, cols)]
diag_units_right = [r+c for r,c in zip(rows, cols[::-1])]
diag_units = [diag_units_left, diag_units_right]
unit_list = row_units + column_units + square_units


# get the peers list for each box
peers = {}
for box in boxes:
    peer_of_box_row_step1 = [rs for rs in row_units if box in rs][0]
    peer_of_box_col_step1 = [cs for cs in column_units if box in cs][0]
    peer_of_box_sqr_step1 = [sqrs for sqrs in square_units if box in sqrs][0]
    
    peer_of_box_row_step2 = [ii for ii in peer_of_box_row_step1 if ii != box]
    peer_of_box_col_step2 = [ii for ii in peer_of_box_col_step1 if ii != box]
    peer_of_box_sqr_step2 = [ii for ii in peer_of_box_sqr_step1 if ii != box]
    
    # if the box is on one of the diagonal line, find the peers on the diagonal line
    if box in diag_units[0] or box in diag_units[1]:
        peer_of_box_diag_step1 = [diags for diags in diag_units if box in diags][0]
        peer_of_box_diag_step2 = [ii for ii in peer_of_box_diag_step1 if ii != box]

        each_peers = peer_of_box_row_step2 + peer_of_box_col_step2 + peer_of_box_sqr_step2 + peer_of_box_diag_step2
    else:
        each_peers = peer_of_box_row_step2 + peer_of_box_col_step2 + peer_of_box_sqr_step2
    peers[box] = each_peers




def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values



def naked_twins(values):
    # get the boxs who have two values in it
    seed_box = [box for box in values.keys() if len(values[box]) == 2]
    # for each one of the seed_box
    for each_seed_box in seed_box:
        # get the value in that box
        seed_element = set(values[each_seed_box])
        # get the peers of this box
        peers_of_each_seed = peers[each_seed_box]
        # for each one of the peers of this box
        for each_peer in peers_of_each_seed:
            # get the values in this peer
            each_peer_element = set(values[each_peer])
            # if the value of this peer is same as the seed box
            if each_peer_element == seed_element:
                # then they are twins
                twins = (each_seed_box, each_peer)
                # get the peers of the seed box
                peers_seed = set(peers[each_seed_box])
                # get the peers of the twin brother
                peers_twin_bro = set(peers[each_peer])
                # get the common peers of them
                common_peers = peers_seed & peers_twin_bro
                # for each one of the peers of the common peers 
                for each_common_peer in common_peers:
                    # if the their peer has more than two values
                    if len(values[each_common_peer]) >= 2:
                        # remove the value from the peer 
                        for remove_val in seed_element:
                            values = assign_value(values, each_common_peer, values[each_common_peer].replace(remove_val, ''))
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [r+c for r in A for c in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    complete_grid = dict(zip(boxes, grid))
    for key in complete_grid.keys():
        if complete_grid[key] == '.':
            complete_grid[key] = '123456789'
        
    return complete_grid

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print 
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unit_list:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # display(values)
        
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Naked Twins Strategy
        values = naked_twins(values)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            # display(values)
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    # values = {"G7": "2345678", "G6": "1236789", "G5": "23456789", "G4": "345678", "G3": "1234569", "G2": "12345678", "G1": "23456789", "G9": "24578", "G8": "345678", "C9": "124578", "C8": "3456789", "C3": "1234569", "C2": "1234568", "C1": "2345689", "C7": "2345678", "C6": "236789", "C5": "23456789", "C4": "345678", "E5": "678", "E4": "2", "F1": "1", "F2": "24", "F3": "24", "F4": "9", "F5": "37", "F6": "37", "F7": "58", "F8": "58", "F9": "6", "B4": "345678", "B5": "23456789", "B6": "236789", "B7": "2345678", "B1": "2345689", "B2": "1234568", "B3": "1234569", "B8": "3456789", "B9": "124578", "I9": "9", "I8": "345678", "I1": "2345678", "I3": "23456", "I2": "2345678", "I5": "2345678", "I4": "345678", "I7": "1", "I6": "23678", "A1": "2345689", "A3": "7", "A2": "234568", "E9": "3", "A4": "34568", "A7": "234568", "A6": "23689", "A9": "2458", "A8": "345689", "E7": "9", "E6": "4", "E1": "567", "E3": "56", "E2": "567", "E8": "1", "A5": "1", "H8": "345678", "H9": "24578", "H2": "12345678", "H3": "1234569", "H1": "23456789", "H6": "1236789", "H7": "2345678", "H4": "345678", "H5": "23456789", "D8": "2", "D9": "47", "D6": "5", "D7": "47", "D4": "1", "D5": "36", "D2": "9", "D3": "8", "D1": "36"}
    values_solved = search(values)

    return values_solved

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    # diag_sudoku_grid = ''
    display(solve(diag_sudoku_grid))
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
