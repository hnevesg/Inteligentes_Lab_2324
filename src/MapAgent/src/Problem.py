from Map import Map

class Problem:

    def __init__(self, initial_state, goal_coordinates : tuple, map_filename : str, maximum_slope : float = 10000, factor_movement : int = 1):
        '''Constructor'''
        self.init_state = initial_state
        self.environment = Map(map_filename)
        self.goal = goal_coordinates
        self.factor_movement = factor_movement
        self.maximum_slope = maximum_slope
        
    def goal_test(self, candidate) -> bool:
        '''Function that checks if a state is a Goal State'''
        if (candidate.x == self.goal[1] and candidate.y == self.goal[0]):
            return True
        return False