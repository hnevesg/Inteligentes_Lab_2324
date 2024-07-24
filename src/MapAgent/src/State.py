from shutil import move
from Problem import Problem
from enum import Enum
import math

class Directions(Enum):
    '''Class used for representing actions. Is an Enumeration'''
    N = "N"
    E = "E"
    S = "S"
    W = "W"

class State:
    '''Class used for representing states'''
    def __init__(self, id = None, y = None, x = None):
        '''Constructor'''
        if y is not None and x is not None:
            self.x = int(x)
            self.y = int(y)
            self.id = f"({y},{x})"

        elif id is not None:
            self.id = str(id)
            id_data = self.id.replace("(","").replace(")","").split(",")
            self.y = int(id_data[0])
            self.x = int(id_data[1])

        elif id is None and y is None and x is None:
            self.id = "()"
            self.x = 0
            self.y = 0
        # Length and Height of any movement (will be used on successor_function)

    def succesor_function(self, problem : Problem): 
        '''Function that defines the successors for the current state, returning them along with the action and cost'''
        successors = []

        # If the state to evaluate is valid, then is adecuate to have successors
        if not self.validate(problem):
            return successors
        
        movement_factor = problem.factor_movement
        problem_cell_size = problem.environment.size_cell
        for direction in Directions:
            if direction == Directions.N:
                successor = State(y=self.y+(movement_factor*problem_cell_size), x=self.x) # type: ignore
                if successor.validate(problem):
                    successor_tuple = (direction.value, successor, (math.sqrt(math.pow(successor.y-self.y,2)+math.pow(successor.x-self.x,2)),abs(problem.environment.umt_yx(successor.y,successor.x)-problem.environment.umt_yx(self.y,self.x)))) # type: ignore
                    if successor_tuple[2][1] < problem.maximum_slope:
                        successors.append(successor_tuple)
            elif direction == Directions.E:
                successor = State(y=self.y, x=self.x+(movement_factor*problem_cell_size))     # type: ignore
                if successor.validate(problem):
                    successor_tuple = (direction.value, successor,  (math.sqrt(math.pow(successor.y-self.y,2)+math.pow(successor.x-self.x,2)),abs(problem.environment.umt_yx(successor.y,successor.x)-problem.environment.umt_yx(self.y,self.x)))) # type: ignore
                    if successor_tuple[2][1] < problem.maximum_slope:
                        successors.append(successor_tuple)
            elif direction == Directions.S:
                successor = State(y=self.y -(movement_factor * problem_cell_size), x=self.x) # type: ignore
                if successor.validate(problem):
                    successor_tuple = (direction.value, successor,  (math.sqrt(math.pow(successor.y-self.y,2)+math.pow(successor.x-self.x,2)),abs(problem.environment.umt_yx(successor.y,successor.x)-problem.environment.umt_yx(self.y,self.x)))) # type: ignore
                    if successor_tuple[2][1] < problem.maximum_slope:
                        successors.append(successor_tuple)
            elif direction == Directions.W:
                successor = State(y=self.y, x=self.x-(movement_factor*problem_cell_size)) #type: ignore
                if successor.validate(problem):
                    successor_tuple = (direction.value, successor,  (math.sqrt(math.pow(successor.y-self.y,2)+math.pow(successor.x-self.x,2)),abs(problem.environment.umt_yx(successor.y,successor.x)-problem.environment.umt_yx(self.y,self.x)))) # type: ignore
                    if successor_tuple[2][1] < problem.maximum_slope:
                        successors.append(successor_tuple)
        return successors
    
    def validate(self, problem : Problem) -> bool:
        '''Function that defines if a state is valid for a given map'''
        if self.x < problem.environment.up_left[0] or self.x >= problem.environment.down_right[0]:
            return False
        if self.y < problem.environment.down_right[1] or self.y >= problem.environment.up_left[1]:
            return False
        if problem.environment.umt_yx(self.y,self.x) == problem.environment.nodata_value:
            return False
        return True