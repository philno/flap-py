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
        self.highScore = 0
        self.restart()

    def on_key_release(self, key: int, modifiers: int):
        pass
        
    def restart(self):
        # Add a few pipes
        self.pipes = []
        while (True):
            self.add_pipe()
            if (self.pipes[-1].centerX > WINDOW_WIDTH + 2*self.get_pipe_dist() + 2* PIPE_WIDTH):
                break
        
        # Add birds
        self.birds = []
        for i in range(25):
            self.birds.append(Bird())

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        arcade.start_render()
        for pipe in self.pipes:
            pipe.draw()

        for bird in self.birds:
            bird.draw()

        arcade.draw_text('High Score: ' + str(self.highScore), WINDOW_WIDTH//2, WINDOW_HEIGHT - FONT_SIZE - 10, arcade.color.TIGERS_EYE, FONT_SIZE)


    def update(self, delta_time):
        for pipe in self.pipes[:]:
            if (pipe.centerX < -PIPE_WIDTH):
                self.pipes.remove(pipe)
                self.add_pipe()
                continue
            # else   
            pipe.update()
        
        birds = self.birds

        if (len(birds) <= 0):
            self.restart()
            return
        # else
        self.highScore = birds[0].score
        for bird in birds:
            if (bird.centerY < 0):
                birds.remove(bird)
                continue

            bird.update()
            nearestPipe = self.get_nearest_pipe(bird)
            if (nearestPipe.hits(bird)):
                birds.remove(bird)
                continue
            
            dist = (nearestPipe.rightCorner - bird.centerX) / self.get_pipe_dist()
            gapTop = nearestPipe.gapTop / WINDOW_HEIGHT
            gapBottom = nearestPipe.gapBottom / WINDOW_HEIGHT
            bird.think(dist, gapTop, gapBottom)
            

    def add_pipe(self):
        insertAt = PIPE_WIDTH*6
        if (len(self.pipes) > 0): 
            insertAt = self.pipes[-1].centerX + self.get_pipe_dist()

        self.pipes.append(Pipe(insertAt, arcade.color.VIRIDIAN_GREEN))

    def get_pipe_dist(self):
        return PIPE_WIDTH * 4 + 10

    def get_nearest_pipe(self, bird: Bird) -> Pipe:
        for pipe in self.pipes:
            if (pipe.rightCorner < bird.centerX):
                continue
            #else
            return pipe
            

def main():
    window = Flap(WINDOW_WIDTH, WINDOW_HEIGHT, "flap-py")

    for i in range(42):
        window.update(0)
    arcade.run()

main()