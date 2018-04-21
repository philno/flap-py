import arcade
from settings import WINDOW_HEIGHT, VELOCITY_BOUND
from math import sqrt
from neural_network import NeuralNetwork
from logger import get_logger
from random import randint


logger = get_logger('Bird')

# inputs: birdY, birdVelocity, pipeDist, gapTop, gapBottom
inputNum = 5
outputNum = 2

def random_color():
    r = randint(0, 210)
    g = randint(0, 210)
    b = randint(0, 210)
    result = (r, g, b, 150)
    return result

class Bird:
    def __init__(self, brain=None):
        self.changeY = -1.0123
        self.velocity = 0
        self.centerX = 40
        self.centerY = WINDOW_HEIGHT // 2
        self.radius = 18
        self.color = random_color()
        self.score = 0
        self.frameCounter = 0
        if (brain):
            self.brain = brain
        else:
            self.brain = NeuralNetwork(inputNum, outputNum)

    def draw(self):
        """ Draw the bird """
        arcade.draw_circle_filled(self.centerX, self.centerY, self.radius, self.color)
    
    def append_shapes(self, shapes: arcade.ShapeElementList):
        radius = self.radius
        shapes.append(arcade.create_ellipse_filled(self.centerX, self.centerY, radius, radius, self.color))

    def append_points(self, points, colors):   
        halfWidth = self.radius / 2
        centerX = self.centerX
        centerY = self.centerY
        left = centerX - halfWidth
        right = centerX + halfWidth
        top = centerY + halfWidth
        bottom = centerY - halfWidth

        # top part of the bird
        top = (centerX, top)
        bottomLeft = (left, bottom)
        bottomRight = (right, bottom)

        points.append(bottomLeft)
        points.append(top)
        points.append(bottomRight)
        
        for i in range(3):
            colors.append(self.color)

    def update(self):
        """ Code to control the bird's movement. """
        self.velocity += self.changeY
        bounds = VELOCITY_BOUND
        if (self.velocity > bounds):
            self.velocity = bounds
        elif(self.velocity < -bounds):
            self.velocity = -bounds
        
        self.centerY += self.velocity

        if (self.centerY > WINDOW_HEIGHT):
            self.centerY = WINDOW_HEIGHT
        elif (self.centerY < -1):
            self.centerY = -1

        self.frameCounter += 1
        if (self.frameCounter % 10 == 0): 
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
        inputs.append(self.velocity / VELOCITY_BOUND)
        inputs.append(dist)
        inputs.append(gapTop)
        inputs.append(gapBottom)
        outputs = self.brain.predict(inputs)[0]
        if (outputs[0] > outputs[1]):
            self.up()

    def save(self, fileName: str):
        self.brain.model.save('best/' + fileName + '.h5', include_optimizer=False)

                