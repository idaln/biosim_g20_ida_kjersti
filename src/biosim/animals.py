# -*- coding: utf-8 -*-

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idna@nmbu.no & kjkv@nmbu.no"

import numpy as np


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
    "DeltaPhiMax": None
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
    """
    Parent class for herbivores and carnivores
    """

    def __init__(self, params, properties, num_animals):
        """
        Initializing class by unpacking all parameters given as input.
        """
        self.w_birth = params["w_birth"]
        self.sigma_birth = params["sigma_birth"]
        self.beta = params["beta"]
        self.eta = params["eta"]
        self.a_half = params["a_half"]
        self.phi_age = params["phi_age"]
        self.w_half = params["w_half"]
        self.phi_weight = params["phi_weight"]
        self.mu = params["mu"]
        self._lambda = params["lambda"]
        self.gamma = params["gamma"]
        self.zeta = params["zeta"]
        self.xi = params["xi"]
        self.omega = params["omega"]
        self.F = params["F"]
        self.DeltaPhiMax = params["DeltaPhiMax"]

        self.weight = properties["weight"]
        self.age = properties["age"]

        if "fitness" not in properties.keys():
            self.fitness = None
        else:
            self.fitness = properties["fitness"]

        self.num_animals = num_animals

    def ageing(self):
        """
        Adds 1 year to the age of the animal for each cycle.
        """
        self.age += 1

    def weight_loss(self):
        """
        Substracts given amount of weight from the animals
        total weight after each cycle, given by eta*weight
        """
        new_weight = (1 - self.eta) * self.weight
        self.weight = new_weight

    def eat(self, fodder):
        """
        Adds amount of weight to animals total body weight given by
        beta*F
        :param fodder
               Amount of fodder available to the animal
        """
        self.weight += self.beta * fodder

    def find_fitness(self):
        """
        Updates fitness.
        Fitness is zero if weight is zero, otherwise given by formula (3).
        """
        q_plus = 1/(1 + np.exp(self.phi_age*(self.age - self.a_half)))
        q_minus = 1/(1 + np.exp(-self.phi_weight*(self.weight - self.w_half)))

        if self.weight <= 0:
            self.fitness = 0
        else:
            self.fitness = q_plus * q_minus


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
        if self.weight < self.zeta * (self.w_birth + self.sigma_birth):
            return 0
        else:
            return min(1, self.gamma * self.fitness * (self.num_animals - 1))

    def bool_give_birth(self):
        """
        Checks probability of giving birth and finds out if a baby is to be
        born.
        :returns bool
        """
        prob = self.prob_give_birth
        random_number = np.random.random()

        if random_number <= prob:
            return True
        else:
            return False

    def birth_process(self):
        """
        If birth takes place, a birth weight is returned. If not, None is
        returned. Weight of mother is reduced according to gived formula.

        :returns birth_weight or None
                 int, float
        """
        bool_birth = self.bool_give_birth()
        if bool_birth is True:
            birth_weight = np.random.normal(self.w_birth, self.sigma_birth)
            if birth_weight == 0:
                return None
            else:
                self.weight -= birth_weight * self.xi
                return birth_weight
        else:
            return None

    def prob_death(self):
        """
        Finds probability of death, which depends on the fitness of the
        animal.
        """
        if self.fitness == 0:
            return 1
        else:
            return self.omega * (1 - self.fitness)

    def bool_death(self):
        """
        Checks the probability of death. Returns True if the animal dies,
        and False if not.
        :return bool
        """
        pass


