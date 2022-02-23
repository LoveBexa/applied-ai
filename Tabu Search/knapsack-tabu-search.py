import pandas as pd
import numpy as np
import math, random

# Show full width and height of dataframe
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

# Converting csv to data frame. Total weight = 2621
data = pd.read_csv("/Users/bexa/Documents/Computer Science/Applied AI/Code.py/Data Files/knapsack.csv")

data_true = data
data_true["true value"] = data_true["values"] / data_true["weights"]

# Add another column for v/w 

# Item list 1-100
items = random.sample(range(1, 101), 100)

########### Calculating bag items ###########

def calculateTotalWeight(bag):
    total_weight = 0
    for item in bag:
    # Iterate through dataframe of bag items
        for index, row in data_true.iterrows():
            if (item == index):
                total_weight += row["weights"]
    return total_weight

def calculateTotalValue(bag):
    total_value = 0
    for item in bag:
    # Iterate through dataframe of bag items
        for index, row in data_true.iterrows():
            if (item == index):
                total_value += row["values"]
    return total_value

def calculateWeight(item):
        for index, row in data_true.iterrows():
            if (item == index):
                return row["weights"]
            
def calculateValue(item):
        for index, row in data_true.iterrows():
            if (item == index):
                return row["values"]
    
def calculateTrueValue(item):
        for index, row in data_true.iterrows():
            if (item == index):
                return row["true value"]
            
def leftovers(bag):
    current_bag = bag
    # Total items from 1 to 100
    total_items = items
    # Items - current bag = leftover bag 
    leftovers = [i for i in total_items if i not in current_bag]
    return leftovers


########### Knapsack Bag Initialisations ########### 


# random_start = random.sample(range(1, 101), 100)

random_start =[ 13, 74, 98, 50, 31, 89, 2, 12, 68, 65, 96, 93, 25, 40, 78, 59, 15, 55, 19, 62, 75, 9, 35, 37, 48, 79, 87, 82, 20, 28, 72, 45, 77, 38, 23, 32, 85, 70, 42, 10, 54, 90, 44, 58, 56, 94, 41, 92, 8, 1, 5, 69, 29, 46]


starting_best = random_start.copy()
best_solution = random_start.copy()

tabu_list = []
tabu_list.append(random_start)

# How many iterations the of 
iterations = 3

bag_leftovers =  leftovers(random_start)
bag_weight = calculateTotalWeight(random_start)
bag_value = calculateTotalValue(random_start)

bag_capacity = 1500 

print(bag_weight, bag_value)

def generateNeighbours(solution):
    neighbour_solutions = []
    counter = 0
    # Deep copy array
    while counter < iterations: 
        bag_copy = solution.copy()
        leftover_copy = leftovers(solution).copy()
        # Grab random item from current bag
        random_bag = random.choice(bag_copy)
        # Grab a random item from the leftover bag
        random_leftover = random.choice(leftover_copy)
        # Remove and add new item
        bag_copy.remove(random_bag)
        bag_copy.append(random_leftover)
        # Remove it from the leftover bag
        leftover_copy.remove(random_leftover)
        neighbour_solutions.append(bag_copy)
        counter += 1
    return neighbour_solutions
    
def bestNeighbour(neighbourhood):
    best_neighbour = random_start
    for solution in neighbourhood:
        if (calculateTotalValue(solution) > calculateTotalValue(best_neighbour)) and (calculateTotalWeight(solution) <= bag_capacity):
            best_neighbour = solution
        else:
            continue
    print(calculateTotalWeight(best_neighbour), calculateTotalValue(best_neighbour), best_neighbour)
    return best_neighbour
    
def tabuSearch():
    global best_solution, starting_best
    
    i = 0
    
    while iterations < 5:
        # Use best candidate as start solution
        neighbourhood = generateNeighbours(best_solution)
        best_solution = bestNeighbour(neighbourhood)
        for solution in neighbourhood:
            if solution not in tabu_list and calculateTotalValue(solution) > calculateTotalValue(best_solution):
                best_solution = solution
                tabu_list.append(solution)
                
        if calculateTotalValue(best_solution) > calculateTotalValue(starting_best):
            starting_best = best_solution
        
        if len(tabu_list) > iterations:
            tabu_list.pop(0)
        i += 1
        
tabuSearch()