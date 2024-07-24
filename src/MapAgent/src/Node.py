
from types import NoneType
from State import State
import math

class Node:
    '''Class used for representing nodes of the search tree'''
    
    def __init__(self, state: State, strategy, heuristic = float(0), action = None, node_number = 0, cost = (0,0), parent = None):
        '''Constructor'''
        self.parent: Node
        #initial Node
        if parent is None:
            self.depth = 0
            self.cost = cost
            self.id = node_number
            self.action = action
        else:
            self.parent = parent
            self.id = node_number
            self.cost = (self.parent.cost[0] + cost[0], max(self.parent.cost[1], cost[1]))
            self.action = action
            self.depth = self.parent.depth + 1
        
        self.strategy = strategy
        self.state = state
        self.state : 'State'
        
        '''These two depend on the strategy used'''

        self.heuristic = heuristic
        self.value = self.strategy.assignValue(self)

    def compute_heuristic(self, heuristic_type: int, problem):
        '''Function that computes the heuristic of a node'''
        if heuristic_type == 1:
            self.heuristic = float(math.sqrt(math.pow((problem.goal[1]-self.state.x),2) + math.pow((problem.goal[0]-self.state.y),2)))
        elif heuristic_type == 2:
            self.heuristic = int(abs(problem.goal[1]-self.state.x) + abs(problem.goal[0]-self.state.y))
        else:
            self.heuristic = 0   

        self.value = self.strategy.assignValue(self) 
        return self.heuristic, float(self.value)

    def path(self, node):
        '''Function that returns a list of nodes from the root node to that specific node'''
        path = []
        while node.id != 0:
            path.append(str(node))
            node = node.parent
        path.append(node)
        path.reverse()
        string_path = ""
        for node_string in path:
            string_path += f"{node_string}\n"
        return string_path
    
    # <
    def __lt__(self, other : 'Node'): 
        '''Less than operator'''
        if self.value < other.value:
            return True
        # in case of draw, we take the one with the lowest ID
        if self.value == other.value:
            if self.id < other.id:
                return True
        return False
    
    def expand(self, problem, strategy, last_node_id,heuristic_type)->list:
        '''Function that returns a list of nodes that are the successors of the current node
        From the node state's successor function we get the list of successors 
        and we create a node for each successor, passing the current node as the parent'''
        successors = self.state.succesor_function(problem)
        expansion = []
        for successor in successors:
            last_node_id += 1
            new_node = Node(state=successor[1], strategy=strategy, heuristic=self.heuristic, action=successor[0], node_number=last_node_id, cost=successor[2], parent=self)
            new_node.heuristic, new_node.value = new_node.compute_heuristic(heuristic_type, problem)
            expansion.append(new_node)
        return expansion
               
    def __str__(self):
        '''String representation of the node'''
        if self.id == 0:
            return f"[{self.id}][({float(self.cost[0]):.3f},{self.cost[1]:.3f}),{self.state.id},None,None,{self.depth},{self.heuristic:.1f},{self.value:.4f}]"
        return f"[{self.id}][({float(self.cost[0]):.3f},{self.cost[1]:.3f}),{self.state.id},{self.parent.id},{self.action},{self.depth},{self.heuristic:.1f},{self.value:.4f}]"