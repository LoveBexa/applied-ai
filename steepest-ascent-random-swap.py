import pandas as pd
import numpy as np
import math, random

# Show full width of dataframe
pd.set_option('display.max_colwidth', None)
# pd.set_option('display.max_rows', None)

# Converting csv to data frame and adding headers
headers = ['X', 'Y']
data = pd.read_csv("TSP-Matrix.csv", names=["X","Y"])

# Calculates the euclidean distance between 2 points 
def calculatePath(first, second):
    # Shift index by +1 because starts from 0
    first -= 1
    second -= 1
    x_sq = ((data["X"].iloc[second] - data["X"].iloc[first])) ** 2
    y_sq = ((data["Y"].iloc[second] - data["Y"].iloc[first])) ** 2
    euclidean =  x_sq + y_sq
    length = math.sqrt(euclidean)
    return length
    
########### Step 1 Initial Solution: Greedy approach for first route ########### 

greedy_start = []
# Create a list of 1 to 24 (cities) everytime one is appended to greedy_start one is removed from the list of cities array
cities = list(range(1, 25))
current_path = greedy_start

def remove(city):
    # Every time we append a new city to greedy we pop it from cities array.
    greedy_start.append(city)
    cities.remove(city)

# Start at start_city, add to array
start_city = 4
start_city_next = 8
start_cost = calculatePath(start_city, start_city_next)
# Add first 2 starting points to greedy start and remove from Cities array. 
remove(start_city)
remove(start_city_next)

# Pointer on the current city!
current_city = start_city_next

########### Choose the next best City by calulating all possible routes from current node and selecting minimum cost option ########### 

def nextBest(current):
# Create a dict for current_city > next_city and all the length values

    city_costs = {}
# Iterate through each item in cities array
    for key, city in enumerate(cities):
        # Calculate distance from each city in array to the current_city
        route_cost = calculatePath(current, city)
        # append each of these cities and their cost to a dictionary
        city_costs[city] = route_cost
        
    city_costs = city_costs.items()
    city_costs_2 = list(city_costs)
    # Convert to a dataframe
    city_costs_3 = pd.DataFrame(city_costs_2)
    city_costs_3.columns = ["City","Cost"]
    # Pick the smallest cost
    min_cost = city_costs_3[city_costs_3.Cost == city_costs_3.Cost.min()]
    # next_city = shortest_route city
    next_city = int(min_cost["City"])
    # Return the shortest length
    return next_city

# Iterates through the length of city
while len(cities) > 0:
    # The next city is the shortest calculated route cost
    next_city = nextBest(current_city)
    # Add next best city stop off to the greedy start array and then remove it from the cities list
    remove(next_city)
    


########### Neighbourhood operator: Do a swap of two adjacent cities. However, you are encouraged to experiment with other neighbourhood operators. ########### 


print("Greedy Start = ", greedy_start)
greedy_cost = 0
        # For each city 
for city in greedy_start:
    # Find the index
    city_index = greedy_start.index(city)
    if city_index < 23:
        # Then count up the cost from A -> B, B -> C etc
        greedy_cost = greedy_cost + calculatePath(greedy_start[city_index], greedy_start[city_index+1])
    else:
        # Then make sure we add on the cost of the last city back to the first
        greedy_cost = greedy_cost + calculatePath(greedy_start[23], greedy_start[0])
print("Cost = ",greedy_cost)


# Random swap!

def swap(route):
    new_route = route.copy()
    city1 = random.randint(0, 23)
    city2 = random.randint(0, 23)
    # They must not be the same city as you can't swap these
    if city1 != city2:
        new_route[city1], new_route[city2] = new_route[city2], new_route[city1]
    else: # If they are the same then go to another city
        city1 -= 1
        new_route[city1], new_route[city2] = new_route[city2], new_route[city1]
    return new_route


########### Add the cost of travelling through the cities ########### 

def calculateRoute(route):
    cost_total = 0
        # For each city     
    for key, city in enumerate(route):
        # Find the index
        if route.index(city) < 23:
            # Then count up the cost from A -> B, B -> C etc
            this_city = route[key]
            next_city = route[key+1]
            cost_total = cost_total + calculatePath(this_city, next_city)
        else:
            # Then make sure we add on the cost of the last city back to the first
            cost_total = cost_total + calculatePath(route[23], route[0])

    return round(cost_total, 2)



########### Stopping criteria: No improvement in consecutive 100 iterations or how ever many ########### 

# There are 24 neihbouring cities therefor there are 24-1 neighbouring solutions
swaps = 1000
count = 0

columns = list(range(1, 25))
solutions = {}
        
while swaps > count:
    new_route_1 = swap(greedy_start)
    cost_route = calculateRoute(new_route_1)
    solutions[cost_route] = new_route_1
    count += 1
    
# Convert dictionary to a pandas Data Frame 
solutions_items = solutions.items()
solution_list = list(solutions_items)
solutions_df = pd.DataFrame(solution_list, columns= ["Cost","Solution"])
solutions_df.index += 1

print(solutions_df)

# # Sort by lowest cost
# best_solution = solutions_df.sort_values(by=['Cost'])
# #print(best_solution.head(24))
# print(solutions_df)
# # Print the best solution!!!!!!! 
solutions_df['Cost'] = pd.to_numeric(solutions_df['Cost'])

print("\nThe best solution out of the neighbourhood is solution number", solutions_df['Cost'].idxmin())
print(solutions_df.min())


# Draw route
# ax1 = data.plot.scatter(x='X',y='Y', c='Pink')
# plot.show(block=True);
# data['Z'] = data['Y'] / data['X']
# data_sort = data.sort_values(by=['Z'])
# print(data)