import random, timeit
from tabnanny import check

# Calculate run time of the program
start = timeit.default_timer()

############## Calculate total weight of genome ##############

# This function calculates the total weight of the entire genome
# By iterating through each item to check if it's a 1 or 0
# If it is 1 then it checks the weight in the array
# Totals this up and returns as valuez
# weight = [3, 9, 5, 6]

def calculateWeight(genome):
    total_weight = 0
    counter = 0
    # Iterate through each item in the genome
    for key, bit in enumerate(genome):
        if bit == 0:
            continue
        else:
            total_weight += weight[key]
        counter += 1
    return total_weight

############## First generate an initial population of genome ##############

# Generates an entire population of genomes 
# By calling the genome function to randomly create a set
# Loops through genome creation until size of population met

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
# If weight is same or under max_weight then return weight as the fitness value

def checkFitness(genome):
    weight = calculateWeight(genome)
    return weight if weight <= max_weight else 0


############## Selection Function ##############
# We want to pick 2 genomes randomly to battle out
# Find the winner
# Then do this again
# Then these two winners are selected! 

def selectionTourney(population):
    new_parents = {}
    counter = 0
    while counter < 2:
        # Pick genome 1 at random
        genome_one = random.randint(0, len(population)-1)
        # Pick genome 2 at random
        genome_two = random.randint(0, len(population)-1)
        # Get the fitness of each genome from the total weight (if it's over limit then its 0)
        fitness_one = checkFitness(list(population.items())[genome_one][1])
        fitness_two = checkFitness(list(population.items())[genome_two][1])        
        # Fittest genome gets added to the winners pot!
        if fitness_one > fitness_two:
            new_parents[counter] = population[genome_one]
        else: 
            new_parents[counter] = population[genome_two]
        counter += 1
        
    # Returns 2 winners as a dict
    return new_parents

############## Crossover Function ##############

# Note: to access first item in a list[0][0] to access second item in first item[0][1]
# We want to find a random point in the genome
# Cut in half at same point for both parents
# Swap 2nd half
# Produce new child! 

def crossover(parents):
    # Split parents out
    parent_one = parents[0]
    parent_two = parents[1]
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
    # Mutation rate should be between 0.005 - 0.01
    mutation_rate = 0.05#
    # Iterate through each bit
    for i in range(len(children)):
        for j in range(len(children[i])):
            # Generate a random number between 0 to 1 for bit 
            bit_rate = random.uniform(0,1)
            # print(mutation_rate, bit_rate)
            # If bit rate is less than mutation rate then we flip the bit
            if mutation_rate > bit_rate:
                if children[i][j] == 1:
                    children[i][j] = 0
                    # print("0", children[i][j])
                else:
                    children[i][j] = 1
                    # print("1", children[i][j])                  
    return children


############## Calculate Average Fitness and Best Fitness of a Population ##############
# This function returns the average fitness of each generation
# Also the fittest genome out of the poulation 

def fitnessStatistics(population):
    
    total_fitness = 0
    fittest_genome = [0,0,0,0]
 
    # Find the fitness of each in population
    for genome in population.values():
        # Check the fittest genome
        if checkFitness(genome) > checkFitness(fittest_genome):
            fittest_genome = genome
        # Add to total fitness
        total_fitness += checkFitness(genome)
    print("Average fitness:", total_fitness/len(population))
    print("Fittest Genome:", fittest_genome, "Fitness:", checkFitness(fittest_genome))

############## Testing Station ##############

# This function generates a population the size of input amount
# Goes through GA stages
# We also want to keep generating a new population until optima solution is found
# 
def createPopulation(population, size):
    
    new_population = {}
    count = 0
    # Find fittest parents from tournement 
    while count < size:   
        parents = selectionTourney(population)
        #print(parents)
        # Remove fittest parents from population
        # Create cross child genomes 
        children = crossover(parents)
        #print(children)
        # Build a new population 
        mutated = mutation(children)
        # Add the new children to the dict
        new_population[count] = mutated[0]
        new_population[count+1] = mutated[1]
        count += 2
    # print(new_population)
    return new_population
    
# If we have a max generations we run through
# We can create populations to the max num of generations based on previous populations and fittest#
# With each iteratino the population should get fotter 
# We want to calculate the average fitness and the BEST fitness from each population
# And look through each population and stop the search once the local optima has been found

def geneticAlgorithm(size, generations):
    
    # Create initial population
    next_population = generatePopulation(size)
    print("Initial population:", next_population)

    # Initialise generation counter
    counter = 0
    found_optima = False
    while counter < generations:
        # create population from previous population
        next_population = createPopulation(next_population, size)
        print("Generation",counter+1,":", next_population)
        fitnessStatistics(next_population)
        # Iterate through the genomes of each population
        for genome in next_population.values():
            # print(genome)
            # If that genome is the optima
            if checkFitness(genome) == max_weight:
                # Then return this solution and break out the optima
                print("Optima found after", counter+1, "generations")
                found_optima = True
                break
        if found_optima == True:
            break
        print("It did not find Optima")
        counter += 1
    
        
        

############## Knapsack initialisation ##############

# We want to use GA to find a solution to the Knapsack problem

items = ["A", "B", "C", "D", "E", "F", "G", "H"]
weight = [3, 9, 5, 6, 2, 1, 7, 8]
max_weight = 27

    
############## Checking through each weight ##############

# First number is total genomes in population
# Second number is the number of generations we want to create
geneticAlgorithm(10, 100)


############## Compute run time of the program ##############

stop = timeit.default_timer()
print('Run time: ', stop - start)  
