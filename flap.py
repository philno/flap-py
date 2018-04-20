import arcade
from pipe import Pipe
from bird import Bird
from population import Population
from settings import WINDOW_HEIGHT, WINDOW_WIDTH, PIPE_WIDTH, FONT_SIZE

# Here: x=0,y=0 means lower left corner of the window
class Flap(arcade.Window):

    def __init__(self, width, height, title):
        # Call the parent class's init function
        super().__init__(width, height, title)

        # Set the background color
        arcade.set_background_color(arcade.color.WHITE_SMOKE)
        self.highScore = 0
        self.pop = Population(100)
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
        self.pop.nextGeneration()


    def on_draw(self):
        """ Called whenever we need to draw the window. """
        shapes = arcade.ShapeElementList()
        pipePoints = []
        pipeColors = []
        for pipe in self.pipes:
            pipe.append_points(pipePoints, pipeColors)
        shapes.append(arcade.create_rectangles_filled_with_colors(pipePoints, pipeColors))

        birdPoints = []
        birdColors = []
        for bird in self.pop.alive:
            bird.append_points(birdPoints, birdColors)
        shapes.append(arcade.create_triangles_filled_with_colors(birdPoints, birdColors))

        arcade.start_render()
        shapes.draw()
        arcade.draw_text('High Score: ' + str(self.highScore), WINDOW_WIDTH//2 - 40, WINDOW_HEIGHT - FONT_SIZE - 10, arcade.color.TIGERS_EYE, FONT_SIZE)

    def update(self, delta_time):
        for pipe in self.pipes[:]:
            if (pipe.centerX < -PIPE_WIDTH):
                self.pipes.remove(pipe)
                self.add_pipe()
                continue
            # else   
            pipe.update()
        
        pop = self.pop
        birds = pop.alive

        if (not pop.hasAlive()):
            self.restart()
            return
        # else
        if (birds[0].score > self.highScore):
            self.highScore = birds[0].score
        
        for bird in birds:
            if (bird.centerY < 0):
                pop.kill(bird)
                continue

            bird.update()
            nearestPipe = self.get_nearest_pipe(bird)
            if (nearestPipe.hits(bird)):
                pop.kill(bird)
                continue
            
            dist = (nearestPipe.rightCorner - bird.centerX) / self.get_pipe_dist()
            gapTop = nearestPipe.gapTop / WINDOW_HEIGHT
            gapBottom = nearestPipe.gapBottom / WINDOW_HEIGHT
            bird.think(dist, gapTop, gapBottom)
            

    def add_pipe(self):
        insertAt = self.get_pipe_dist()
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

    for i in range(20):
        while(window.pop.hasAlive()):
            if (window.highScore > 9000):
                break
            window.update(0)
        print('High Score', window.highScore)
        if (window.highScore > 9000):
            print('over 9000!!!')
            break
        window.on_draw()
        window.update(0)
    arcade.run()

main()