import arcade
from pipe import Pipe
from bird import Bird
from settings import WINDOW_HEIGHT, WINDOW_WIDTH, PIPE_WIDTH, FONT_SIZE

# Here: x=0,y=0 means lower left corner of the window
class Flap(arcade.Window):

    def __init__(self, width, height, title):
        # Call the parent class's init function
        super().__init__(width, height, title)

        # Set the background color
        arcade.set_background_color(arcade.color.WHITE_SMOKE)
        self.restart()

    def on_key_release(self, key: int, modifiers: int):
        if (key == arcade.key.SPACE): 
            self.bird.up()
        
    def restart(self):
        # Add a few pipes
        self.pipes = []
        while (True):
            self.add_pipe()
            if (self.pipes[-1].centerX > WINDOW_WIDTH + 2*self.get_pipe_dist() + 2* PIPE_WIDTH):
                break
        
        # Add a bird
        self.bird = Bird()

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        for pipe in self.pipes:
            pipe.draw()

        arcade.draw_text('Score: ' + str(self.bird.score), WINDOW_WIDTH//2, WINDOW_HEIGHT - FONT_SIZE - 10, arcade.color.TIGERS_EYE, FONT_SIZE)

        self.bird.draw()

    def update(self, delta_time):
        if (self.bird.centerY < 0):
            self.restart()

        for pipe in self.pipes[:]:
            if (pipe.centerX < -PIPE_WIDTH):
                self.pipes.remove(pipe)
                self.add_pipe()
            else:
                pipe.update()
        
        self.bird.update()

    def add_pipe(self):
        insertAt = PIPE_WIDTH*6
        if (len(self.pipes) > 0): 
            insertAt = self.pipes[-1].centerX + self.get_pipe_dist()

        self.pipes.append(Pipe(insertAt, arcade.color.VIRIDIAN_GREEN))

    def get_pipe_dist(self):
        return PIPE_WIDTH * 4 + 10

def main():
    window = Flap(WINDOW_WIDTH, WINDOW_HEIGHT, "flap-py")

    arcade.run()


main()