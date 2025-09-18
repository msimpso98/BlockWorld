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

#switch from state to block stacks when adapting this for project
search_queue.put(initial_arrangement )

move_number = 0
goal_reached = False
while not search_queue.empty() and not goal_reached:
    current_state = search_queue.get()
    #generate possible moves for current state
    possible_moves = (())
    possible_states = (())
    #placeholder for entire games possible moves and possible states
    #possible_moves = full_list_of_possible_moves[move_number]
    #possible_states = full_list_of_possible_states[move_number]
    #is this where I put the parent node into the visited list?
    visited_list.append(current_state)
    move_costs = calc_costs(possible_moves)
    min_cost = max_items
    print(move_number)
    #place holders for move gen and cost calc
    

    #moving stack by stack is likely to be more successful than merging the dicts
    #Jiahuan Ye on forum recommends we NEVER put a block onto a stack that has any errors in it.
    #this would be stack_dict(k,v) == goal_stack_dict(k,v    )
    #don't move a block that's on the table to the table
    #if no reduction, go to subgoals?
    #MAS, you can calculate the past cost up through each child nod, f(p) + delta,
    #discard all not at the minimum
    for i, state in enumerate(possible_states):
        #calc cost of each move
        move = possible_moves[i]
        #print(move)
        #print(move)
        if state == goal_arrangement:
            #print(move_number, state, move)
            #THIS is the final state to append to your final path
            #ALSO the final move to append to your list of moves
            final_moves_list.append(move)
            final_states_list.append(state)
            goal_reached = True
            print( f"Goal Reached {possible_states[i]} at move {move}, {move_number + 1}")
            break
        #if needing to save memory, make visited_list into a set
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
