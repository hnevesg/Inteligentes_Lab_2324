
import numpy
import Map
from os import path
import State
import Search
import math
import Strategy
import Problem
   
def test_map_1():
    file_name = "./data/LaGomera.hdf5" 
    map_lagomera = Map.Map(file_name)
    test_file = open("test_map_original.txt", "r")


    file_data = test_file.readlines()
    for line in file_data:
        result = line.split("\t")

        y = int(result[0])
        x = int(result[1])
        expected = float(result[2])

        obtained = map_lagomera.umt_yx(y,x)
        passed = math.isclose(float(f"{obtained:.3f}"), expected)
        if not passed:
            print(f"{obtained} is not equal to {expected}")
            
        assert passed

def test_map_300resize():
    file_name = "data/LaGomera.hdf5" 
    map_lagomera = Map.Map(file_name)
    test_resized300file = open("test_map_300_mean.txt", "r")
    resized_map = map_lagomera.resize(300, numpy.nanmean, "prueba_resize_1_300")
    file_data = test_resized300file.readlines()

    if resized_map is None:
        print("A negative factor is not allowed (negative dimensions don't exist).")
    else:        
        for line in file_data:
            result = line.split("\t")
            y = int(result[0])
            x = int(result[1])
            expected = float(result[2])

            obtained = resized_map.umt_yx(y,x)
            passed = math.isclose(float(f"{obtained:.3f}"), expected)
            if not passed:
                print(f"{obtained} is not equal to {expected}")
            
            assert passed

    test_resized300file.close()

def test_map_400resize():
    file_name = "data/LaGomera.hdf5" 
    map_lagomera = Map.Map(file_name)
    test_resized400file = open("test_map_400_max.txt", "r")
    file_data = test_resized400file.readlines()
    resized_map = map_lagomera.resize(400, numpy.max, "prueba_resize_1_400")

    if resized_map is None:
        print("A negative factor is not allowed (negative dimensions don't exist).")
    else:        

        for line in file_data:
            result = line.split("\t")
            y = int(result[0])
            x = int(result[1])
            expected = float(result[2])

            obtained = resized_map.umt_yx(y,x)
            passed = math.isclose(float(f"{obtained:.3f}"), expected)
            if not passed:
                print(f"{obtained} is not equal to {expected}")
            
            assert passed
    test_resized400file.close()
                        
def test_successors_1():
    example_name="./data/prueba_resize_1_300.hdf5" 
    test_file = open("sucesores_300_mean.txt", "r")
        
    file_data = test_file.readlines()
   
    for line in file_data:
        tokens= line.split(" ")
        test_state_id = tokens[0].strip('\n')
        s = State.State(test_state_id)                  
        p = Problem.Problem(s,(1,1),example_name,maximum_slope=10000)
        successors = s.succesor_function(p)
        obtained_line = s.id
        failing_data = 0
        if(len(successors) != 0):
            for successor in successors:
                obtained_line += f" ('{successor[0]}',{successor[1].id.replace(' ','')},({float(successor[2][0])},{round(float(successor[2][1]),3)}))"
                successor_id = successor[1].id.replace(' ','')
                state_successor = State.State(successor_id)
                failing_data = (p.environment.umt_yx(s.y,s.x),p.environment.umt_yx(state_successor.y,state_successor.x))
        obtained_line += "\n"

        passed = obtained_line == line
        if not passed:
            print(f"Obtained: {obtained_line} \t Expected: {line}")
            print(f"Value of UMT SUCCESSOR: {failing_data}")

        assert passed
    
    test_file.close()

def test_successors_2():
    example_name="./data/prueba_resize_1_400.hdf5" 
    test_file = open("sucesores_400_max.txt", "r")

    file_data = test_file.readlines()
   

    for line in file_data:
        tokens= line.split(" ")
        test_state_id = tokens[0].strip('\n')
        s = State.State(test_state_id)                   
        p = Problem.Problem(s,(1,1),example_name,maximum_slope=10000)
        successors = s.succesor_function(p)
        obtained_line = s.id
        failing_data = 0
        if(len(successors) != 0):
            for successor in successors:
                obtained_line += f" ('{successor[0]}',{successor[1].id.replace(' ','')},({float(successor[2][0])},{round(float(successor[2][1]),3)}))"
                successor_id = successor[1].id.replace(' ','')
                state_successor = State.State(successor_id)
                failing_data = (p.environment.umt_yx(s.y,s.x),p.environment.umt_yx(state_successor.y,state_successor.x))
        obtained_line += "\n"

        passed = obtained_line == line
        if not passed:
            print(f"Obtained: {obtained_line} \t Expected: {line}")
            print(f"Value of UMT SUCCESSOR: {failing_data}")

        assert passed
    
    test_file.close()
        
def test_3_1():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("ejemplo1.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3117601, x = 273733)  
    p = Problem.Problem(s, (3107401,287533), example_name,maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Breadth(), 500000)
    
    if node:
        with open("ejemplo1_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("ejemplo1_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_3_2_1():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("ejemplo21.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3118801, x = 273133)  
    p = Problem.Problem(s, (3106201, 285733), example_name,maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Depth(), 500000)
    
    if node:
        with open("ejemplo21_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("ejemplo21_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_3_2_2():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("ejemplo22.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3118801, x = 273133)  
    p = Problem.Problem(s, (3106201,285733), example_name,maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Uniform(), 500000)
    
    if node:
        with open("ejemplo22_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("ejemplo22_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]

    if not node:
        print("No solution found")

def test_3_3():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("ejemplo3.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3118801, x = 273133)  
    p = Problem.Problem(s, (3106201, 285733), example_name,maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Breadth(), 500000)
    
    if node:
        with open("ejemplo3_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("ejemplo3_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]

    if not node:
        print("No solution found")


def test_3_4():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("ejemplo4.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3102601, x = 281533)  
    p = Problem.Problem(s, (3121801, 279133), example_name,maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Uniform(), 500000)
    
    if node:
        with open("ejemplo4_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("ejemplo4_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

    
def test_3_5():
    example_name="./data/prueba_resize_1_300.hdf5" 
 
    expected_data = [] 
    with open("ejemplo5.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3102601, x = 281533)  
    p = Problem.Problem(s, (3121801, 279133), example_name,maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Depth(), 500000)
    
    if node:
        with open("ejemplo5_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("ejemplo5_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]

    if not node:
        assert False
    
def test_3_6():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("ejemplo6.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3102601, x = 281533)  
    p = Problem.Problem(s, (3121801, 279133), example_name,maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Breadth(), 500000)
    
    if node:
        with open("ejemplo6_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("ejemplo6_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_3_7():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("ejemplo7.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3117601, x = 273733)  
    p = Problem.Problem(s, (3107401, 287533), example_name,maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Uniform(), 500000)
    
    if node:
        with open("ejemplo7_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("ejemplo7_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_3_8():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("ejemplo8.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3117601, x = 273733)  
    p = Problem.Problem(s, (3107401, 287533), example_name,maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Depth(), 500000)
    
    if node:
        with open("ejemplo8_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("ejemplo8_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")


def test_4_E0():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("./MapAgent/src/ejemplos_euclidea0.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3106201, x = 274933)
    p = Problem.Problem(s, (3119401, 282133), example_name, maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.A_star(), 500000, 1)
    
    if node:
        with open("./MapAgent/src/ejemplo_eucl0_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("./MapAgent/src/ejemplo_eucl0_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_4_E1():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("./MapAgent/src/ejemplos_euclidea1.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3106201, x = 274933)
    p = Problem.Problem(s, (3119401, 282133), example_name, maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Greedy(), 500000, 1)
    
    if node:
        with open("./MapAgent/src/ejemplo_eucl1_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("./MapAgent/src/ejemplo_eucl1_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_4_E2():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("./MapAgent/src/ejemplos_euclidea2.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3116401, x = 271933)
    p = Problem.Problem(s, (3108601, 288733), example_name, maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.A_star(), 500000, 1)
    
    if node:
        with open("./MapAgent/src/ejemplo_eucl2_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("./MapAgent/src/ejemplo_eucl2_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_4_E3():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("./MapAgent/src/ejemplos_euclidea3.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3116401, x = 271933)
    p = Problem.Problem(s, (3108601, 288733), example_name, maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Greedy(), 500000, 1)
    
    if node:
        with open("./MapAgent/src/ejemplo_eucl3_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("./MapAgent/src/ejemplo_eucl3_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_4_E4():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("./MapAgent/src/ejemplos_euclidea4.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3105001, x = 279133)
    p = Problem.Problem(s, (3119401, 280333), example_name, maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.A_star(), 500000, 1)
    
    if node:
        with open("./MapAgent/src/ejemplo_eucl4_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("./MapAgent/src/ejemplo_eucl4_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_4_E5():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("./MapAgent/src/ejemplos_euclidea5.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3105001, x = 279133)
    p = Problem.Problem(s, (3119401, 280333), example_name, maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Greedy(), 500000, 1)
    
    if node:
        with open("./MapAgent/src/ejemplo_eucl5_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("./MapAgent/src/ejemplo_eucl5_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_4_E6():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("./MapAgent/src/ejemplos_euclidea6.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3117001, x = 271933)
    p = Problem.Problem(s, (3107401, 288733), example_name, maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.A_star(), 500000, 1)
    
    if node:
        with open("./MapAgent/src/ejemplo_eucl6_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("./MapAgent/src/ejemplo_eucl6_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_4_E7():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("./MapAgent/src/ejemplos_euclidea7.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3117001, x = 271933)
    p = Problem.Problem(s, (3107401, 288733), example_name, maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Greedy(), 500000, 1)
    
    if node:
        with open("./MapAgent/src/ejemplo_eucl7_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("./MapAgent/src/ejemplo_eucl7_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_4_M0():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("./MapAgent/src/ejemplos_manhattan0.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3105601, x = 274333)
    p = Problem.Problem(s, (3120001, 283333), example_name, maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.A_star(), 500000, 2)
    
    if node:
        with open("./MapAgent/src/ejemplo_manh0_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("./MapAgent/src/ejemplo_manh0_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_4_M1():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("./MapAgent/src/ejemplos_manhattan1.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3105601, x = 274333)
    p = Problem.Problem(s, (3120001, 283333), example_name, maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Greedy(), 500000, 2)
    
    if node:
        with open("./MapAgent/src/ejemplo_manh1_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("./MapAgent/src/ejemplo_manh1_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_4_M2():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("./MapAgent/src/ejemplos_manhattan2.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3108601, x = 274933)
    p = Problem.Problem(s, (3116401, 287533), example_name, maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.A_star(), 500000, 2)
    
    if node:
        with open("./MapAgent/src/ejemplo_manh2_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("./MapAgent/src/ejemplo_manh2_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_4_M3():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("./MapAgent/src/ejemplos_manhattan3.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3108601, x = 274933)
    p = Problem.Problem(s, (3116401, 287533), example_name, maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Greedy(), 500000, 2)
    
    if node:
        with open("./MapAgent/src/ejemplo_manh3_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("./MapAgent/src/ejemplo_manh3_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_4_M4():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("./MapAgent/src/ejemplos_manhattan4.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3118801, x = 273733)
    p = Problem.Problem(s, (3106201, 285133), example_name, maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.A_star(), 500000, 2)
    
    if node:
        with open("./MapAgent/src/ejemplo_manh4_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("./MapAgent/src/ejemplo_manh4_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_4_M5():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("./MapAgent/src/ejemplos_manhattan5.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3118801, x = 273733)
    p = Problem.Problem(s, (3106201, 285133), example_name, maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Greedy(), 500000, 2)
    
    if node:
        with open("./MapAgent/src/ejemplo_manh5_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("./MapAgent/src/ejemplo_manh5_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")

def test_4_M6():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("./MapAgent/src/ejemplos_manhattan6.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3103801, x = 277933)
    p = Problem.Problem(s, (3120601, 282133), example_name, maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.A_star(), 500000, 2)
    
    if node:
        with open("./MapAgent/src/ejemplo_manh6_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("./MapAgent/src/ejemplo_manh6_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")
        
def test_4_M7():
    example_name="./data/prueba_resize_1_300.hdf5" 

    expected_data = [] 
    with open("./MapAgent/src/ejemplos_manhattan7.txt", "r") as test_file:
        expected_data = test_file.readlines()
    
    s = State.State(y = 3103801, x = 277933)
    p = Problem.Problem(s, (3120601, 282133), example_name, maximum_slope=100)
    search = Search.Search()
    node = search.graph_search(p, Strategy.Greedy(), 500000, 2)
    
    if node:
        with open("./MapAgent/src/ejemplo_manh7_result.txt", "w") as f:
            f.write(node.path(node))
    
        with open("./MapAgent/src/ejemplo_manh7_result.txt", "r") as obtained_file:
            obtained_data = obtained_file.readlines()
            for line in obtained_data:
                assert line == expected_data[expected_data.index(line)]
    
    if not node:
        print("No solution found")