# -*- coding: utf-8 -*-
"""
Created on Sat Sep 13 16:30:30 2025

@author: msimp
#OrderedDict?  List of Dicts?, Linked Lists?
#Linked List, must traverse to retrieve
"""

#%%
import numpy as np
from collections import OrderedDict
from collections import defaultdict
from scipy.special import perm
import copy

from icecream import ic

#%%
'''
a letter stack must have the following capabilities:
hold letters
hold "downstairskeh" letter
hold stack number
have topmost key-value element identifiable
have topmost key-value element removable
accept new topmost key-value element
'''
#%%

# state1 = ["A","B", "C", "D"]
# goal_state = ["D", "C", "B", "A"]
# #[(stack_no, dict_ltr_lower_neighbors), . . . all stacks]

# #for joint traversals involving named element in list, both lists must be coterminous
# state1b = ["Table"] + state1[0:-1]
# goal_stateb = ["Table"] + goal_state[0:-1]

# dict1 = OrderedDict()
# dict2 = OrderedDict()
# dict1["A"] = "Table"
# dict1["B"] = "A"
# dict1["C"] = "B"
# dict1["D"] = "C"
# print(dict1)

# for i, ltr in enumerate(state1):
#     dict1[ltr] = state1b[i]
    
# print(dict1)

# print(dict2)    
# for i, ltr in enumerate(goal_state):
#     dict2[ltr] = goal_stateb[i]
# print(dict2)    

#a list of tuples is ordered_dict ready
#OrderedDict([(A,1),(B,2), (C,3),. . .(k,n)])

# how to use starmap, https://www.geeksforgeeks.org/python/python-convert-two-lists-into-a-dictionary/

# dict1 = OrderedDict(zip(state1, state1b))

# stack0_loc = dict(zip(state1, [0]*len(state1)))
# stack_locs = [stack0_loc, {}]
# test1 = OrderedDict(zip(state1, state1b))
# test1 == dict1
# test1["A"] == dict1["A"]


# dict2 = OrderedDict(zip(goal_state, goal_stateb))    
# dict1["A"] == dict2["A"]

#set of keys 1 intersect keys 2
#retrieve k,v for intersection
#compare values

#DEEPCOPY old state to save to history

#can you peek at an ordered dict?

#https://realpython.com/python-ordereddict/#choosing-between-ordereddict-and-dict

#ordered dicts can be merged   
 # ordered_dict3 = ordered_dict1 | ordered_dict2, unique entries only
 #like SAS merge ops, values on the elft get overwritten by values on the right for common keys

#delta scoring, where keys match in goal and state combo ordered dicts, do the values match   

#https://www.google.com/search?q=is+there+a+way+to+%22peek%22+at+the+final+item+in+a+python+ordered+dictionary&sca_esv=395b2b4c3d4fa45a&sxsrf=AE3TifNPpxl72-oxGfHUmCPNCyj0ynNg7A%3A1757808848324&ei=0AjGaPq8E6re5NoPobTPkQQ&ved=0ahUKEwj65PKf_NaPAxUqL1kFHSHaM0IQ4dUDCBE&uact=5&oq=is+there+a+way+to+%22peek%22+at+the+final+item+in+a+python+ordered+dictionary&gs_lp=Egxnd3Mtd2l6LXNlcnAiSWlzIHRoZXJlIGEgd2F5IHRvICJwZWVrIiBhdCB0aGUgZmluYWwgaXRlbSBpbiBhIHB5dGhvbiBvcmRlcmVkIGRpY3Rpb25hcnlIyWZQAFjCZHACeAGQAQOYAf8CoAGsNaoBCTYyLjEyLjIuMbgBA8gBAPgBAZgCPqAChyvCAgQQIxgnwgILEAAYgAQYkQIYigXCAgsQABiABBixAxiDAcICCBAAGIAEGLEDwgIKEAAYgAQYQxiKBcICDhAAGIAEGLEDGIMBGIoFwgIEEAAYA8ICBRAAGIAEwgIOEC4YgAQYsQMYgwEYigXCAgYQABgWGB7CAgsQABiABBiGAxiKBcICBRAAGO8FwgIIEAAYgAQYogTCAgUQIRigAcICBRAhGKsCwgIFECEYnwXCAggQABiiBBiJBcICBxAhGKABGAqYAwCSBwc0Ni4xNS4xoAfhsAOyBwc0NC4xNS4xuAf6KsIHCTAuMTIuNDcuM8gHmAI&sclient=gws-wiz-serp
#google search ai aided, no code consulted

#https://stackoverflow.com/questions/16125229/last-key-in-python-dictionary
#how to peek at last key,value pair in ordered dict
# top_key = list(dict1.keys())[-1]
#to move,  retrieve key of top entry:
# change value to that of its new lower neighbor
# dict1[top_key] = 'Table'
# dict1
#getitem() from dict1 
#add item to new stack
#make last key,value pair in new loc equal to extracted entry
#change stack loc

#for each possible next state:
#deep copy current state and loc, store in node
#for each state and loc:
#proceeding from stack to stack:
# in each stack, get top item, move to next valid position, do not forget table if no new stack has been started
#for now work with only 1 new stack

#%%
#https://medium.com/@teamcode20233/converting-a-list-to-a-tuple-in-python-is-a-common-operation-that-is-frequently-used-in-data-61593ad2e182
#converting lists to tuples.  happens anyway on the ordered dict

input_state = [["A", "B", "C"], ["D", "E"]]
#input_state = [["A"], ["D", "E", "B"], ["C"]]
#input_state = [["A", "C"], ["D", "E", "B"]]
goal_state = [["A", "C"], ["D", "E", "B"]]

def make_letter_stack(letter_list):
    letter_listb = copy.deepcopy(letter_list)
    letter_listc = ["Table"] + letter_listb[0:-1]
    return OrderedDict(zip(letter_listb, letter_listc))

def initialize_round(input_state_list, goal_state_list):
    input_state = copy.deepcopy(input_state_list)
    goal_state = copy.deepcopy(goal_state_list)
    #? why 9?
    input_stacks = [9]*len(input_state)
    goal_stacks = [9]*len(goal_state)


    for i in range(len(input_stacks)):
        input_stacks[i] = make_letter_stack(input_state[i])
    
    for i in range(len(goal_stacks)):
        goal_stacks[i] = make_letter_stack(goal_state[i])    
        
    return input_stacks, goal_stacks

#variable inspector in spyder is sorting dict by key
input_stacks1b, goal_stacks1b = initialize_round(input_state, goal_state)
#print(input_stacks1b)
#print(goal_stacks1b)

#%%
#https://www.askpython.com/python/dictionary/compare-two-dictionaries
#list comp to cf ttwo dicts 
#all keys in common
#need n unequal value
# input_super_dict = OrderedDict()
# for odict in input_stacks1b:
#     input_super_dict = input_super_dict | odict
    
# goal_super_dict = OrderedDict()    
# for odict in goal_stacks1b:
#     goal_super_dict = goal_super_dict | odict

# key_list = input_super_dict.keys()
# delta_score = 0
# for key in key_list:
#     if input_super_dict[key] != goal_super_dict[key]:
#         delta_score += 1
# print(delta_score)

#%%
#list of input stacks are for a single state, single possible move
def get_delta_score(input_stacks, goal_stacks):

    input_stacks = copy.deepcopy(input_stacks)
    goal_stacks = copy.deepcopy(goal_stacks)
    
    super_input_stacks = OrderedDict()
    for odict in input_stacks:
        super_input_stacks = super_input_stacks | odict
        
    super_goal_stacks = OrderedDict()
    for odict in goal_stacks:
        super_goal_stacks = super_goal_stacks | odict
        
    key_list = super_input_stacks.keys()
    delta_score = 0
    for key in key_list:
        if super_input_stacks[key] != super_goal_stacks[key]:
            delta_score += 1
            
    return delta_score
    
get_delta_score(input_stacks1b, goal_stacks1b)

#%%
#stack correct so far
def correct_so_far(input_stack, goal_stacks, move_number):
        
    super_goal_stacks = OrderedDict()
    for odict in goal_stacks:
        super_goal_stacks = super_goal_stacks | odict
        
    if move_number == 0:
        key_list = list(input_stack.keys())[0:-1]
    else:
       key_list = list(input_stack.keys())
    
    for key in key_list:
        if input_stack[key] != super_goal_stacks[key]:
            return False
    return True
            

    

#%%
#check subgoals, subcosts?
def subgoal_met(input_stack, goal_stack):
    if input_stack == goal_stack:
        return True
    else:
        return False
    
subgoal_met(input_stacks1b[1], goal_stacks1b[1])

# %%
# for input_stack in input_stacks1b:
#     print(correct_so_far(input_stack, goal_stacks1b))

#%%
def goal_met(input_stacks, goal_stacks):
    if input_stacks == goal_stacks:
        return True
    else:
        return False
    
goal_met(input_stacks1b, goal_stacks1b)    
    
#%%
#borrow top of input
#https://stackoverflow.com/questions/9917178/how-to-get-last-element-from-ordereddict-without-removing-it
last_keys_list = []
position_list = []

# for i,input_stack in enumerate(input_stacks1b):
#     last_keys_list.append(list(input_stack.keys())[-1])
#     position_list.append(i)
    

# #hard to keep straight which move comes from which stacks
# possible_moves = permutations(last_keys_list, 2)
# position_crosswalk = permutations(position_list,2)

# for i, move in enumerate(possible_moves):
#     print(move)
    
# for position in position_crosswalk:
#     print(position)

# pesky1 = OrderedDict()
# pesky1[last_key] = item[last_key]
# print(pesky1)
#%%

#generates possible moves, skips pulling from stacks that are 'correct so far', 
#skips putting on stacks not completely correct
#double nested loops ar O(nsq) time complexity, so if you had 26 stacks, this 
#manoever would examine 650 moves, not excluding ienti
move_number = 0
def get_and_vet_possible_moves(input_stacks, goal_stacks, move_number):
    possible_moves = []
    position_crosswalk = []
    addon_odict = OrderedDict({"Table":99})
    input_stacks = copy.deepcopy(input_stacks)
    goal_stacks = copy.deepcopy(goal_stacks)
    
    if move_number == 0:
        input_stacks.append(addon_odict)
            
    for i, input_stack in enumerate(input_stacks):
        dont_put_on = 99
        dont_pull_from = 99
        if correct_so_far(input_stack, goal_stacks, move_number):
            dont_pull_from = i
        else:
            dont_put_on = i
        for j, input_stack in enumerate(input_stacks):
            if (i != j) and (i != dont_pull_from) and (j != dont_put_on):
                #print(i,j)
                #print(list(input_stacks[i].keys())[-1], list(input_stacks[j].keys())[-1])
                possible_moves.append((list(input_stacks[i].keys())[-1], list(input_stacks[j].keys())[-1]))
                position_crosswalk.append((i,j))
    return possible_moves, position_crosswalk

possible_moves, position_crosswalk = get_and_vet_possible_moves(input_stacks1b, goal_stacks1b, move_number)

#%%
#make scored nodes for all possible moves that survived pruning
#input is: possible_moves, position_crosswalk, input_stacks.deepcopy()
#calc delta scores

#position_crosswalk_tuple
#input_stacks, goal_stacks,

def make_a_move(source_stack, target_stack, move):
    #you need to mutate the lists here
    #returns a tuple instead of correct kv pair
    item_to_move = source_stack.popitem(last=True)
    new_value = list(target_stack.keys())[-1]
    target_stack[item_to_move[0]] = new_value

    return source_stack, target_stack

def make_stacks_for_move(input_stacks, goal_stacks, position_tuple, move):
    input_stacks = copy.deepcopy(input_stacks)
    goal_stacks = copy.deepcopy(goal_stacks)
    source_stack = input_stacks[position_tuple[0]]
    target_stack = input_stacks[position_tuple[1]]
    source_stack, target_stack = make_a_move(source_stack, target_stack, move)
    delta_score = get_delta_score(input_stacks, goal_stacks)
    return input_stacks, delta_score



make_stacks_for_move(input_stacks1b, goal_stacks1b, position_crosswalk[0], possible_moves[0])






    



