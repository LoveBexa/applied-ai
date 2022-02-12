import pandas as pd
import random

########### Convert CSV to DataFrame ########### 

# Show full width and height of dataframe
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', None)

# Converting csv to data frame. Total weight of items = 2621kg

data = pd.read_csv("knapsack.csv")
# Find "true weight" ratio of each item; values divided by weights
data_true = data
data_true["true value"] = data_true["values"] / data_true["weights"]

# Index starts from 0 so added 1 to start from 1 = item 1
data_true.index += 1


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
    total_items = items
    leftovers = [i for i in total_items if i not in current_bag]
    return leftovers

########### Knapsack Bag Initialisations ########### 

bag_weight = 0
bag_value = 0

bag_contents = []
bag_leftovers = [] 

bag_capacity = 1500 

########### Random Start ###########


# Create a random list of numbers between 1-100
random_list = random.sample(range(1, 101), 100)

# Go through each one if item value + bag weight is less than capacity add
for item in random_list:
    if (bag_weight + calculateWeight(item) <= bag_capacity):
        bag_weight += calculateWeight(item)
        bag_contents.append(item)
    else:
        bag_leftovers.append(item)

bag_value = calculateTotalValue(bag_contents)
start_solution = {"Value": bag_value,"Weight": bag_weight,"Solution": bag_contents }
print("Start Solution:\n",start_solution)
print("Start Leftovers:\n",bag_leftovers)

# Item list 1-100
items = random.sample(range(1, 101), 100)

# These items were generated using commented out random start script above
# Reason why it's hardcoded is to ensure the rest of the test uses the same items to help compare


# bag_contents = [66, 34, 67, 84, 83, 13, 74, 98, 50, 31, 89, 2, 12, 68, 65, 96, 93, 25, 40, 78, 59, 15, 55, 19, 62, 75, 9, 35, 37, 48, 79, 87, 82, 20, 28, 72, 45, 77, 38, 23, 32, 85, 70, 42, 10, 54, 90, 44, 58, 56, 94, 41, 92, 8, 1, 5, 69, 29, 46]
bag_leftovers =  leftovers(bag_contents)


bag_weight = calculateTotalWeight(bag_contents)
bag_value = calculateTotalValue(bag_contents)

print("Starting weight:", bag_weight)
print("Starting value:", bag_value)
print("Starting bag:",bag_contents)
print("Starting leftovers:",bag_leftovers)

########### Swap items from bag with leftover bag ###########

best_solution = bag_contents

def swap(bag):
    # Deep copy array
    bag_copy = bag.copy()
    leftover_copy = leftovers(bag).copy()
    # Grab random item from current bag
    random_bag = random.choice(bag_copy)
    # Grab a random item from the leftover bag
    random_leftover = random.choice(leftover_copy)
    # Remove and add new item
    bag_copy.remove(random_bag)
    bag_copy.append(random_leftover)
    # Remove it from the leftover bag
    leftover_copy.remove(random_leftover)  
    
    return bag_copy
        
def steepestHill(bag):
    
    global best_solution
    
    counter = 0
    # Deep copy arrays into new ones
    best_bag = bag
    temp_leftovers = leftovers(bag)
    # The total swaps number = the amount of items in the leftover bag
    total_swaps = len(temp_leftovers)
    
    while counter < total_swaps:
        # Swap items in leftover and current bag!
        temp_bag = swap(best_bag)  
        # If the new bag value is bigger than the current bag value and it is under the max weight limit then use as best solution!
        if (calculateTotalValue(best_bag) < calculateTotalValue(temp_bag)) and (calculateTotalWeight(temp_bag) <= bag_capacity):
            best_bag = temp_bag
            #print("Update to best:", calculateTotalValue(best_bag))
            counter += 1
        else:
            #print("Current solution is better")
            counter += 1
            continue
        
    print("The best overall solution from neighbourhood was:\nValue:", calculateTotalValue(best_bag),"Weight:", calculateTotalWeight(best_bag), "Solution:", best_bag)
    return best_bag


# Iterate over neighbours to find the best!
iterations = 50
# Create a dictionary to append new solutions to (to build graph)
steepest_solutions = {"Value": [],"Weight": [],"Solution": [] }

while iterations > 0:
    best_solution = steepestHill(best_solution)
    steepest_solutions["Value"].append(calculateTotalValue(best_solution))
    steepest_solutions["Weight"].append(calculateTotalWeight(best_solution))
    steepest_solutions["Solution"].append(best_solution)
    iterations -= 1

best_df = pd.DataFrame.from_dict(steepest_solutions)
# Export to CSV
best_df.to_csv(r'knapsack-steepest.csv')