
from bird import Bird
from neural_network import NeuralNetwork
from logger import get_logger
from random import random
import numpy as np

logger = get_logger('Population')

class Population:
    def __init__(self, popSize=10):
        self.popSize = popSize
        self.halfSize = popSize // 2
        self.quarterSize = popSize // 4
        self.alive = None
        self.dead = None
        self.counter = 0

    def nextGeneration(self):
        self.counter += 1
        dead = self.dead
        nextGen = []
        if(dead):
            dead[-1].save('gen' + str(self.counter))
            winners = dead[-self.quarterSize:]
            weights = [b.score for b in winners]
            weightSum = sum(weights)
            logger.info('Best Quarter Score avg: %f', weightSum/self.quarterSize)
            logger.info('Scores: %s', str(weights))
            logger.info('Generation %d', self.counter)
            weights = [w/weightSum for w in weights]
            winners = [b.brain for b in winners]
            dead = [b.brain for b in dead]

            # reproduce winners
            zipper = zip(np.random.choice(winners, size=self.quarterSize, p=weights), np.random.choice(winners, size=self.quarterSize, p=weights))
            for mom, dad in zipper:
                child1, child2 = mom.crossover(dad)
                child1.mutate()
                child2.mutate()
                nextGen.append(Bird(child1))
                nextGen.append(Bird(child2))

            # will leave space for 10% new genomes
            fourtyPerc = self.popSize // 5
            zipper = zip(np.random.choice(dead, size=fourtyPerc), np.random.choice(dead, size=fourtyPerc))
            for mom, dad in zipper:
                child1, child2 = mom.crossover(dad)
                child1.mutate()
                child2.mutate()
                nextGen.append(Bird(child1))
                nextGen.append(Bird(child2))
        
        for i in range(self.popSize - len(nextGen)):
            nextGen.append(Bird())

        self.alive = nextGen
        self.dead = []

    def kill(self, bird: Bird):
        self.alive.remove(bird)
        self.dead.append(bird)

    def hasAlive(self) -> bool:
        return (len(self.alive) > 0)
