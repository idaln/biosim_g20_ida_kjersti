# -*- coding: utf-8 -*-

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idna@nmbu.no & kjkv@nmbu.no"

params_herbivore = {
    "w_birth": 8.0,
    "sigma_birth": 1.5,
    "beta": 0.9,
    "eta": 0.05,
    "a_half": 40.0,
    "phi_age": 0.2,
    "w_half": 10.0,
    "phi_weight": 0.1,
    "mu": 0.25,
    "lambda": 1.0,
    "gamma": 0.2,
    "zeta": 3.5,
    "xi": 1.2,
    "omega": 0.4,
    "F": 10.0,
}

params_carnivore = {
        "w_birth": 6.0,
        "sigma_birth": 1.0,
        "beta": 0.75,
        "eta": 0.125,
        "a_half": 60.0,
        "phi_age": 0.4,
        "w_half": 4.0,
        "phi_weight": 0.4,
        "mu": 0.4,
        "lambda": 1.0,
        "gamma": 0.8,
        "zeta": 3.5,
        "xi": 1.1,
        "omega": 0.9,
        "F": 50.0,
        "DeltaPhiMax": 10.0
}


class Animal:
    """ Parent class for herbivores and carnivores
    """

    def __init__(self, params, properties):
        """ Initializing class
        Need to unpack params
        """
        self.weight = properties['weight']
        self.age = properties['age']

        if 'fitness' not in properties.keys():
            self.fitness = None

        else:
            self.fitness = properties['fitness']

    def ageing(self):
        """ Adds 1 year to the age of the animal for each cycle."""
        pass

    def weight_loss(self):
        """ Substracts given amount of weight from the animals
        total weight after each cycle, given by eta*weight"""
        pass

    def eat(self):
        """ Adds amount of weight to animals total body weight given by
        beta*F"""
        pass

    def fitness(self):
        """ Updates fitness.
        Fitness is zero if weight is zero, otherwise given by formula (3)."""
        pass

    def migration(self):
        """
        Moves animal
        """
        pass

    @property
    def prob_give_birth(self):
        """
        Checks that weight of animal is more than given limit. If so,
        probability of giving birth is calculated from formula (8).
        :returns prob
                 Probability of giving birth
        """
        pass

    def give_birth(self):
        """ Finds probability of animal giving birth, created new instance of
        animal and reduces weight of mother."""
        pass

    def death(self):
        """ Finds probability of dying, and returns True if animal dies and
        False if not. """
        pass


