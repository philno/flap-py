import arcade
from random import uniform
from math import floor
from settings import WINDOW_HEIGHT, PIPE_WIDTH
from bird import Bird
class Pipe:
    def __init__(self, centerX, color):
        """ Constructor. """

        # Take the parameters of the init function above, and create instance variables out of them.
        self.centerX = centerX
        self.color = color
        self.changeX = -3
        gapSize = floor(uniform(0.7, 1) * 100)
        gapLocation = floor(uniform(0.25, 0.75) * WINDOW_HEIGHT)
        gapTop = gapLocation - gapSize
        gapBottom = gapLocation + gapSize
        if (gapTop < 0):
            gapTop = 0
        if (gapBottom > WINDOW_HEIGHT):
            gapBottom = WINDOW_HEIGHT

        self.lowerHeight = gapTop
        self.lowerCenterY = self.lowerHeight // 2

        self.upperHeight = WINDOW_HEIGHT - gapBottom
        self.upperCenterY = WINDOW_HEIGHT - (self.upperHeight // 2)

        self.gapLocation = gapLocation
        self.gapSize = gapSize
        self.rightCorner = centerX + (PIPE_WIDTH // 2)

    def draw(self):
        """ Draw the pipe """
        # Draw upper part
        arcade.draw_rectangle_filled(self.centerX, self.upperCenterY, PIPE_WIDTH, self.upperHeight, self.color)
        # Draw lower part
        arcade.draw_rectangle_filled(self.centerX, self.lowerCenterY, PIPE_WIDTH, self.lowerHeight, self.color)

    def update(self):
        """ Code to control the pipe's movement. """
        # Move the ball
        self.centerX += self.changeX
    
    def hits(self, bird: Bird) -> bool:
        radius = PIPE_WIDTH / 2

        if (abs(bird.centerX - self.centerX) <= radius):
            return (abs(bird.centerY - self.gapLocation) > self.gapSize)
        # else
        return False