import random
from copy import deepcopy

# We want to use GA to find a solution to the Knapsack problem

############## Knapsack initialisation ##############
items = ["A", "B", "C", "D"]
weight = [3, 9, 5, 6]
max_weight = 18

############## Calculate total weight of genome ##############
def calculateWeight(genome):
    total_weight = 0
    # Iterate through each item in the genome
    for key, each in enumerate(genome):
        # If it is 1 then it is in the bag
        if each == 1:
            # Add up weight of item 
            total_weight += weight[key]
    return total_weight

############## First generate a population of genome ##############
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
# Must be less than total bag weight 18

def checkFitness(weight):
    # If weight is large than max_weight then we will discard
    if weight > max_weight:
        return 0
    else:
        return 1

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

def crossover(parents):
    # Randomly selects an int between 2 and the length of genome
    # Takes first half of genome 1 
    # Takes second half of genome 2
    # Makes a new genome
    # Takes second half of genome 1
    # Takes first half of genome 2
    # Makes a new genome
    # Returns 2 child genomes as a new solution! 


############## Testing Station ##############


population = generatePopulation(10)
print(population)
for key, value in population.items():
    print(key, "weight =", calculateWeight(value))
    if checkFitness(calculateWeight(value)) == 0:
        print("OVERWEIGHT")
    else:
        print("UNDERWEIGHT")

hehe = selectionTourney(population)
print(hehe)