"""
#need to manually connect python to spyder kernel via kernel[9999].json
#run in terminal window:  python -m spyder-kernels.console
#
#To connect another client to this kernel, use:
#--existing kernel-32064.json
#geeks for geeks presentation of A-Star has less symbol switching
#will likely work fine with small problems.
"""
#%%
#this code allows a better astar implementation where ALL generated states on a move
# that are not in the visited list get added to the search queue and MOST IMPORTANTLY the total estimated path
#cost is calculated before enqing
#means-end, too greedy to see more than one move ahead, so need to get bona fided astar wroking
#need to eventually allow for subgoals
import numpy as np
from queue import *

import icecream as ic

#modfified astar ignores g, just runs oof of h


initial_arrangement_1 = [["A", "B", "C"], ["D", "E"]]
goal_arrangement_1 = [["A", "C"], ["D", "E", "B"]]


#initial_arrangement_0 = [["A", "C"], ["B"]]
#goal_arrangement_0 = [["C", "B", "A"]]
max_items = 26

#initialize game, single stack goal state
initial_arrangement = initial_arrangement_1
goal_arrangement = goal_arrangement_1

search_queue = PriorityQueue(maxsize=max_items)
visited_list = []
final_moves_list = []
final_states_list = []
# enqueue initial state
initial_cost = 3
initial_state = (initial_cost, initial_arrangement, ("Start", "Start"))



#%%
full_list_of_possible_moves = ((("C", "Table"),("C","E")), 
                               (("C", "B"), ("B","C"), ("B","E")),
                               (("C","B"),("C", "Table")),
                               (("A","C"), ("C", "A")))

full_list_of_possible_states = [
[[["A","B"], ["D","E"], ["C"]],
[["A","B"], ["D","E", "C"]]],
[[["A","B","C"], ["D","E"]], 
[["A"], ["D","E"], ["C","B"]],
[["A"], ["D","E","B"], ["C"]]],
[[["A","B","C"], ["D","E"]],
[["A","B"], ["D","E"], ["C"]]],
[[["A"], ["D","E","B","C"]],
[["A","C"], ["D","E","B"]]]
]
  
                                
full_list_of_costs = [[2,3,3], [2, 2,  1], [ 2, 2], [1, 0]]



#%%

#switch from list of lists to lists of ordered dicts, input_stacks
search_queue.put(initial_arrangement )

move_number = 0
goal_reached = False
while not search_queue.empty() and not goal_reached:
    current_state = search_queue.get()
    visited_list.append(current_state)
    #get and prune possible moves
    possible_moves = get_and_prune_possible_moves()
    
    min_cost = max_items
    print(move_number)
    #place holders for move gen and cost calc
    
    for i, move in enumerate(possible_moves):
        #make stacks for this move and calc delta
        new_state = []
        new_state.parent = current_state.id
        #calc cost of each move

        if new_state == goal_arrangement:
            final_moves_list.append(move)
            #final_states_list.append(state)
            goal_reached = True
            print( f"Goal Reached {possible_states[i]} at move {move}, {move_number + 1}")
            break
        #O(n) oepration, cant use a set with the lists of ordered dicts
        elif new_state in visited_list:
            #print(state)
            continue
        else:
            #calc_cost
            search_queue.put(new_state)
    #min_move is the last move, min_state is the pentultimate state
    qsize = search_queue.qsize()
    visted_list_len = len(visited_list)     
    move_number += 1


