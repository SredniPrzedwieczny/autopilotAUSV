import random
from operator import attrgetter

from deap import base
from deap import creator
from deap import tools
from scipy.spatial import distance

import detobst
import spline

global obsts, start, stop, movObsts

mySpeed = 1

def xyToPoints(x,y):
    points = []
    for i in range(x.__len__()):
        points.append([x[i],y[i]])
    return points

def arrayToPoints(arr):
    points = []
    for i in range(0, arr.__len__(), 2):
        points.append([arr[i],arr[i+1]])
    return points

def evalOneMax(individual):
    points = [start]
    points.extend(arrayToPoints(individual))
    points.append(stop)
    x,y = spline.spline_pts(points)
    points = xyToPoints(x,y)
    dst = 0
    lastPt = points[0]
    for point in points:
        dst += distance.euclidean(lastPt, point)
        lastPt = point
    dst += detobst.det_valid(points, obsts, movObsts, mySpeed)
    return dst,

def randomNumber():
    return random.random() * 0.01

def evolutionAlgorithm(obstNum):
    N = obstNum
    IND_SIZE=N


    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)
    toolbox = base.Toolbox()
    # Attribute generator
    toolbox.register("attr_float", randomNumber)
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual,
        toolbox.attr_float, n=N*2)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    CXPB = 0.6
    MUTPB = 0.1



    toolbox.register("evaluate", evalOneMax)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)


    pop = toolbox.population(n=round((obstNum/2+1)*100))
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]
    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while g < N*10:
        # A new generation
        g = g + 1
        # print("-- Generation %i --" % g)
        # Select the next generation individuals
        if min(fits) < 100:
            offspring = toolbox.select(pop, max(round(len(pop)*0.8), 20))
        else:
            offspring = toolbox.select(pop, max(round(len(pop)), 20))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))
        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        pop[:] = offspring
        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(pop, key=attrgetter("fitness")))
    points = [start]
    points.extend(arrayToPoints(max(pop, key=attrgetter("fitness"))))
    points.append(stop)
    return spline.spline_pts(points)