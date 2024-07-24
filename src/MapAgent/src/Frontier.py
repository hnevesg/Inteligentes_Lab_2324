import bisect
from Node import Node
import time
import random

class Frontier:
    ''''Frontier object that stores nodes in a Search Problem'''
    def __init__(self):
        '''Constructor'''
        self.nodes_inserted = -1
        self.frontier = []

    def insert(self, node):
        '''Function that inserts in the right order a node in the frontier'''
        bisect.insort(self.frontier, node)
        self.nodes_inserted += 1

    def remove(self):
        '''Function that removes the first node in the frontier'''
        return self.frontier.pop(0)

    def isEmpty(self):
        '''Function that checks if the frontier is empty'''
        return len(self.frontier) == 0
    
    def add_all(self,expand):
        '''Function that adds all the nodes in the expand list to the frontier'''
        for node in expand:
            self.insert(node)

    def test(self):
        '''Stress test. It adds nodes with random values to the frontier until it reaches the memory limit, then prints. 
            The timestamp when this limit is reached'''
        timestamp = time.time()
        for i in range(500000):
            node = Node(None,None,None,(0,0),None,0) # type: ignore
            print("node added after", time.time() - timestamp, "time units")
            node.value = random.randint(0,100)
            try:
                self.insert(node)
            except MemoryError:
                print("Memory limit reached at: ", time.time() - timestamp)
                print("Number of nodes in the frontier: ", len(self)) 
                break

    def __len__(self):
        '''Function that returns the number of nodes in the frontier'''
        return len(self.frontier)

    def __str__(self):
        '''Function that returns a string with the contents of the frontier'''''
        frontier_str = "Contents of the frontier:\n"
        for node in self.frontier:
            frontier_str += f"{str(node)}\n"
        return frontier_str
