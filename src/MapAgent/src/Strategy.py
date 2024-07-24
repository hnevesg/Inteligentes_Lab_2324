import Node

# Use of polimorphism to implement the different strategies
class Strategy:

    def assignValue(self, node : Node.Node):
        '''Assigns a value to a node'''
        pass
    
class Breadth(Strategy):

    def assignValue(self, node : Node.Node)-> float:
        '''Assigns a value to a node based on BFS'''
        return float(node.depth)
    
class Depth(Strategy):

    def assignValue(self, node : Node.Node)-> float:
        '''Assigns a value to a node based on DFS'''
        return float(1/(node.depth+1))
    
class Uniform(Strategy):

    def assignValue(self, node : Node.Node)-> float:
        '''Assigns a value to a node based on UCS'''
        return float(node.cost[0])
    
class A_star(Strategy):

    def assignValue(self, node : Node.Node)-> float:
        '''Assigns a value to a node based on A*'''
        return float(node.cost[0] + node.heuristic)

class Greedy(Strategy):

    def assignValue(self, node : Node.Node)-> float:
        '''Assigns a value to a node based on Greedy'''
        return float(node.heuristic)