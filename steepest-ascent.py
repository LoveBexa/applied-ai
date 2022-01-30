import pandas as pd
import math

# Goal: Run the steepest hill climb! 

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
    
########### Step 1 Initial Solution: Greedy approach for first route

greedy_start = []
# Create a list of 1 to 24 (cities) everytime one is appended to greedyStart one is removed from here
cities = list(range(1, 25))

# Start at start_city, add to array
start_city = 1
start_city_next = 4

def cityList(pop):
        
    # Every time we append a new city to greedy we pop it from cities array.
    greedy_start.append(pop)
    cities.remove(pop)

# Go to start_cityNext, add to array 
cityList(start_city)
cityList(start_city_next)


# Calculate the first route cost
start_cost = calculatePath(start_city, start_city_next)

# Pointer on the current city!
current_city = start_city_next


def nextBest(route):
# Create a dict for current_city > next_city and all the length values

    city_costs = {}
# Iterate through each item in cities array
    for key, city in enumerate(cities):
        # Calculate distance from each city in array to the current_city
        route_cost = calculatePath(current_city, city)
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
    print(next_city)

nextBest(current_city)
# Return the largest length
# Iterate through the next largest length 
# At each step of the journey, visit the nearest unvisited city that will reduce the route the most
# Pick the next largest gap from start city to end city.



########### Step 2: Neighbourhood operator: Do a swap of two adjacent cities. However, you are encouraged to experiment with other neighbourhood operators.

########### Step 3: Solution evaluation: Add the cost of travelling through the cities

########### Step 4: Stopping criteria: No improvement in consecutive 100 iterations (feel free to play around with this parameter by increasing or decreasing its numeric value).


# Draw route
# ax1 = data.plot.scatter(x='X',y='Y', c='Pink')
# plot.show(block=True);
# data['Z'] = data['Y'] / data['X']
# data_sort = data.sort_values(by=['Z'])
# print(data)
