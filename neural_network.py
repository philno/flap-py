from random import random, randint
from keras.models import Sequential
from keras.layers import Dense
from typing import Optional
import numpy as np
import copy

def change_weights(weights):
    if (not np.isscalar(weights[0])):
        for sub in weights:
            change_weights(sub)
        return

    rate = 0.5
    
    for i in range(len(weights)):
        if (random() >= rate):
            # dont change the weight.
            continue
        # else    
        change = 0.1
        if (random() < 0.5):
            change *= -1

        weights[i] += change


class NeuralNetwork:
    def __init__(self, inputs: int, outputs: int):
        model = Sequential()
        model.add(Dense(units=inputs, activation='relu',
                        input_dim=inputs, bias_initializer='glorot_uniform'))
        model.add(Dense(units=outputs, activation='softmax',
                        bias_initializer='glorot_uniform'))
        # For a binary classification problem
        model.compile(optimizer='rmsprop',
                      loss='binary_crossentropy', metrics=['accuracy'])
        model.summary()
        self.model = model

    def mutate(self):   
        model = self.model
        weights = model.get_weights()
        change_weights(weights)
        model.set_weights(weights)

    def crossover(self, partner: Optional['NeuralNetwork']) -> Optional['NeuralNetwork']:
        # todo: add crossover code
        pass

    def copy(self) -> Optional['NeuralNetwork']:
        return copy.deepcopy(self)

    def predict(self, inputs):
        inputs = np.array([inputs,])
        print('input shape', inputs.shape)
        return self.model.predict(inputs, batch_size=1)

nn = NeuralNetwork(4,2)

prediction = nn.predict([0.7, 0.2, 0.4, 0.1])
print(prediction)