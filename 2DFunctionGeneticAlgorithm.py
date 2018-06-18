# coding: utf-8

import random
import math
import pylab
import numpy

gene_length = 1
individual_length = 100
generation = 100
mutate_rate = 0.05
elite_rate = 0.2

def get_population():
    population = []
    for i in xrange(individual_length):
        population_list = []
        for j in xrange(gene_length):
            population_list.append(random.uniform(-10000., 10000.))
        population.append((f(population_list[0]), population_list))
    return population

def f(x):
    #return x**2
    #return x / ((x**2.) + 1.)
    #return x*math.exp(x)
    #return math.exp(-x) * math.sin(x)
    #return (math.exp(x) + math.exp(-x)) / 2.
    #return (3*x**4) + (4*x**3) - (12*x**2) + 16
    #return math.sin(x) / x
    return numpy.log(1 + (abs(x))**(2+numpy.sin(x)))

def evaluate(pop):
    pop.sort()
    return pop

def crossover(parent):
    a = []
    m = random.uniform(min(parent)[1][0], max(parent)[1][0])
    a.append(m)
    return a

def mutate(parent):
    a = []
    if random.random() <= 0.5:
        m = (1. / random.uniform(min(parent)[1][0], max(parent)[1][0])) ** 2
    elif random.random() <= 0.5:
        m = -(1. / random.uniform(min(parent)[1][0], max(parent)[1][0])) ** 2
    elif random.random() <= 0.5:
        m = 2. * ((random.uniform(min(parent)[1][0], max(parent)[1][0]))
               - ((1. / random.uniform(min(parent)[1][0], max(parent)[1][0])) ** 2))
    else:
        m = -2. * ((random.uniform(min(parent)[1][0], max(parent)[1][0]))
                - ((1. / random.uniform(min(parent)[1][0], max(parent)[1][0])) ** 2))
    #m = -1. / random.uniform(min(parent)[1][0], max(parent)[1][0])
    a.append(m)
    return a

def main():
    pop = []
    for p in get_population():
        pop.append(p)
    print 'Generation: 0'
    #print pop
    print '(Min-x, Min-y) = (%f, %f)' % (evaluate(pop)[0][1][0], evaluate(pop)[0][0]) 
    #print evaluate(pop)
    print '-----------------------------------------'
    for g in xrange(generation):
        print 'Generation: ' + str(g + 1)
        eva = evaluate(pop)
        elites = eva[:int(len(pop) * elite_rate)]
        pop = elites
        while len(pop) < individual_length:
            if random.random() <= mutate_rate:
                m = mutate(pop)
                pop.append((f(m[0]), m))
                #print pop, "mutate"
            else:
                m = crossover(pop)
                pop.append((f(m[0]), m))
                #print pop, "crossover"
        eva = evaluate(pop)
        pop = eva
        print '(Min-x, Min-y) = (%f, %f)' % (evaluate(pop)[0][1][0], evaluate(pop)[0][0])
        #print evaluate(pop)
        print '-----------------------------------------'
        
    x = []
    y = []
    eps = 1e-10
    for i in xrange(-1000, 1000):
        if i == 0:
            i = eps
        x.append(i * 0.1)
        y.append(f(i * 0.1))
    pylab.xlabel("x")
    pylab.ylabel("y")
    pylab.plot(x, y, "-")
    pylab.plot(evaluate(pop)[0][1][0], evaluate(pop)[0][0], "o", color="r")
    pylab.grid()
    pylab.savefig("2DFunctionGA.png")
    
if __name__ == '__main__':
    main()
