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

    rate = 0.04
    
    for i in range(len(weights)):
        if (random() >= rate):
            # dont change the weight.
            continue
        # else    
        change = 0.1
        if (random() < 0.5):
            change *= -1

        weights[i] += change

def random_merge(list1, list2, prob1):
    result = []
    if (not np.isscalar(list1[0])):
        for i in range(len(list1)):
            result.append(random_merge(list1[i], list2[i], prob1))
    else:
        for i, elem in enumerate(list1):
            rnd = random()

            if (rnd < prob1):
                # pick element from list1
                result.append(elem)
            else:
                # pick element from list2
                result.append(list2[i])

    result = np.array(result)
    return result

class NeuralNetwork:
    def __init__(self, inputs: int, outputs: int, weights=None):
        model = Sequential()
        model.add(Dense(units=inputs, activation='relu',
                        input_dim=inputs, bias_initializer='glorot_uniform'))
        model.add(Dense(units=outputs, activation='softmax',
                        bias_initializer='glorot_uniform'))
        # For a binary classification problem
        model.compile(optimizer='rmsprop',
                      loss='binary_crossentropy', metrics=['accuracy'])
        #model.summary()
        if (weights):
            model.set_weights(weights)

        self.model = model
        self.inputs = inputs
        self.outputs = outputs


    def mutate(self):   
        model = self.model
        weights = model.get_weights()
        change_weights(weights)
        model.set_weights(weights)

    def crossover(self, partner: Optional['NeuralNetwork']):              
        weights1 = self.model.get_weights()
        weights2 = partner.model.get_weights()

        rate = 0.15
        result1 = random_merge(weights1, weights2, rate)
        result2 = random_merge(weights1, weights2, 1 - rate)

        child1 = self.copy()
        child1.model.set_weights(result1)

        child2 = partner.copy()
        child2.model.set_weights(result2)
        return child1, child2

    def copy(self) -> Optional['NeuralNetwork']:
        return NeuralNetwork(self.inputs, self.outputs, self.model.get_weights())

    def predict(self, inputs):
        inputs = np.array([inputs,])
        return self.model.predict(inputs, batch_size=1)