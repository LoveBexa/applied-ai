from importlib.resources import contents
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

########### Knapsack Bag Initialisations ########### 

bag_weight = 0
bag_value = 0
bag_contents = []
bag_leftovers = []
bag_capacity = 1500 
 
########### Step 1: Initial Solution: Greedy start from higher true value ########### 


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

# Iterate 2nd time through the bag_leftovers again to see if anything can be added 
for item in bag_leftovers:
    # Iterate through dataframe of bag items
    for index, row in data_true.iterrows():
        # If the item in leftover bag is the same as dataframe item (to find the weight and value)
        # And if the weight of that item + current weight is less than maximum capacity
        if (item == index) & (bag_weight + row["weights"] <= bag_capacity):
            # Find the weight of item and add it to bag
            bag_weight += row["weights"]
            bag_value += row["values"] 
            # Add item to the bag_contents 
            bag_contents.append(index)
            # Remove from bag_leftovers
            bag_leftovers.remove(item)



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
    
########### Testing stuff out ###########

calculateWeight(bag_leftovers) 
print("Start solution: ", bag_contents)        
print("Items leftover: ", bag_leftovers)     
print("Start weight: ", bag_weight, "Start value: ", bag_value)

    
########### Step 2: Neighbourhood operator: random swap each item from leftovers with a random bag item ########### 


def swap(contents, leftovers):
    
    # Deep copy bag contents of knapsack and leftovers into temporary bag
    temp_bag = contents.copy()
    temp_leftovers = leftovers.copy()
    
    # Get a random item in bag
    remove_item = random.choice(temp_bag)
    remove_weight = calculateWeight(remove_item)
    # print("Item removed:", remove_item, "Weight: ", remove_weight)
    
    # Iterate through the items in the left overs to swap them in
    for index, item in enumerate(bag_leftovers):
        
        # Create a dictionary to append new values to 
        items_swapped = {}
        
        # If the weight of item from leftover is same or smaller than weight of randomly select bag item
        if calculateWeight(item) <= remove_weight:
            # print("Item added:", item,  "Weight: ", calculateWeight(item))
            # Then remove random item from bag
            temp_bag.remove(remove_item)
            # Add NEW item from left over bag to the bag
            temp_bag.append(item)
            # Remove from leftover bag
            temp_leftovers.remove(item)
            
            # Append new items to dictionary & calculate weight, values etc
            items_swapped["Removed"] = remove_item
            items_swapped["Added"] = item
            items_swapped["Value"] = calculateTotalValue(temp_bag)
            items_swapped["Weight"] = calculateTotalWeight(temp_bag)
            items_swapped["Solution"] = temp_bag
            
            # Print out dict of info for items swapped
            # print(items_swapped)
            # Breaks out of the lopp to return the new bag as a dict
            return items_swapped
        
        
    
    # Calculate new bag


########### Step 3: Show all neighbourhood solutions ########### 

# Create a new function that you can set the iterations for
def steepestAscent(contents, leftovers, iterations):
    
    count = 0
    # Create an empty dataframe with wanted columns
    swapped_df = pd.DataFrame(columns=["Removed", "Added","Value", "Weight", "Solution"])
    
    # Append the FIRST (greedy) solution to Dataframe
    start_items_dict = {"Removed":0,"Added":0,"Value":calculateTotalValue(contents),"Weight":calculateTotalWeight(contents),"Solution":contents};
    swapped_df = swapped_df.append(start_items_dict, ignore_index=True)

    while count < iterations:
        # Creates swapped item dict
        swapped_dict = swap(contents, leftovers)
        # Append dict to a dataframe
        swapped_df = swapped_df.append(swapped_dict, ignore_index=True)
        # Create a new dataframe with only solutions - ready for graphs
        swapped_solutions = swapped_df[["Value", "Solution"]]
        count += 1
        
    # Move index from 0 to 1 for better visual purpose // removed as decided to start the start solution at 0
    # swapped_df.index += 1
    # swapped_solutions.index += 1
    return swapped_df


########### Step 4: Pick the best solution ########### 

solutions = steepestAscent(bag_contents, bag_leftovers, 31)

# Export to CSV
solutions.to_csv(r'knapsack-steepest-ascent.csv')


# Remove solution from dataframe 
best_solution = solutions[["Value", "Solution"]].sort_values(by='Value', ascending=False)
print(best_solution)