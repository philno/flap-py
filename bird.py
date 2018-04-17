import arcade
from settings import WINDOW_HEIGHT
from math import sqrt

class Bird:
    def __init__(self):
        self.changeY = -1.0123
        self.velocity = 0
        self.centerX = 40
        self.centerY = WINDOW_HEIGHT // 2
        self.score = 0
        self.frameCounter = 0

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
        if (self.frameCounter % 60 == 0): 
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
                