# flap-py
flap-py is about using a genetic algorithm to teach an AI how to play flappy bird in python. 
In each generation, the population of birds tries to beat the game (stay in between the pipes and not fall down). The next generation is mostly formed from the members of the previous one based on their score (== fitness function). A smaller parts is sampled from the whole previous population with equal probability and the missing spots are filled with new, random birds to make sure there is enough diversity in the gene pool. Crossover and mutation are applied to converge to a 'good enough' solution quickly. 

The 'brain' of the birds (neural network that decides wheter to jump or not) uses a `keras` model with 5 inputs, a hidden layer with 5 nodes and 2 outputs. Softmax is applied so the outputs can be interpreted as the probability to either jump or do nothing. The neural network gets the following inputs (normalized to [0,1]): birdY, birdVelocity, pipeDist, gapTop, gapBottom; Where pipe and gap related values are taken from the closest pipe in front of the bird.

A simplified version of the flappy bird game is drawn with the `arcade` library. Every bird is a triangle with a random color. Depending on the population size, it might need a few minutes to produce a new generation.

# How to run
You want to install the dependencies with the python packet manager of your choice first: 

* tensorflow (or any keras backend of your choice)
* keras
* arcade
* numpy
* pygal (for plots of statistics)

The main application file is `flap.py`. There, you can also configure the population size (128 should be a good value).
You can generate different statistics like top and average score of each generation by running `stats.py`. The generated plots will open in your default browser.
