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


########### KNAPSACK INITIALISATIONS ########### 

bag_weight = 0
bag_value = 0

bag_contents = []
bag_leftovers = [] 

bag_capacity = 1500 


###########  CONFIGURATIONS  ###########

# Maximimum temperature it starts at 
current_temp = 40
# Minimum temperature it stops at 
temp_min = 0.005
# The rate of reduction
alpha = 0.7
# Iterations per temperature level
iterations = 10



########### Calculate acceptance probablity ########### 

def acceptanceProbability(current, new):
    # Calculate the acceptance probability
    difference = -abs(current-new)
    accepted = math.exp(difference/current_temp)
    return accepted


########### Random Start ###########

# # Create a random list of numbers between 1-100
# random_list = random.sample(range(1, 101), 100)

# # Go through each one if item value + bag weight is less than capacity add
# for item in random_list:
#     if (bag_weight + calculateWeight(item) <= bag_capacity):
#         bag_weight += calculateWeight(item)
#         bag_contents.append(item)
#     else:
#         bag_leftovers.append(item)

# bag_value = calculateTotalValue(bag_contents)
# start_solution = {"Value": bag_value,"Weight": bag_weight,"Solution": bag_contents }
# print("Start Solution:\n",start_solution)
# print("Start Leftovers:\n",bag_leftovers)

# Item list 1-100
items = random.sample(range(1, 101), 100)

# These items were generated using commented out random start script above
# Reason why it's hardcoded is to ensure the rest of the test uses the same items to help compare


bag_contents = [66, 34, 67, 84, 83, 13, 74, 98, 50, 31, 89, 2, 12, 68, 65, 96, 93, 25, 40, 78, 59, 15, 55, 19, 62, 75, 9, 35, 37, 48, 79, 87, 82, 20, 28, 72, 45, 77, 38, 23, 32, 85, 70, 42, 10, 54, 90, 44, 58, 56, 94, 41, 92, 8, 1, 5, 69, 29, 46]
bag_leftovers =  leftovers(bag_contents)

bag_weight = calculateTotalWeight(bag_contents)
bag_value = calculateTotalValue(bag_contents)

print("Starting weight:", bag_weight)
print("Starting value:", bag_value)
print("Starting bag:",bag_contents)
print("Starting leftovers:",bag_leftovers)

########### Pick best solution based on value; if worse then use acceptance probablity to pick ########### 

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

list_solutions = {"Value": [], "Weight": [],  "Solution": [] }
def simulatedAnnealing(bag):
    
    global neighbourhood, best_solution, current_temp
    
    counter = 0
    
    # Deep copy arrays into new ones
    best_bag = bag.copy()
    
    # Iterates through whiles the current temp is bigger than min temp
    while temp_min < current_temp:

        # Swap items in leftover and current bag!
        temp_bag = swap(best_bag)
        # Calculate value of new and old bags
        best_value = calculateTotalValue(best_bag)
        temp_value = calculateTotalValue(temp_bag)
        
    
        ####### STOPPING CRITERIA #######
        if current_temp <= temp_min:
            break
        
        # If the new bag value is bigger than the current bag value and it is under the max weight limit then use as best solution!
        if (best_value < temp_value) and (calculateTotalWeight(temp_bag) <= bag_capacity):
            best_bag = temp_bag
            # print("Best solution is new solution", calculateTotalValue(best_bag))        
        else:
            # Calculate the acceptance probability of current and new solution values
            new_probability = acceptanceProbability(best_value, temp_value)
            # Generate random number between 0 and 1 
            random_number = random.uniform(0,1)
            # If random number < probability = accept move and change to best_route
            if (random_number < new_probability) and (calculateTotalWeight(temp_bag) <= bag_capacity):
                best_bag = temp_bag
        # If we have run through all iterations
        if counter == iterations:
            # Then we should reduce temperature
            current_temp = current_temp * alpha
            # But is the current temp goes BELOW minimum temp we should break out
            if current_temp <= temp_min:
                
             # if count == iterations then reset the counter
                # print("Current temp:", current_temp)
                # print("Min temp:", temp_min)
                # print("Solution no.", counter+1)
                # And reset the counter 
                break
            counter = 0
                # print("test")
        else:
            # print("Solution no.", count+1)
            counter += 1
            # print("test 2")
            
        list_solutions["Value"].append(calculateTotalValue(best_bag))
        list_solutions["Weight"].append(calculateTotalWeight(best_bag))
        list_solutions["Solution"].append(best_bag)
        print("The best solution was:\nValue:", calculateTotalValue(best_bag),"Weight:", calculateTotalWeight(best_bag), "Solution:", best_bag)

    # print("The best overall solution from neighbourhood was:\nValue:", calculateTotalValue(best_bag),"Weight:", calculateTotalWeight(best_bag), "Solution:", best_bag)
    return best_bag
            
        
########### Start the program! ########### 


best_solution = simulatedAnnealing(best_solution)

best_df = pd.DataFrame.from_dict(list_solutions)
print(best_df)

# iterations = 5
# while iterations > 0:
#     best_solution = simulatedAnnealing(best_solution)
#     iterations -= 1

# Export to CSV
best_df.to_csv(r'simulated-static-start.csv')