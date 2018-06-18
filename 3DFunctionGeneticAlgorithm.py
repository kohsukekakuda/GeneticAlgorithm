# coding: utf-8

import random
import math
import pylab
import sys
import numpy
from mpl_toolkits.mplot3d import Axes3D

gene_length = 1
individual_length = 100
generation = 1000
mutate_rate = 0.05
elite_rate = 0.2

def get_population():
    population = []
    for i in xrange(individual_length):
        population_list = []
        for j in xrange(gene_length):
            population_list.append((random.uniform(-10000, 10000.),
                                    random.uniform(-10000., 10000.)))
        population.append((f(population_list[0][0], population_list[0][1]), population_list))
    return population

def f(x, y):
    #return ((y+numpy.sqrt(y**2.+4.*x**2.))/2.-5.)**2.
    #return ((x-3)**2) + y**2
    #return 100 * (numpy.exp(-(((x+30)**2) + ((y+30)**2))/400.) - numpy.exp(-(((x-30)**2) + ((y-30)**2))/400.))
    #return 50 * numpy.cos((x*y)/2000)
    #return ((1 - x)**2) + 100*((y - x**2)**2)
    #return ((x**2 + y -11)**2) + (x + y**2 -7)**2
    #return (x**2) + (y**2) + x*numpy.sin(y) + y*numpy.sin(x)
    #return (x**2) + (y**2)
    return numpy.sin(numpy.sqrt((x**2) + (y**2))) / numpy.sqrt((x**2) + (y**2))
    #return numpy.log(1 + (abs(x+y))**(2 + numpy.sin(x+y)))

def evaluate(pop):
    pop.sort()
    return pop

def crossover(parent):
    a = []
    mx = random.uniform(min(parent)[1][0][0], max(parent)[1][0][0])
    my = random.uniform(min(parent)[1][0][1], max(parent)[1][0][1])
    #print "X"
    a.append((mx, my))
    return a

def mutate(parent):
    a = []
    if random.random() <= 0.5:
        mx = (1. / random.uniform(min(parent)[1][0][0], max(parent)[1][0][0])) ** 2
        my = (1. / random.uniform(min(parent)[1][0][1], max(parent)[1][0][1])) ** 2
        #print "a"
    elif random.random() <= 0.5:
        mx = -(1. / random.uniform(min(parent)[1][0][0], max(parent)[1][0][0])) ** 2
        my = -(1. / random.uniform(min(parent)[1][0][1], max(parent)[1][0][1])) ** 2
        #print "b"
    elif random.random() <= 0.5:
        mx = 2. * ((random.uniform(min(parent)[1][0][0], max(parent)[1][0][0]))
                - ((1. / random.uniform(min(parent)[1][0][0], max(parent)[1][0][0])) ** 2))
        my = 2. * ((random.uniform(min(parent)[1][0][1], max(parent)[1][0][1]))
                - ((1. / random.uniform(min(parent)[1][0][1], max(parent)[1][0][1])) ** 2))
        #print "c"
    else: #random.random() <= 0.5:
        mx = -2. * ((random.uniform(min(parent)[1][0][0], max(parent)[1][0][0]))
                - ((1. / random.uniform(min(parent)[1][0][0], max(parent)[1][0][0])) ** 2))
        my = -2. * ((random.uniform(min(parent)[1][0][1], max(parent)[1][0][1]))
                - ((1. / random.uniform(min(parent)[1][0][1], max(parent)[1][0][1])) ** 2))
        #print "d"
    #mx = -1. / random.uniform(min(parent)[1][0][0], max(parent)[1][0][0])
    #my = -1. / random.uniform(min(parent)[1][0][1], max(parent)[1][0][1])
    a.append((mx ,my))
    return a

def main():
    pop = []
    for p in get_population():
        pop.append(p)
    print 'Generation: 0'
    #print pop
    print '(Min-x, Min-y, Min-z) = (%f, %f, %f)' % (evaluate(pop)[0][1][0][0], evaluate(pop)[0][1][0][1], evaluate(pop)[0][0]) 
    #print evaluate(pop)
    print '-------------------------------------------------------------'
    for g in xrange(generation):
        print 'Generation: ' + str(g + 1)
        eva = evaluate(pop)
        elites = eva[:int(len(pop) * elite_rate)]
        pop = elites
        while len(pop) <= individual_length:
            if random.random() <= mutate_rate:
                m = mutate(pop)
                pop.append((f(m[0][0], m[0][1]), m))
                #print pop, "mutate"
            else:
                m = crossover(pop)
                pop.append((f(m[0][0], m[0][1]), m))
                #print pop, "crossover"
        eva = evaluate(pop)
        pop = eva
        print '(Min-x, Min-y, Min-z) = (%f, %f, %f)' % (evaluate(pop)[0][1][0][0], evaluate(pop)[0][1][0][1], evaluate(pop)[0][0]) 
        #print evaluate(pop)
        print '-------------------------------------------------------------'

    eps = 1e-10
    dx, dy = 0.5, 0.5
    x, y = numpy.mgrid[slice(-100, 100, dx),
                       slice(-100, 100, dy)]
    z = f(x + eps, y + eps)
    pylab.xlabel("x")
    pylab.ylabel("y")
    pylab.pcolor(x, y, z)
    ax=pylab.colorbar()
    ax.set_label("f(x, y)")
    pylab.plot(evaluate(pop)[0][1][0][0], evaluate(pop)[0][1][0][1], "o", color="r")
    pylab.savefig("3DFunctionGA_ColorMap.png")
    pylab.clf()
    
    x1 = numpy.arange(-100, 100, 0.5)
    y1 = numpy.arange(-100, 100, 0.5)
    X, Y = numpy.meshgrid(x1, y1)
    Z = f(X + eps, Y + eps)
    fig = pylab.figure()
    ax1 = Axes3D(fig)
    ax1.plot_surface(X, Y, Z)
    ax1.set_xlim([-100, 100])
    ax1.set_ylim([-100, 100])
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    ax1.set_zlabel("f(x, y)")
    ax1.scatter(evaluate(pop)[0][1][0][0], evaluate(pop)[0][1][0][1], evaluate(pop)[0][0], "o", color="r")
    #pylab.show()
    pylab.savefig("3DFunctionGA_SurfacePlot.png")
    
if __name__ == '__main__':
    main()
