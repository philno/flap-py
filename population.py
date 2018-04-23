
from bird import Bird
from neural_network import NeuralNetwork
from logger import get_logger
from random import random, shuffle
from math import floor
import numpy as np
from keras import backend as be
from settings import WINDOW_HEIGHT
import json
import copy

logger = get_logger('Population')

class Population:
    def __init__(self, popSize=10):
        self.popSize = popSize
        self.winnerThreshold = 0.16
        self.winnerPerc = 0.4
        self.equalPerc = 0.5
        self.alive = None
        self.dead = None
        self.counter = 0

    def nextGeneration(self):
        self.counter += 1
        dead = self.dead
        nextGen = []
        if(dead):
            for b in dead:
                if (0 < b.centerY < WINDOW_HEIGHT):
                    b.score += 10

            self.saveStats()
            dead.sort(key=(lambda b: b.score))
            dead[-1].save('gen' + str(self.counter))
            be.clear_session()
            winnerThreshold = floor(self.popSize * self.winnerThreshold)
            winners = dead[-winnerThreshold:]
            weights = [b.score for b in winners]
            weightSum = sum(weights)
            logger.info('Best Quarter Score avg: %f', weightSum/winnerThreshold)
            logger.info('Scores: %s', str(weights))
            logger.info('Generation %d', self.counter)
            weights = [w/weightSum for w in weights]
            winners = [b.brain for b in winners]
            dead = [b.brain for b in dead]

            # reproduce winners
            # half size because there are 2 resulting children in each iteration.
            winnerSize = floor(self.popSize * self.winnerPerc / 2)
            zipper = zip(np.random.choice(winners, size=winnerSize, p=weights), np.random.choice(winners, size=winnerSize, p=weights))
            for mom, dad in zipper:
                child1, child2 = mom.crossover(dad)
                child1.mutate()
                child2.mutate()
                nextGen.append(Bird(child1))
                nextGen.append(Bird(child2))

            # reproduce any genome with equal probability.
            # half size because there are 2 resulting children in each iteration.
            equalPoolSize = floor(self.popSize * self.equalPerc / 2)
            zipper = zip(np.random.choice(dead, size=equalPoolSize), np.random.choice(dead, size=equalPoolSize))
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

    def saveStats(self):        
        def encode(bird: Bird):
            result = {
                'changeY': bird.changeY,
                'velocity': bird.velocity,
                'centerX': bird.centerX,
                'centerY': bird.centerY,
                'radius': bird.radius,
                'color': bird.color,
                'score': bird.score,
                'frameCounter': bird.frameCounter
            }
            return result

        allBirds = self.alive + self.dead
        allBirds = [encode(b) for b in allBirds]
        # last gen's stats, but counter was already increased. make sure the file name matches the actual generation.
        with open('stats/birds_gen' + str(self.counter - 1) + '.json', mode='w') as f:
            json.dump(allBirds, f, sort_keys=True, indent=4)

    def kill(self, bird: Bird):        
        self.alive.remove(bird)
        self.dead.append(bird)

    def hasAlive(self) -> bool:
        return (len(self.alive) > 0)
