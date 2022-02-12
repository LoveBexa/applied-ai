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

# Inde start from 1 rather than 0 i.e Item 1 to 100
data_true.index += 1 

########### Knapsack Bag Initialisations ########### 

bag_weight = 0
bag_value = 0
bag_contents = []
bag_leftovers = []
bag_capacity = 1500 


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
            
 
########### Step 1: Initial Solution: Random start ########### 

# List items 1 to 100
items = random.sample(range(1, 101), 100)
bag_leftovers = items.copy()
    
# While bag weight is less than bag capacity 
tried_items = []



while bag_weight < bag_capacity:
    
    # Grab a random item from the leftover bag
    random_item = random.choice(bag_leftovers)
    random_item_weight = calculateWeight(random_item)
    # If the random item grabbed from leftover bag and the current bag weight is less than max. capcity
    # Also if the new random item ISNT in already tried items
    if ((random_item_weight + bag_weight) <= bag_capacity) & (random_item not in tried_items):
        # Add it!
        bag_contents.append(random_item)
        # Remove it from the leftover bag
        bag_leftovers.remove(random_item)
        # Update the bag weight
        bag_weight += random_item_weight
        tried_items.append(random_item)
    # If the new random item isn't in tried items BUT is over max capcity
    elif(random_item not in tried_items):
        # Add to tried items
        tried_items.append(random_item)
        continue
    else:
        # If items are already in tried_items then escape the loop
        break


########### Step 2: Neighbourhood operator: random swap each item from leftovers with a random bag item ########### 


def swap(contents, leftovers):
    
    # For this neighbourhood operator I want to random swap the items len(leftover) times to cover bags that have contained every single of the items
    # In order to do so we need to be able to ensure the bags are < 1500kg maximum weight
    # Once the item in leftover bag has been swapped it should be popped from the leftovers
    
    temp_bag = contents.copy()
    temp_leftovers = leftovers.copy()
    temp_neighbours = []
    # Once item found to swap change to true
    swapped_item = False
    
    while swapped_item == False:
        # Get item from leftover bag
        add_item = random.choice(temp_leftovers)
        
        # Random item from current bag
        remove_item = random.choice(temp_bag)
        
        # Whats the current bag's weight without the current item?
        bag_without_item = calculateTotalWeight(temp_bag) - calculateWeight(remove_item)
            
        # New random item taken from left over bag's value is more than current item's value
        # And the total weight of the new item and the bag(without the item we want to remove) is less than total bag capacity then we can swap!
        if (bag_without_item + calculateWeight(add_item) <= bag_capacity):
            # remove item from bag
            temp_bag.remove(remove_item)
            # add item to neighbour
            temp_leftovers.append(remove_item)
            # remove new random item from leftover
            temp_leftovers.remove(add_item)
            # add new random item to bag
            temp_bag.append(add_item)
            # Break out of loop when item to swap has been found
            swapped_item == True
            # print(temp_bag)
            return temp_bag
        else: # If new item isn't better value than existing then return existing
            return temp_bag
            



########### Step 3: Calculate acceptance probablity ########### 

###########  CONFIGURATIONS  ###########

# Maximimum temperature it starts at 
current_temp = 50
# Minimum temperature it stops at 
temp_min = 0.005
# The rate of reduction
alpha = 0.7

iterations = 10

def acceptanceProbability(current, new):
    # Calculate the acceptance probability
    difference = -(current-new)
    accepted = math.exp(difference/current_temp)
    return accepted


########### Step 4: Pick best solution based on value; if worse then use acceptance probablity to pick ########### 

best_solution = bag_contents

# Pick the best solution based on higher value but also take acceptance probability into account
def pickBest(solution):
    global current_temp, best_solution
    # Append all solutions to this dict 
    solution = {"Value": [], "Weight": [],  "Solution": [] }
    best_value = calculateTotalValue(best_solution)
    
    
    count = 0
    # Iterations is how many iterations needed per temp level 
    while temp_min < current_temp:

        # print("Current temp:", current_temp)
        # print("Min temp:", temp_min)
        
        
        new_solution = swap(bag_contents, bag_leftovers)
        new_value = calculateTotalValue(new_solution)
        
        
        ####### STOPPING CRITERIA #######
        if current_temp <= temp_min:
            break

        # If the total value of the new solution is MORE than the current total value of the best solution then add as new solution!
        if new_value > best_value:
            best_solution = new_solution
            # print("1",new_solution)
        else:
            # Calculate the acceptance probability of current and new solution values
            new_probability = acceptanceProbability(best_value, new_value)
            # Generate random number between 0 and 1 
            random_number = random.uniform(0,1)
            # If random number < probability = accept move and change to best_route
            if random_number < new_probability:
                best_solution = new_solution
                # print(new_probability)
                
            # If we have run through all iterations
        if count == iterations:
            # Then we should reduce temperature
            current_temp = current_temp * alpha
            # But is the current temp goes BELOW minimum temp we should break out
            if current_temp <= temp_min:
                
             # if count == iterations then reset the counter
                # print("Current temp:", current_temp)
                # print("Min temp:", temp_min)
                # print("Solution no.", count+1)
                # And reset the counter 
                break
            count = 0
                # print("test")
        else:
            # print("Solution no.", count+1)
            count += 1
            # print("test 2")
            
        best_solution = best_solution
        
        solution["Value"].append(calculateTotalValue(best_solution))
        solution["Weight"].append(calculateTotalWeight(best_solution))
        solution["Solution"].append(best_solution)
        
    return solution
        
    
########### Testing stuff out ###########


# print("Start solution: ", bag_contents)        
# print("Items leftover: ", bag_leftovers)     

bag_weight = calculateTotalWeight(bag_contents)
bag_value = calculateTotalValue(bag_contents)

# print("Start weight: ", bag_weight, "Start value: ", bag_value)

best_dict = pickBest(bag_contents)
best_df = pd.DataFrame.from_dict(best_dict)

print(best_df)
# Export to CSV
best_df.to_csv(r'knapsack-sim-annealing.csv')