from typing import Any
from Node import Node
from Frontier import Frontier
from Problem import Problem
from State import State

class Search:
    '''Class used for representing the graph search algorithm'''
    
    def graph_search(self, problem : Problem, strategy, max_depth, heuristic_type = 0):
        '''Function that implements the graph search algorithm'''
        # Invalid initial or goal state
        if not problem.init_state.validate(problem) or not State(y=problem.goal[0],x=problem.goal[1]).validate(problem):
            return None
        fringe = Frontier()
        closed = []
        initial_node = Node(problem.init_state,strategy)
        initial_node.heuristic, initial_node.value = initial_node.compute_heuristic(heuristic_type, problem)
        fringe.insert(initial_node)
        solution_found = False
        
        node = None
        while not solution_found:
            if fringe.isEmpty():
                return None
            node = fringe.remove() 
            if problem.goal_test(node.state):
                solution_found = True
            elif node.depth < max_depth and not self.belongs(closed,node.state.id):
                self.insert(closed,node.state.id)
                fringe.add_all(node.expand(problem, strategy, fringe.nodes_inserted,heuristic_type))
        
        return node
    
    def belongs(self,set,element):
        '''Function that checks if a state belongs to the closed list'''
        return element in set
    
    def insert(self,set,element):
        '''Function that inserts the state id of the node to the closed list'''
        set.append(element)