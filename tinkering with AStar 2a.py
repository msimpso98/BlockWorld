"""
#need to manually connect python to spyder kernel via kernel[9999].json
#run in terminal window:  python -m spyder-kernels.console
#
#To connect another client to this kernel, use:
#--existing kernel-32064.json
#geeks for geeks presentation of A-Star has less symbol switching
"""
#%%
#this code allows a better astar implementation where ALL generated states on a move
# that are not in the visited list get added to the search queue and MOST IMPORTANTLY the total estimated path
#cost is calculated before enqing
#means-end, too greedy to see more than one move ahead, so need to get bona fided astar wroking
#need to eventually allow for subgoals
import numpy as np
from queue import *

#modfified astar ignores g, just runs oof of h

#initial_arrangement_1 = [["A", "B", "C"], ["D", "E"]]
#goal_arrangement_1 = [["A", "C"], ["D", "E", "B"]]
initial_arrangement_0 = [["A", "C"], ["B"]]
goal_arrangement_0 = [["C", "B", "A"]]
max_items = 26

#initialize game, single stack goal state
search_queue = PriorityQueue(maxsize=max_items)
visited_list = []
final_moves_list = []
final_states_list = []
# enqueue initial state
initial_state = (3, initial_arrangement_0, ("Start", "Start"))



#%%
full_list_of_possible_moves = ((("C", "Table"), ("C", "B"), ("B","C")),
                               (("A","B"), ("A","C"), ("B","A"), ("B","C"), ("C","A"), ("C","B")),
                               (("B","A"), ("A","B")))

full_list_of_possible_states = [ 
    [[["A", "B", "C"]], [["A"], ["B","C"]],[["A","C", "B"], ["B"]] ],
                                [[["B","A"],["C"]], [["B"],["C","A"]],[["A","B"],["C"]],
                                [["A"],["C","B"]],[["A","C"],["B"]], [["A"],["B","C"]]],
                                [[["A","B"], ["C"]],[["C","B","A"]]]
                                ]
full_list_of_costs = [[2,3,3], [2, 2, 2, 1, 3, 3], [1, 0]]

#%%
full_list_of_possible_moves[0]

#%%


search_queue.put(initial_arrangement_0 )

move_number = 0
goal_reached = False
while not search_queue.empty() and not goal_reached:
    current_state = search_queue.get()
    
    #placeholder for entire games possible moves and possible states
    possible_moves = full_list_of_possible_moves[move_number]
    possible_states = full_list_of_possible_states[move_number]
    #is this where I put the parent node into the visited list?
    visited_list.append(current_state)
    move_costs = full_list_of_costs[move_number]
    min_cost = max_items
    print(move_number)
    #place holders for move gen and cost calc
    possible_moves = full_list_of_possible_moves[move_number]
    possible_states = full_list_of_possible_states[move_number]

    #likely collapse goal and input states into respective merged ordered dicts
    for i, state in enumerate(possible_states):
        #calc cost of each move
        move = possible_moves[i]
        #print(move)
        #print(move)
        if state == goal_arrangement_0:
            #print(move_number, state, move)
            #THIS is the final state to append to your final path
            #ALSO the final move to append to your list of moves
            final_moves_list.append(move)
            final_states_list.append(state)
            goal_reached = True
            print( f"Goal Reached {possible_states[i]} at move {move}, {move_number + 1}")
            break
        elif state in visited_list:
            #print(state)
            continue
        else:
            #calc_cost
            search_queue.put(state)
    #min_move is the last move, min_state is the pentultimate state
    qsize = search_queue.qsize()
    visted_list_len = len(visited_list)     
    move_number += 1




# f, lists
