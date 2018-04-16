import arcade
from random import uniform
from math import floor

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PIPE_WIDTH = 40

# Here: x=0,y=0 means lower left corner of the window

class Pipe:
    def __init__(self, centerX, color):
        """ Constructor. """

        # Take the parameters of the init function above, and create instance variables out of them.
        self.centerX = centerX
        self.color = color
        self.changeX = -2
        gapSize = 100
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


    def draw(self):
        """ Draw the pipe """
        # Draw upper part
        arcade.draw_rectangle_filled(self.centerX, self.upperCenterY, PIPE_WIDTH, self.upperHeight, self.color)
        # Draw lower part
        arcade.draw_rectangle_filled(self.centerX, self.lowerCenterY, PIPE_WIDTH, self.lowerHeight, self.color)

    def update(self):
        """ Code to control the ball's movement. """
        # Move the ball
        self.centerX += self.changeX

class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        # Call the parent class's init function
        super().__init__(width, height, title)

        # Set the background color
        arcade.set_background_color(arcade.color.WHITE_SMOKE)

        # Add a few pipes
        self.pipes = []
        while (True):
            self.add_pipe()
            if (self.pipes[-1].centerX > WINDOW_WIDTH + 2*self.get_pipe_dist() + 2* PIPE_WIDTH):
                break

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        for pipe in self.pipes:
            pipe.draw()

        arcade.draw_circle_filled(40, WINDOW_HEIGHT//2, 18, arcade.color.AUBURN)

    def update(self, delta_time):
        for pipe in self.pipes[:]:
            if (pipe.centerX < -PIPE_WIDTH):
                self.pipes.remove(pipe)
                self.add_pipe()
            else:
                pipe.update()

    def add_pipe(self):
        insertAt = 100
        if (len(self.pipes) > 0): 
            insertAt = self.pipes[-1].centerX + self.get_pipe_dist()

        self.pipes.append(Pipe(insertAt, arcade.color.VIRIDIAN_GREEN))

    def get_pipe_dist(self):
        return PIPE_WIDTH * 4 + 10

def main():
    window = MyGame(WINDOW_WIDTH, WINDOW_HEIGHT, "flap-py")

    arcade.run()


main()