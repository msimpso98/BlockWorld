import numpy as np
from collections import OrderedDict, defaultdict
from queue import PriorityQueue
import copy

class BlockWorldAgent:
    def __init__(self):
        #If you want to do any initial processing, add it here.
        
        #helper function that conversts single list of letters into
        #an ordered dict with key = letter and value to the lower neighbor
        self.MAX_ITEMS = 26
        self.input_state = None
        self.goal_state = None
        self.goal_reached = False
        self.move_number = None
        self.valid_inputs = None
        self.final_moves_list = [()]
        self.restacked_goal = None
        self.search_queue = PriorityQueue(maxsize=self.MAX_ITEMS)
        self.visited_list = []
        
    def make_letter_stack(self, letter_list):
        letter_list = copy.deepcopy(letter_list)
        letter_listb = ["Table"] + letter_list[0:-1]
        return OrderedDict(zip(letter_list, letter_listb))
    
    def check_inputs(self, input_state_list, goal_state_list):
        if input_state_list != [] and goal_state_list != []:
            self.valid_inputs = True
        else:
            self.valid_inputs = False
            
    def get_valid_inputs(self):
        return self.valid_inputs
    
    def get_final_moves_list(self):
        return self.final_moves_list
    
    def add_to_final_moves_list(self, move):
        self.final_moves_list.append(move)
            
    def initialize_round(self, input_state_list, goal_state_list):
        input_state_list = copy.deepcopy(input_state_list)
        goal_state_list = copy.deepcopy(goal_state_list)
        self.check_inputs(input_state_list, goal_state_list)
        if self.valid_inputs:
            #? why 9?
            self.input_state = [9]*len(input_state_list)
            self.goal_state = [9]*len(goal_state_list)
                
            for i in range(len(self.input_state)):
                self.input_state[i] = self.make_letter_stack(input_state_list[i])
            
            for i in range(len(self.goal_state)):
                self.goal_state[i] = self.make_letter_stack(goal_state_list[i])  
        else:
            print("one or both input matrices are empty. no game possible")
            
            
    def get_input_state(self):
        return self.input_state
    
    def get_goal_state(self):
        return self.goal_state
    
    #makes single ordered dict out of goal stacks, used for delta score calc
    #and goal checking
    def make_restacked_goal(self):
        goal_state = copy.deepcopy(self.goal_state)
        self.restacked_goal = OrderedDict()
        for odict in goal_state:
            self.restacked_goal = self.restacked_goal | odict
            
    
    def get_restacked_goal(self):
        return self.restacked_goal
                
    
    def set_goal_reached(self, value : bool):
        self.goal_reached = value
        
    def get_goal_reached(self):
        return self.goal_reached
    
    def add_to_visted_list(self, state):
        self.visited_list.append(state)
        
   
    def goal_met(input_stacks, goal_stacks):
        if input_stacks == goal_stacks:
            return True
        else:
            return False      
        
    def subgoal_met(input_stack, goal_stack):
        if input_stack == goal_stack:
            return True
        else:
            return False        
        
        
    def correct_so_far(self, input_stack, move_number):
        
        if move_number == 0:
            key_list = list(input_stack.keys())[0:-1]
        else:
           key_list = list(input_stack.keys())
        
        for key in key_list:
            if input_stack[key] != self.get_restacked_goal()[key]:
                return False
        return True
    
        
    def get_delta_score(self, state):
        state = copy.deepcopy(state)
        super_state = OrderedDict()
        for odict in state:
            super_state = super_state | odict
    		
        key_list = list(super_state.keys())
        
            
        delta_score = 0
        
        for key in key_list:
            if key != "Table":
                if super_state[key] != self.restacked_goal[key]:
                    delta_score += 1
        return delta_score
    
    
    def make_a_move(self, source_stack, target_stack, move):
        #you need to mutate the lists here
        #returns a tuple instead of correct kv pair
        item_to_move = source_stack.popitem(last=True)
        new_value = list(target_stack.keys())[-1]
        target_stack[item_to_move[0]] = new_value
    
        return source_stack, target_stack
    
    
   
    def make_stacks_for_move(self, input_stacks, position_tuple, move):
        input_stacks = copy.deepcopy(input_stacks)
        source_stack = input_stacks[position_tuple[0]]
        target_stack = input_stacks[position_tuple[1]]
        source_stack, target_stack = self.make_a_move(source_stack, target_stack, move)
        delta_score = self.get_delta_score(input_stacks)
        return input_stacks, delta_score    
    
    

    def get_and_vet_possible_moves(self, current_state, move_number):
        possible_moves = []
        position_crosswalk = []
        addon_odict = OrderedDict({"Table":99})
        #current_state will need updating if move = 0
        #current_state = copy.deepcopy(current_state)

        
        if move_number == 0:
            current_state.append(addon_odict)
                
        for i, input_stack in enumerate(current_state):
            dont_put_on = 99
            dont_pull_from = 99
            if self.correct_so_far(input_stack, move_number):
                dont_pull_from = i
            else:
                dont_put_on = i
            for j, input_stack in enumerate(current_state):
                if (i != j) and (i != dont_pull_from) and (j != dont_put_on):
                    #print(i,j)
                    #print(list(input_stacks[i].keys())[-1], list(input_stacks[j].keys())[-1])
                    possible_moves.append((list(current_state[i].keys())[-1], list(current_state[j].keys())[-1]))
                    position_crosswalk.append((i,j))
        return possible_moves, position_crosswalk
        
    
    def init_astar(self):
        self.make_restacked_goal()
        self.search_queue.put(self.input_state)    
        
    def run_astar_mod(self):
        #self.search queue empty created in __init__
        #self.visited_list emptyy created in __init__
        #self.make_restacked_goal.  make it once no need to keep doing it
        #self.get_restack_goal()
        #makes restacked goal and puts initial input state into search queue
        self.init_astar()
        
        move_number = 0
        while not self.search_queue.empty() and not self.goal_reached:
            current_state = self.search_queue.get()
            #print(current_state)
            self.visited_list.append(current_state)
            #get and prune possible moves
            possible_moves, position_crosswalk = self.get_and_vet_possible_moves(current_state, move_number)
            
            #print(current_state)
            #place holders for move gen and cost calc
            
            for i, move in enumerate(possible_moves):
                pass
                #print(move)
                #make stacks for this move and calc delta
                new_state, delta_score = self.make_stacks_for_move(current_state, position_crosswalk[i], move)
                print(move, new_state, delta_score)
            #     new_state = make_stacks_for_move(current_state, goal_stacks1b, position_crosswalk[0], move)
            #     new_state.parent = current_state.id
            #     #calc cost of each move
        
            #     if new_state == self.goal_state:
            #         self.final_moves_list.append(move)
            #         #final_states_list.append(state)
            #         self.goal_reached = True
            #         print( f"Goal Reached {possible_moves[i]} at move {move}, {move_number + 1}")
            #         break
            #     #O(n) oepration, cant use a set with the lists of ordered dicts
            #     elif new_state in self.visited_list:
            #         #print(state)
            #         continue
            #     else:
            #         #calc_cost
            #         self.search_queue.put(new_state)
            # #min_move is the last move, min_state is the pentultimate state
            qsize = self.search_queue.qsize()
            move_number += 1         
     
        
    
                
     

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


