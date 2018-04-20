
from bird import Bird
from neural_network import NeuralNetwork
from random import choices, random
import numpy as np

class Population:
    def __init__(self, popSize=10):
        self.popSize = popSize
        self.alive = None
        self.dead = None
        self.counter = 0

    def nextGeneration(self):
        self.counter += 1
        print('Generation', self.counter)
        dead = self.dead
        nextGen = []
        if(dead):
            weights = list(map((lambda b: b.score), dead))
            dead = list(map((lambda b: b.brain), dead))

            for i in range(self.popSize//2 - self.popSize//10):
                mom, dad = choices(dead, weights=weights, k=2)
                child1, child2 = mom.crossover(dad)
                child1.mutate()
                child2.mutate()
                nextGen.append(Bird(child1))
                nextGen.append(Bird(child2))

            for i in range(self.popSize - len(nextGen)):
                nextGen.append(Bird())
        else:
            for i in range(self.popSize):
                nextGen.append(Bird())
        
        self.alive = nextGen
        self.dead = []

    def kill(self, bird: Bird):
        self.alive.remove(bird)
        self.dead.append(bird)

    def hasAlive(self) -> bool:
        return (len(self.alive) > 0)
