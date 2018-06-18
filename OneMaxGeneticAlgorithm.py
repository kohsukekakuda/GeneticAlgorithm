# coding: utf-8

import random
import copy
import pylab
import numpy

# パラメータ
gene_length = 1000 # 遺伝子長
individual_length = 100 # 個体数
generation = 1000 # 世代数
mutate_rate = 0.1 # 突然変異の確率
elite_rate = 0.2 # エリート選択の割合

def get_population():
    population = []
    for i in xrange(individual_length):
        population_list = []
        for j in xrange(gene_length):
            population_list.append(random.randint(0, 1))
        population.append(population_list)
    return population

def fitness(pop): # 適応度
    return sum(pop)

def evaluate(pop): #　適応度が高い順に評価
    pop.sort(reverse=True)
    return pop

def one_point_crossover(parent1, parent2): # 1点交叉法
    r1 = random.randint(0, gene_length - 1)
    child = copy.deepcopy(parent1)
    child[0:r1] = parent2[0:r1]
    return child

def two_point_crossover(parent1, parent2): # 2点交叉法
    r1 = random.randint(0, gene_length - 1)
    r2 = random.randint(r1, gene_length - 1)
    child = copy.deepcopy(parent1)
    child[r1:r2] = parent2[r1:r2]
    return child

def uniform_point_crossover(parent1, parent2): # 一様交叉法
    child = copy.deepcopy(parent1)
    for i in xrange(len(parent1)):
        if random.random() < 0.50:
            child[i] = parent2[i]
    return child

def mutate(parent): # 突然変異
    r = random.randint(0, gene_length - 1)
    child = copy.deepcopy(parent)
    if child[r] == 0:
        child[r] = 1
    else:
        child[r] = 0
    return child

def main():
    pop = []
    g_list = []
    ave = []
    # 初期個体生成
    for p in get_population():
        pop.append((fitness(p), p))
    pop.sort(reverse=True)
    ave.append(pop[0][0] / float(gene_length))
    print 'Generation: 0'
    print 'Min : %d' % ((pop[-1][0]))
    print 'Max : %d' % ((pop[0][0]))
    print '--------------------------'
    
    for g in xrange(generation):
        print 'Generation: ' + str(g + 1)

        # エリートを選択
        eva = evaluate(pop)
        elites = eva[:int(len(pop) * elite_rate)]
        #print pop

        # 突然変異、交叉
        pop = elites
        while len(pop) <= individual_length: # <= ?
            if random.random() < mutate_rate:
                m = random.randint(0, len(elites) - 1)
                child = mutate(elites[m][1])
                #print pop, "mutate"
                pop.append((fitness(child), child))
            else:
                m1 = random.randint(0, len(elites)-1)
                m2 = random.randint(0, len(elites)-1)
                # 交叉法を選ぶ
                child = uniform_point_crossover(elites[m1][1], elites[m2][1])
                #print pop, "crossover"
                pop.append((fitness(child), child))

        # 評価
        eva = evaluate(pop)
        pop = eva

        print 'Min : %d' % ((pop[-1][0]))
        print 'Max : %d' % ((pop[0][0]))
        print '--------------------------'

        g_list.append(g + 1)
        ave.append(pop[0][0] / float(gene_length))
    #print g_list
    #print ave
    hoge = zip(g_list, ave)
    print 'Result : %s%s' % ((pop[0])) 

    pylab.plot(ave, "-")
    pylab.yticks(numpy.arange(0., 1.11, 0.1))
    pylab.xticks(numpy.arange(0., g_list[-1] + 1., 10.))
    pylab.ylabel("Propotion")
    pylab.xlabel("Generation")
    pylab.grid()
    pylab.savefig("OneMaxGA.png")

if __name__ == '__main__':
    main()
