import pandas as pd
import numpy as np
import random
import math
import matplotlib as plot

# Show full width of dataframe
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_row', None)
# pd.set_option('display.max_rows', None)

# Converting csv to data frame and adding headers
headers = ['X', 'Y']
data = pd.read_csv("TSP-Matrix.csv", names=["X","Y"])
print(data)

############## Step 1: Initial Solution: Based on either the random or greedy start

# Create a list of 1 to 24 (cities) everytime one is appended to greedy_start one is removed from the list of cities array
cities = list(range(0, 25))
greedy_start = []

def randomStart():
    random_route = random.sample(range(1, 25), 24)
    print("Random start:", random_route)

def greedyStart(city1,city2):

    global current_city
    
    # Make current city the last visited city (num2)
    current_city = city2
    # Append and remove first and second items from greedy parameter
    appendRemove(city1)
    appendRemove(city2)
    
    # We want to go through the length of not chosen city list 
    while len(cities) > 0:
        # Then we want to find the next best city according to the current city we are on
        next_city = findNext(current_city)
        # Add next best city stop off to the greedy start array and then remove it from the cities list
        appendRemove(next_city)
        next_city = current_city
  
    print("Greedy Start:",greedy_start)
        
    
############## Step 2: Neighbourhood operator: Inversion operation

def randomSwap(route):
    new_route = route.copy()
    city1 = random.randint(0, 24)
    city2 = random.randint(0, 24)
    # They must not be the same city as you can't swap these
    if city1 != city2:
        new_route[city1], new_route[city2] = new_route[city2], new_route[city1]
    else: # If they are the same then go to another city
        city1 -= 1
        new_route[city1], new_route[city2] = new_route[city2], new_route[city1]
    return new_route


############## Step 3: Solution evaluation: Add the cost of travelling through the cities

# Calculates the euclidean distance between 2 points 
def calculatePath(city1, city2):
    
    # We need to find this number from the pandas dataframe but - 1
    # Shift index by -1 because index starts from 0 not 1
    city1_index = city1 - 1
    city2_index = city2 - 1
    
    # Find position of city within the DataFrame to calculate Euclidean distance between the 2 points for X, Y
    x_sq = ((data["X"].iloc[city2_index] - data["X"].iloc[city1_index])) ** 2
    y_sq = ((data["Y"].iloc[city2_index] - data["Y"].iloc[city1_index])) ** 2
    euclidean =  x_sq + y_sq
    length = math.sqrt(euclidean)
    
    return length

# Calculates the cost of the entire array of path/solution using euclidean distance

def calculateRoute(route):
    cost_total = 0
        # For each city     
    for key, city in enumerate(route):
        # Find the index
        if route.index(city) < 24:
            # Then count up the cost from A -> B, B -> C etc
            this_city = route[key]
            next_city = route[key+1]
            cost_total = cost_total + calculatePath(this_city, next_city)
        else:
            # Then make sure we add on the cost of the last city back to the first
            cost_total = cost_total + calculatePath(route[23], route[0])

    return round(cost_total, 2)


def findNext(current):
    # Create a temp dict for current_city > next_city and all the length values
    city_costs = {}
    # Iterate through each item in cities array
    for index, each in enumerate(cities):
        # Calculate cost from current city to each city not visited
        path_cost = calculatePath(current, each)
        # Append each of these cities and their cost to a dictionary
        city_costs[each] = path_cost
    # Convert the dictionary into items and then a list    
    city_costs = city_costs.items()
    list_city = list(city_costs)
    # Convert list into a DataFrame
    city_dataframe = pd.DataFrame(list_city)
    # Give DataFrame column names
    city_dataframe.columns = ["City","Cost"]
    # Pick the smallest cost
    min_cost = city_dataframe.loc[city_dataframe.Cost == city_dataframe.Cost.min(), 'City'].values[0]
    # Return the city with the minimum cost
    return min_cost

    
def appendRemove(city):
    # Every time we append a new city to new solution path we must pop it from cities array.
    greedy_start.append(city)
    cities.remove(city)

############## Step 4: Stopping criteria: When temperature T reaches to Tmin. Tmax = 10.00 /Tmi n = 0.0005 / alpha = 0.995


# Create a function with parametres current cost, new cost, temperature 
def acceptanceProbability(current,new,temperature):
    # If the new solution is better, accept it
    currentCost = calculateRoute(current)
    newCost = calculateRoute(new)
    
    # Calculate the acceptance probability
    accepted = math.exp((currentCost - newCost) / temperature)
    return accepted


###############  CONFIGURATIONS  ###############

# Maximimum temperature it starts at 
current_temp = 5.00
# Minimum temperature it stops at 
temp_min = 0.001
# The rate of reduction
alpha = 0.9
# Iteration s
total_iterations = 1
iteration_index = 0
counter = 0

# Create an array with all the costs
solution_costs = {}


# Setting up the greedy start solution 
greedyStart(4,8)
greedy_cost = calculateRoute(greedy_start)
print("Greedy cost:", greedy_cost)
# Or choose randomStart() 

start_route = greedy_start
best_route = greedy_start

# while iteration is equal to or less than total iterations needed per "temperature leve"
while iteration_index <= total_iterations: 
    # Generate a new neighbour by swapping adjacent
    new_route = randomSwap(start_route)
    # Calculate cost 
    current_cost = calculateRoute(best_route)
    new_route_cost = calculateRoute(new_route)

    # If new neighbour costs less than current best route accept that is the best route 
    if new_route_cost < current_cost:
        best_route = new_route
        # print("FIrst pick best route", best_route, "Cost", calculateRoute(best_route))
    # IF new neighbour costs more than current best route calculate the probability 
    else:
        new_probability = acceptanceProbability(best_route, new_route, current_temp)
        # Generate random number between 0 and 1 
        random_number = random.uniform(0,1)
        # If random number < probability = accept move and change to best_route
        if random_number < new_probability:
            best_route = new_route
            print("New route best route", best_route, "Cost", calculateRoute(best_route))

    # If we have run through all iterations
    if iteration_index == total_iterations:
        # Then we should reduce temperature
        current_temp = current_temp * alpha
        # And reset the counter 
        iteration_index = 0
        # print("test")
    else:
        iteration_index += 1
        # print("test 2")
    counter += 1 
    print("Solution " + str(counter), best_route, "Cost:", calculateRoute(best_route))
    
    # Append all costs to a dict
    solution_costs[counter] = calculateRoute(best_route)

    
    ####### STOPPING CRITERIA #######
    if current_temp < temp_min:
        break

solution_cost = solution_costs.items()
list_of_solutions = list(solution_cost)
# Convert list into a DataFrame
solution_df = pd.DataFrame(list_of_solutions)
# Give DataFrame column names
solution_df.columns = ["Solution","Cost"]

print("Overall best solution:", best_route, "\nCost:", calculateRoute(best_route))
print("Total iterations:", counter)       

######### Draw graphs
solution_df.plot.line(x=0, y=1, style='-o',marker='x', figsize=(20, 10));
solution_df.plot()