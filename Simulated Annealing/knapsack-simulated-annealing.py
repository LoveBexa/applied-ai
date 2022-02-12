import enum
from importlib.resources import contents
import pandas as pd
import random, math

########### Convert CSV to DataFrame ########### 

# Show full width and height of dataframe
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

# Converting csv to data frame. Total weight of items = 2621kg

data = pd.read_csv("knapsack.csv")
# Find "true weight" ratio of each item; values divided by weights
data_true = data
data_true["true value"] = data_true["values"] / data_true["weights"]

########### Knapsack Bag Initialisations ########### 

bag_weight = 0
bag_value = 0
bag_contents = []
bag_leftovers = []
bag_capacity = 1500 
 
########### Step 1: Initial Solution: Greedy start from higher true value ########### 


# Random first node for greedy there are 100 available items
random_start = random.uniform(0,100)

print(random_start)

# Sort items in descending order based on true value to help with greedy start
data_true = data_true.sort_values('true value',ascending=False)
# Add 1 to index so item numbers start from 1 not 0
data_true.index += 1
# print(data_true)

# Iterate 1st time through each item in the dataframe from largest true value down to smallest
for index, row in data_true.iterrows():
    # print (index, row["weights"], row["values"], row["true value"])
# If current weight of bag + weight of new item is less than 1200kg
    if bag_weight + row["weights"] <= bag_capacity:
        # Add to bag
        bag_contents.append(index)
        # Then increase current bag weight & value
        bag_weight += row["weights"]
        bag_value += row["values"]
    else:
        # Skipped items goes into the bag_leftovers (to iterate over the next time)
        bag_leftovers.append(index)

# # Iterate 2nd time through the bag_leftovers again to see if anything can be added 
# for item in bag_leftovers:
#     # Iterate through dataframe of bag items
#     for index, row in data_true.iterrows():
#         # If the item in leftover bag is the same as dataframe item (to find the weight and value)
#         # And if the weight of that item + current weight is less than maximum capacity
#         if (item == index) & (bag_weight + row["weights"] <= bag_capacity):
#             # Find the weight of item and add it to bag
#             bag_weight += row["weights"]
#             bag_value += row["values"] 
#             # Add item to the bag_contents 
#             bag_contents.append(index)
#             # Remove from bag_leftovers
#             bag_leftovers.remove(item)



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


########### Step 2: Neighbourhood operator: random swap each item from leftovers with a random bag item ########### 


def swap(contents, leftovers):
    
    # For this neighbourhood operatore I want to random swap the items len(leftover) times to cover bags that have contained every single of the items
    # In order to do so we need to be able to ensure the bags are < 1500kg maximum weight
    # Once the item in leftover bag has been swapped it should be popped from the leftovers
    
    temp_bag = contents.copy()
    temp_leftovers = leftovers.copy()
    
    # Once item found to swap change to true
    swapped_item = False
    
    while swapped_item == False:
        # Get item from leftover bag
        add_item = random.choice(temp_leftovers)
        # Iterate through dataframe of bag values, weights
        for item in contents:
            # Index = an item in the bag
            # Get an item in bag that is equal to or more than the item in the leftover bag
            if calculateWeight(item) >= calculateWeight(add_item):
                # remove item from bag
                temp_bag.remove(item)
                # add item to leftover
                temp_leftovers.append(item)
                # remove new random item from leftover
                temp_leftovers.remove(add_item)
                # add new random item to bag
                temp_bag.append(add_item)
                # Break out of loop when item to swap has been found
                swapped_item == True
                # print(temp_bag)
                return temp_bag
            else:
                continue  
            
        # If weight <= remove_item weight 
        # Can be used to swap!
        # If not get a new random item



########### Step 3: Calculate acceptance probablity ########### 

###########  CONFIGURATIONS  ###########

# Maximimum temperature it starts at 
current_temp = 70
# Minimum temperature it stops at 
temp_min = 0
# The rate of reduction
alpha = 0.9


def acceptanceProbability(current, new):
    # Calculate the acceptance probability
    difference = -(current-new)
    accepted = math.exp(difference/current_temp)
    return accepted


########### Step 4: Pick best solution based on value; if worse then use acceptance probablity to pick ########### 

best_solution = bag_contents

# Pick the best solution based on higher value but also take acceptance probability into account
def pickBest(solution, iterations):
    global current_temp
    
    best_value = calculateTotalValue(solution)
    count = 0
    while count < iterations:
        new_solution = swap(bag_contents, bag_leftovers)
        new_value = calculateTotalValue(new_solution)
        
        # If the total value of the new solution is MORE than the current total value of the best solution then add as new solution!
        if new_value > best_value:
            best_value = new_value
            # print("1",new_solution)
        else:
            # Calculate the acceptance probability of current and new solution values
            new_probability = acceptanceProbability(best_value, new_value)
            # Generate random number between 0 and 1 
            random_number = random.uniform(0,1)
            # If random number < probability = accept move and change to best_route
            if random_number < new_probability:
                best_route = new_solution
                # print(new_probability)
                
            # If we have run through all iterations
        if count == iterations:
            # Then we should reduce temperature
            current_temp = current_temp * alpha
            print("Solution no.", count+1)
            # And reset the counter 
            count = 0
            # print("test")
        else:
            print("Solution no.", count+1)
            count += 1
            # print("test 2")
        
        print("The best solution:", best_solution)
        print("Value:", calculateTotalValue(best_solution))
        print("Weight:", calculateTotalWeight(best_solution), "\n")
        
    
########### Testing stuff out ###########


print("Start solution: ", bag_contents)        
print("Items leftover: ", bag_leftovers)     
print("Start weight: ", bag_weight, "Start value: ", bag_value)

pickBest(bag_contents,0)


