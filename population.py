
from bird import Bird
from neural_network import NeuralNetwork
from random import choices, random
from keras import backend as be
import numpy as np

class Population:
    def __init__(self, popSize=10):
        self.popSize = popSize
        self.halfSize = popSize // 2
        self.thirdSize = popSize // 3
        self.alive = None
        self.dead = None
        self.counter = 0

    def nextGeneration(self):
        self.counter += 1
        print('Generation', self.counter)
        dead = self.dead
        nextGen = []
        if(dead):
            dead.sort(key=(lambda b: b.score), reverse=True)
            winners = dead[:self.halfSize // 2]
            weights = list(map((lambda b: b.score), winners))
            winners = list(map((lambda b: b.brain), winners))
            dead = list(map((lambda b: b.brain), dead))

            # reproduce winners
            for i in range(self.halfSize):
                mom, dad = choices(winners, weights=weights, k=2)
                child1, child2 = mom.crossover(dad)
                child1.mutate()
                child2.mutate()
                nextGen.append(Bird(child1))
                nextGen.append(Bird(child2))

            for i in range(self.thirdSize):
                mom, dad = choices(dead, k=2)
                child1, child2 = mom.crossover(dad)
                child1.mutate()
                child2.mutate()
                nextGen.append(Bird(child1))
                nextGen.append(Bird(child2))
        
        # fill remaining slots with new birds
        for i in range(self.popSize - len(nextGen)):
            nextGen.append(Bird())

        self.alive = nextGen
        self.dead = []

    def kill(self, bird: Bird):
        self.alive.remove(bird)
        self.dead.append(bird)

    def hasAlive(self) -> bool:
        return (len(self.alive) > 0)
