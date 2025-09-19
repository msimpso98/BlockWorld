import numpy as np
from collections import OrderedDict, defaultdict
from queue import PriorityQueue
import copy
from memory_profiler import profile

#/begin code copied from https://docs.python.org/3/library/queue.html
#generic code for a wrapper to make the PriorityQueue() class not
#try to order entries in the list of ordered dictionaries
#MAS added getter methods to retrieve pieces needed for astar

from dataclasses import dataclass, field
from typing import Any
@dataclass(order=True)
class PrioritizedItem:
    priority: int
    item: Any=field(compare=False)
    
    def get_item(self):
        return self.item
    
    def get_priority(self):
        return self.priority
    
#/end borrowed code

#begin code, largely adapted from
#can also set memory limits to simulate gradescope limitations
#https://www.geeksforgeeks.org/python/python-how-to-put-limits-on-memory-and-cpu-usage/

#https://www.google.com/search?q=AttributeError%3A+module+%27signal%27+has+no+attribute+%27SIGALRM%27&oq=AttributeError%3A+module+%27signal%27+has+no+attribute+%27SIGALRM%27&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRg60gEJMTI4MmowajE1qAIMsAIB8QU_wN6yVmYupA&sourceid=chrome&ie=UTF-8
import threading
import time

def timeout_handler():
    print("Timeout occurred!")
    
# end borrowed code    
    

class Node():
   pass 
    
class BlockWorldAgent:
    #@profile
    def __init__(self):
        #If you want to do any initial processing, add it here.
        
        #agent is initialized ONCE for the entire main program, so you need to
        #reset between solve() runs
        self.MAX_ITEMS = 26
 
        
    #@profile
    def make_letter_stack(self, letter_list):
        letter_list = copy.deepcopy(letter_list)
        letter_listb = ["Table"] + letter_list[0:-1]
        return OrderedDict(zip(letter_list, letter_listb))
    
    #@profile
    def check_inputs(self, input_list, goal_list):
        if input_list != [] and goal_list != []:
            self.valid_inputs = True
        else:
            self.valid_inputs = False

    #@profile            
    def get_valid_inputs(self):
        return self.valid_inputs
    
    #@profile
    def get_final_moves_list(self):
        return self.final_moves_list
    
    #@profile
    def add_to_final_moves_list(self, move):
        self.final_moves_list.append(move)
            
    #@profile
    def initialize_round(self, input_list, goal_list):
        input_list = copy.deepcopy(input_list)
        goal_list = copy.deepcopy(goal_list)
        self.check_inputs(input_list, goal_list)
        if self.valid_inputs:
            #? why 9?
            self.input_stacks = [9]*len(input_list)
            self.goal_stacks = [9]*len(goal_list)
                
            for i in range(len(self.input_stacks)):
                self.input_stacks[i] = self.make_letter_stack(input_list[i])
            
            for i in range(len(self.goal_stacks)):
                self.goal_stacks[i] = self.make_letter_stack(goal_list[i])  
        else:
            print("one or both input matrices are empty. no game possible")


            
            
    #@profile
    def get_input_stacks(self):
        return self.input_stacks
    
    #@profile
    def get_goal_stacks(self):
        return self.goal_stacks
    
    #makes single ordered dict out of goal stacks, used for delta score calc
    #and goal checking
    #@profile
    def make_restacked_goal(self):
        goal_stacks = copy.deepcopy(self.goal_stacks)
        self.restacked_goal = OrderedDict()
        for odict in goal_stacks:
            self.restacked_goal = self.restacked_goal | odict
            
    
    #@profile
    def get_restacked_goal(self):
        return self.restacked_goal
                
    
    #@profile
    def set_goal_reached(self, value : bool):
        self.goal_reached = value
        
    #@profile
    def get_goal_reached(self):
        return self.goal_reached
    
    #@profile
    def add_to_visted_list(self, state):
        self.visited_list.append(state)
        
   
    #@profile 
    def goal_met(input_stacks, goal_stacks):
        if input_stacks == goal_stacks:
            return True
        else:
            return False      
        
    #@profile
    def subgoal_met(input_stack, goal_stack):
        if input_stack == goal_stack:
            return True
        else:
            return False        
        
        
    #@profile
    def correct_so_far(self, input_stack, move_number):
    
        key_list = list(input_stack.keys())
        
        for key in key_list:
           if key != "Table":
               if input_stack[key] != self.restacked_goal[key]:
                   return False
        return True
    
        
    #@profile
    def get_delta_score(self, stacks):
        stacks = copy.deepcopy(stacks)
        super_stacks = OrderedDict()
        for odict in stacks:
            super_stacks = super_stacks | odict
    		
        key_list = list(super_stacks.keys())
        
            
        delta_score = 0
        
        for key in key_list:
            if key != "Table":
                if super_stacks[key] != self.restacked_goal[key]:
                    delta_score += 1
        return delta_score
    
    
    #@profile
    def make_a_move(self, source_stack, target_stack, move):
        #you need to mutate the lists here
        #returns a tuple instead of correct kv pair
        item_to_move = source_stack.popitem(last=True)
        new_value = list(target_stack.keys())[-1]
        target_stack[item_to_move[0]] = new_value
    
        return source_stack, target_stack
    
    
   
    #@profile 
    def make_states_for_move(self, input_state, position_tuple, move):
        input_stacks = copy.deepcopy(input_state.get_item())
        source_stack = input_stacks[position_tuple[0]]
        target_stack = input_stacks[position_tuple[1]]
        source_stack, target_stack = self.make_a_move(source_stack, target_stack, move)
        delta_score = self.get_delta_score(input_stacks)
        return PrioritizedItem(delta_score, input_stacks)
    
    

    #@profile    
    def get_and_vet_possible_moves(self, current_state, move_number):
        current_stacks = current_state.get_item()
        possible_moves = []
        position_crosswalk = []
        addon_odict = OrderedDict({"Table":99})
        #current_state will need updating if move = 0
        #current_state = copy.deepcopy(current_state)

        
        if move_number == 0:
            current_stacks.append(addon_odict)
                
        for i, input_stack in enumerate(current_stacks):
            dont_put_on = 99
            dont_pull_from = 99
            if self.correct_so_far(input_stack, move_number):
                dont_pull_from = i
            else:
                dont_put_on = i
            for j, input_stack in enumerate(current_stacks):
                if (i != j) and (i != dont_pull_from) and (j != dont_put_on):
                    #print(i,j)
                    #print(list(input_stacks[i].keys())[-1], list(input_stacks[j].keys())[-1])
                    possible_moves.append((list(current_stacks[i].keys())[-1], list(current_stacks[j].keys())[-1]))
                    position_crosswalk.append((i,j))
        return possible_moves, position_crosswalk
        
    
    #@profile()
    def make_state(self, stacks, cost = None):
        if cost == None:
            cost = self.get_delta_score(stacks)
        return PrioritizedItem(cost, stacks)
        
    ##@profile
    def init_astar(self):
        self.goal_reached = False
        self.final_moves_list = [()]
        self.visited_list = []
        #list holding all non-discarded states
        self.states_dict_list = defaultdict(list)            
        self.make_restacked_goal()
        self.search_queue = PriorityQueue(maxsize=self.MAX_ITEMS)
        self.input_state = self.make_state(self.input_stacks)
        self.search_queue.put(self.input_state)  
        print(f"Initial State added to PQ {self.search_queue.qsize()}")
        print("")
        
    ##@profile
    def run_astar_mod(self):
        #self.search queue empty created in __init__
        #self.visited_list emptyy created in __init__
        #self.make_restacked_goal.  make it once no need to keep doing it
        #self.get_restack_goal()
        #makes restacked goal and puts initial input state into search queue
        self.init_astar()
        # Example using threading.Timer
        timer = threading.Timer(5, timeout_handler) # 5 seconds
        timer.start()
        move_number = 0
        print(f"Move Number: {move_number}")
        while not self.search_queue.empty() and not self.goal_reached:
            current_state = self.search_queue.get()
            print(f"Current State Removed {self.search_queue.qsize()}")
            print("")
            #print(current_state)
            #print(f"current_state: {current_state}")
            #print(current_state)
            self.visited_list.append(current_state)
            #get and prune possible moves
            possible_moves, position_crosswalk = self.get_and_vet_possible_moves(current_state, move_number)
           # print(possible_moves)
            
            #print(current_state)
            #place holders for move gen and cost calc
            
            for i, move in enumerate(possible_moves):
                #print(move)
                #make stacks for this move and calc delta
                new_state = self.make_states_for_move(current_state, position_crosswalk[i], move)
                print(f"Move: {move_number}, Iteration {i}: move: {move}, priority: {new_state.get_priority()}, stacks: {new_state.get_item()}")
                print("New State is being populated correctly")
                print("")
     
                #print(move, new_state)
                #     new_state.parent = current_state.id
        
                if new_state.get_priority() == 0:
                    self.final_moves_list.append(move)
                    #final_states_list.append(state)
                    self.goal_reached = True
                    print( f"Goal Reached, move {move}, at move {move_number + 1}, Final State: {new_state.get_item()}")
                    break
                #O(n) oepration, cant use a set with the lists of ordered dicts
                elif new_state.get_item() in self.visited_list:
                    #print(state)
                    print("another to the visited list")
                    print("")
                    continue
                else:
                    #cost slready calcualted
                    print(new_state, type(new_state))
                    self.search_queue.put(new_state) 
 
            
            if timer.alive():
                timer.cancel()
            move_number += 1         
     
       
              
     
    #@profile
    def solve(self, initial_arrangement, goal_arrangement):
        #Add your code here! Your solve method should receive
		#as input two arrangements of blocks. The arrangements
		#will be given as lists of lists. The first item in each
		#list will be the bottom block on a stack, proceeding
		#upward. For example, this arrangement:
		#
		#[["A", "B", "C"], ["D", "E"]]
		#
		#...represents two stacks of blocks: one with B on top
		#of A and C on top of B, and one with E on top of D.
		#
		#Your goal is to return a list of moves that will convert
		#the initial arrangement into the goal arrangement.
		#Moves should be represented as 2-tuples where the first
		#item in the 2-tuple is what block to move, and the
		#second item is where to put it: either on top of another
		#block or on the table (represented by the string "Table").
		#
		#For example, these moves would represent moving block B
		#from the first stack to the second stack in the example
		#above:
		#
		#("C", "Table")
		#("B", "E")
		#("C", "A")
        #edge case 1, input or goal state is empty
        
        self.initialize_round(initial_arrangement, goal_arrangement)
        self.run_astar_mod()
        return self.get_final_moves_list()



