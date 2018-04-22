from random import random, randint, uniform
from keras.models import Sequential, clone_model
from keras.layers import Dense
from typing import Optional
import numpy as np
import copy

def change_weights(weights):
    if (not np.isscalar(weights[0])):
        for sub in weights:
            change_weights(sub)
        return

    rate = 0.07
    
    for i in range(len(weights)):
        if (random() >= rate):
            # dont change the weight.
            continue
        # else    
        #change = 0.2
        #if (random() < 0.5):
        #    change *= -1

        weights[i] += uniform(-1, 1)

def random_merge(list1, list2, prob1):
    result = []

    if (not np.isscalar(list1[0])):
        for elem1, elem2 in zip(list1,list2):
            result.append(random_merge(elem1, elem2, prob1))
    else:
        for elem1, elem2 in zip(list1,list2):
            rnd = random()

            if (rnd < prob1):
                # pick element from list1
                result.append(elem1)
            else:
                # pick element from list2
                result.append(elem2)

    result = np.array(result)
    return result


class NeuralNetwork:
    def __init__(self, inputs: int, outputs: int, weights=None):
        #if (model):
            # creates new random weights. hopefully saves time!
        #    model = clone_model(model)
        #else:
        model = Sequential()
        model.add(Dense(units=inputs, activation='relu',
                        input_dim=inputs, bias_initializer='glorot_uniform'))
        model.add(Dense(units=outputs, activation='softmax',
                        bias_initializer='glorot_uniform'))
            # For a binary classification problem
           # model.compile(optimizer='rmsprop',
          #              loss='binary_crossentropy', metrics=['accuracy'])
        #model.summary()
        if (weights != None):
            model.set_weights(weights)
        else:
            weights = model.get_weights()
            
        self.model = model
        self.inputs = inputs
        self.outputs = outputs
        self.weights = weights

    def mutate(self):   
        weights = self.get_weights()
        change_weights(weights)
        self.set_weights(weights)

    def crossover(self, partner: Optional['NeuralNetwork']):
        child1 = self.copy()
        child2 = partner.copy()

        if (self != partner):              
            weights1 = self.get_weights()
            weights2 = partner.get_weights()

            rate = 0.2
            result1 = random_merge(weights1, weights2, rate)
            result2 = random_merge(weights1, weights2, 1 - rate)

            child1.set_weights(result1)
            child2.set_weights(result2)
        return child1, child2

    def copy(self) -> Optional['NeuralNetwork']:
        #return self
        return NeuralNetwork(self.inputs, self.outputs, self.weights)

    def predict(self, inputs):
        inputs = np.array([inputs,])
        return self.model.predict(inputs, batch_size=1)

    def get_weights(self):
        return self.weights;
    
    def set_weights(self, weights):
        self.weights = weights
        self.model.set_weights(weights)