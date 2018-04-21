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
        gapTop = gapLocation + gapSize
        gapBottom = gapLocation - gapSize
        if (gapTop < 0):
            gapTop = 0
        if (gapBottom > WINDOW_HEIGHT):
            gapBottom = WINDOW_HEIGHT

        self.lowerHeight = gapTop
        self.lowerCenterY = self.lowerHeight // 2

        self.upperHeight = WINDOW_HEIGHT - gapBottom
        self.upperCenterY = WINDOW_HEIGHT - (self.upperHeight // 2)

        self.gapTop = gapTop
        self.gapBottom = gapBottom
        self.gapLocation = gapLocation
        self.gapSize = gapSize
        self.halfWidth = PIPE_WIDTH / 2
        self.rightCorner = centerX + self.halfWidth

    def draw(self):
        """ Draw the pipe """
        # Draw upper part
        arcade.draw_rectangle_filled(self.centerX, self.upperCenterY, PIPE_WIDTH, self.upperHeight, self.color)
        # Draw lower part
        arcade.draw_rectangle_filled(self.centerX, self.lowerCenterY, PIPE_WIDTH, self.lowerHeight, self.color)

    def append_shapes(self, shapes: arcade.ShapeElementList):
        shapes.append(arcade.create_rectangle_filled(self.centerX, self.upperCenterY, PIPE_WIDTH, self.upperHeight, self.color))
        shapes.append(arcade.create_rectangle_filled(self.centerX, self.lowerCenterY, PIPE_WIDTH, self.lowerHeight, self.color))

    def append_points(self, points, colors):   
        halfWidth = PIPE_WIDTH / 2
        centerX = self.centerX
        left = centerX - halfWidth
        right = centerX + halfWidth
        gapTop = self.gapTop
        gapBottom = self.gapBottom

        # top part of the pipe
        topLeft = (left, WINDOW_HEIGHT)
        topRight = (right, WINDOW_HEIGHT)
        bottomLeft = (left, gapTop)
        bottomRight = (right, gapTop)

        points.append(topLeft)
        points.append(topRight)
        points.append(bottomRight)
        points.append(bottomLeft)
        
        for i in range(4):
            colors.append(self.color)

        # bottom part of the pipe
        topLeft = (left, gapBottom)
        topRight = (right, gapBottom)
        bottomLeft = (left, 0)
        bottomRight = (right, 0)

        points.append(topLeft)
        points.append(topRight)
        points.append(bottomRight)
        points.append(bottomLeft)
        
        for i in range(4):
            colors.append(self.color)
        

    def update(self):
        """ Code to control the pipe's movement. """
        # Move the ball
        self.centerX += self.changeX
        self.rightCorner = self.centerX + self.halfWidth
    
    def hits(self, bird: Bird) -> bool:
        radius = self.halfWidth

        if (abs(bird.centerX - self.centerX) <= radius):
            result = (abs(bird.centerY - self.gapLocation) > self.gapSize)
            if (not result):
                bird.score += 2
            return result
        # else
        return False