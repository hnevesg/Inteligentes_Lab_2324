from os import path
import numpy
import Search
import Map
import State
import Problem
import Strategy
import Node
from time import sleep

IMPORT_DIR = '../imports/'

def main():
    print("========== WELCOME TO THE MAP AGENT ==========\n")
    menu()
      
def menu():

    print("\nMenu:")
    print("1. Get height above the sea of a point in the map.")
    print("2. Resize the current map.")
    print("3. Calculate neighbour points of a given point.")
    print("4. Find a route.")
    print("5. Exit.")

    file_name = "./MapAgent/src/data/LaGomera.hdf5" 
    map = Map.Map(file_name)
    previous_map = map

    while True:
        try:
            choice = input("Enter your choice: ")
            if choice == '1':
                coordinate_y = int(input("Enter coordinate y: "))
                coordinate_x = int(input("Enter coordinate x: "))
                try:
                    height_above_sea = map.umt_yx(coordinate_y,coordinate_x)

                    if height_above_sea == map.nodata_value:
                        print("No data found for these coordinates.")
                        continue
                    print(f"Height Above the sea on ({coordinate_y},{coordinate_x}): {height_above_sea:.3f}") 
                except ValueError:
                    print("Invalid coordinates.")
                    continue
            elif choice == '2':
                previous_map = map
                map = choose_resize(map)

                if not map:
                    map = previous_map
                    print("A negative factor is not allowed (negative dimensions don't exist).")
                    continue

                print("Map resized successfully.")

            elif choice == '3':
                coordinate_y = int(input("Enter coordinate y: "))
                coordinate_x = int(input("Enter coordinate x: "))
                max_slope = float(input("Enter the maximum slope (-1 for default value): "))

                s = State.State(y=coordinate_y, x=coordinate_x)   
                if max_slope == -1:
                    p = Problem.Problem(s,(1,1),map.file_name)
                else:                
                    p = Problem.Problem(s,(1,1),map.file_name,maximum_slope=max_slope)
                successors = s.succesor_function(p)
                result = "No neighbour points found."
                if(len(successors) != 0):
                    result = "Neighbour points:\n"
                    for successor in successors:
                        result += f" ('{successor[0]}',{successor[1].id.replace(' ','')},({float(successor[2][0])},{round(float(successor[2][1]),3)}))"
                        result += "\n"
                print(result)

            elif choice == '4':
                coordinate_y = int(input("Enter coordinate y: "))
                coordinate_x = int(input("Enter coordinate x: "))

                goal_y = int(input("Enter goal coordinate y: "))
                goal_x = int(input("Enter goal coordinate x: "))

                max_slope = float(input("Enter the maximum slope (-1 for default value): "))
                s = State.State(y=coordinate_y, x=coordinate_x)    
                if max_slope == -1:
                    p = Problem.Problem(s,(goal_y,goal_x),map.file_name)
                else:              
                    p = Problem.Problem(s,(goal_y,goal_x),map.file_name,maximum_slope=max_slope)
                search = Search.Search()

                print("Choose a strategy:\n1. BFS\n2. DFS\n3. UCS\n4. Greedy\n5. A*")
                strategy = int(input("Enter your choice: "))
                result = choose_strategy(strategy, p, search)
                if result is not None:
                    with open("./results.txt", "w") as f:
                        f.write(result.path(result))
                    print("---- Solution Found. Result saved in results.txt ----")
                else:
                    print("---- No solution found ----")
                
            elif choice == '5':
                print("----- Exiting the program. Goodbye! --------")
                sleep(1.5)
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
                continue
        except Exception as e:
            print(">>>> An error Occurred. Please try again. <<<<")
            map = previous_map
            continue

            
def choose_heursitic():
    
    while True:
        heuristic_type = int(input("Which heuristic are you choosing?\n1. Euclidean\n2.Manhattan"))
        if heuristic_type == 1:
            return 1
        elif heuristic_type == 2:
            return 2
        else:
            print("\nThe allowed values are only 1 & 2\n")    

def choose_strategy(strategy, p, search):
    while True:
           

        if 1 <= strategy <= 3:
            print("Please, wait until the agent finds the solution to the problem. This may take a while...")
            if strategy == 1:
                return search.graph_search(p, Strategy.Breadth(), 500000)
            if strategy == 2:
                return search.graph_search(p, Strategy.Depth(), 500000)
            if strategy == 3:
                return search.graph_search(p, Strategy.Uniform(), 500000)
        elif 4 <= strategy <= 5:
            heuristic_type = choose_heursitic()
            print("Please, wait until the agent finds the solution to the problem. This may take a while...")
            if strategy == 4:
                return search.graph_search(p, Strategy.Greedy(), 500000, heuristic_type)
            if strategy == 5:
                return search.graph_search(p, Strategy.A_star(), 500000, heuristic_type)
        else:
            print("Invalid strategy choice. Please enter a number between 1 and 5.")
            strategy = int(input("Enter your choice: "))

def choose_resize(map):
    resize_num = int(input("Enter the resize factor: "))
    option_selected = False
    resized_name = map.file_name.replace(".hdf5","").split("/")[len(map.file_name.replace(".hdf5","").split("/"))-1]
    while not option_selected:
        operation = input("Enter the operation to be applied when resizing (max or mean): ")        
        if operation == "max":
            map = map.resize(resize_num, numpy.max, resized_name+"Zoom"+str(resize_num)+"_max")
            option_selected = True      
            return map
        elif operation == "mean":
            map = map.resize(resize_num, numpy.nanmean, resized_name+"Zoom"+str(resize_num)+"_mean")
            option_selected = True
            return map
        else:
            print("Invalid operation. Please enter either 'max' or 'mean'.")

    
if __name__ == '__main__':
    main()
    