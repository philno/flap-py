import arcade
from settings import WINDOW_HEIGHT
from math import sqrt
from neural_network import NeuralNetwork
class Bird:
    def __init__(self, brain):
        self.changeY = -1.0123
        self.velocity = 0
        self.centerX = 40
        self.centerY = WINDOW_HEIGHT // 2
        self.score = 0
        self.frameCounter = 0
        if (brain):
            self.brain = brain
        else:
            # inputs: birdY, birdVelocity, pipeDist, gapTop, gapBottom
            self.brain = NeuralNetwork(5,2)

    def draw(self):
        """ Draw the bird """
        arcade.draw_circle_filled(self.centerX, self.centerY, 18, arcade.color.AUBURN)

    def update(self):
        """ Code to control the bird's movement. """
        self.velocity += self.changeY
        self.centerY += self.velocity

        if (self.centerY > WINDOW_HEIGHT):
            self.centerY = WINDOW_HEIGHT
        elif (self.centerY < -1):
            self.centerY = -1

        self.frameCounter += 1
        if (self.frameCounter % 61 == 0): 
            self.score += 1
            self.frameCounter = 0
    
    def up(self):
        """ Let the bird go up with it's wings """
        vel = self.velocity
        change = 0
        if (vel >= 0):
            change = 16 - sqrt(vel*12)
            gravity = abs(self.changeY)
            if (change < gravity):
                change = 16
        else:
            change = 20 + sqrt(abs(vel))
        self.velocity += change

    def think(self, dist, gapTop, gapBottom):
        inputs = []
        # inputs: birdY, birdVelocity, pipeDist, gapTop, gapBottom
        inputs.append(self.centerY / WINDOW_HEIGHT)
        inputs.append(self.velocity / 10)
        inputs.append(dist)
        inputs.append(gapTop)
        inputs.append(gapBottom)
        outputs = self.brain.predict(inputs)[0]
        if (outputs[0] > outputs[1]):
            self.up()
                