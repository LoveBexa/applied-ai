import random
from copy import deepcopy

# We want to use GA to find a solution to the Knapsack problem

############## Knapsack initialisation ##############
items = ["A", "B", "C", "D", "E", "F"]
weight = [3, 9, 5, 6, 1, 3]
max_weight = 18

############## Calculate total weight of genome ##############

# This function calculates the total weight of the entire genome
# By iterating through each item to check if it's a 1 or 0
# If it is 1 then it checks the weight in the array
# Totals this up and returns as value

def calculateWeight(genome):
    total_weight = 0
    # Iterate through each item in the genome
    for key, each in enumerate(genome):
        # If it is 1 then it is in the bag
        if each == 1:
            # Add up weight of item 
            total_weight += weight[key]
    return total_weight

############## First generate an initial population of genome ##############

# Generates an entire population of genomes 
# By calling the genome function to randomly create a set


def generateGenome(size):
    genome = []
    for number in range(size):
        # randomly generate 0 or 1 and append to array
        genome.append(random.randint(0,1))
    return genome        

############### Generate new population ##############

def generatePopulation(size):
    # Create a dict of population
    population = {}
    # Loop through size
    for number in range(size):
        # Append each generated genome to population dict
        population[number] = generateGenome(len(items))
    # Return population 
    return population
    

############### Fitness Function ##############

# Returns fitness value for each genome
# If weight is large than max_weight then return fitness value 0
# If weight is same or under max_weight then return fitness value of 1

def checkFitness(weight):
    return 1 if weight <= max_weight else 0


############## Selection Function ##############

def selectionTourney(population):
    # Convert dict to a list
    new_population = list(population.items())
    
    # While new_population has more than 2 genomes we'll keep looping through; we want to return the top 2
    while len(new_population) > 2:
        # Randomly select 2 genomes
        genome_one = random.choice(new_population)
        genome_two = random.choice(new_population)
        # If genome one is bigger than genome two
        if calculateWeight(genome_one[1]) > calculateWeight(genome_two[1]):
            # Then genome one wins & we remove genome two!
            new_population.remove(genome_two)
        else: 
            # Then genome two wins & we remove genome one!
            new_population.remove(genome_one)
    # The two leftover are the fittest and will become parents
    return new_population
    

############## Crossover Function ##############

# Note: to access first item in a list[0][0] to access second item in first item[0][1]
# We want to find a random point in the genome
# Cut in half at same point for both parents
# Swap 2nd half
# Produce new child! 

def crossover(parents):
    # Split parents out
    parent_one = parents[0][1]
    parent_two = parents[1][1]
    
    # Randomly selects an int between 2n and the length of genome 
    # I've selected items-1 as counting starts from 0 and we want total length of items in bag
    pointer = random.randint(2,len(items)-1)
    # Takes second half of genome 1 
    p1_tmp = parent_one[pointer:]
    # Takes second half of genome 2
    p2_tmp = parent_two[pointer:]
    # Takes first half of genome 1
    p1_tmp2 = parent_one[:pointer]
    # Takes first half of genome 2
    p2_tmp2 = parent_two[:pointer]
    # Makes a new genome
    p1_tmp2.extend(p2_tmp)
    p2_tmp2.extend(p1_tmp)
    # Append 2 new genomes to results
    result = []
    result.append(p1_tmp2)
    result.append(p2_tmp2)
    # Returns 2 child genomes as a new solution! 
    return result

############## Mutation Function ##############

# We want to 'mutate' aka flip a bit 
# If a problem uses 10 bits, then a good default mutation rate would be (1/10) = 0.10 or a probability of 10 percent.

def mutation(children):
    for i in children:
        for j in i:
            print(j)

############## Testing Station ##############


population = generatePopulation(10)
# Checking through each weight 
for key, value in population.items():
    print(key, "weight =", calculateWeight(value))
    if checkFitness(calculateWeight(value)) == 0:
        print("NO")
    else:
        print("YES")

parents = selectionTourney(population)
print(parents)
children = crossover(parents)
print(children)
new_population = mutation(children)