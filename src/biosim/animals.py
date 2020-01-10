# -*- coding: utf-8 -*-

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idna@nmbu.no & kjkv@nmbu.no"

import numpy as np

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
    params = {
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

    def __init__(self, properties):
        """
        Initializing class by unpacking all parameters given as input.
        """

        self.weight = properties["weight"]
        self.age = properties["age"]

        if "fitness" not in properties.keys():
            self.fitness = None
        else:
            self.fitness = properties["fitness"]

    def age_animal_up_one_year(self):
        """
        Adds 1 year to the age of the animal for each cycle.
        """
        self.age += 1

    def weight_loss(self):
        """
        Substracts given amount of weight from the animals
        total weight after each cycle, given by eta*weight
        """
        new_weight = (1 - self.params['eta']) * self.weight
        self.weight = new_weight

    def add_eaten_fodder_to_weight(self, fodder):
        """
        Adds amount of weight to animals total body weight given by
        beta*F
        :param fodder
               Amount of fodder available to the animal
        """
        self.weight += self.params['beta'] * fodder

    def find_fitness(self):
        """
        Updates fitness.
        Fitness is zero if weight is zero, otherwise given by formula (3).
        """
        q_plus = 1/(1 + np.exp(
            self.params["phi_age"]*(self.age - self.params["a_half"])
        ))
        q_minus = 1/(1 + np.exp(
            -self.params["phi_weight"]*(self.weight - self.params["w_half"])
        ))

        if self.weight <= 0:
            self.fitness = 0
        else:
            self.fitness = q_plus * q_minus

    def migration(self):
        """
        Moves animal
        """
        pass

    def prob_give_birth(self, num_animals):
        """
        Checks that weight of animal is more than given limit. If so,
        probability of giving birth is calculated from formula (8).
        :returns prob
                 Probability of giving birth
        """
        if self.weight < self.params['zeta'] * (
                self.params['w_birth'] + self.params['sigma_birth']
        ):
            return 0
        else:
            return min(
                1, self.params['gamma'] * self.fitness * (num_animals - 1)
            )

    def will_birth_take_place(self, num_animals):
        """
        Checks probability of giving birth and returns True if a baby is to be
        born.
        :returns bool
        """
        prob = self.prob_give_birth(num_animals)
        random_number = np.random.random()

        if random_number <= prob:
            return True

    def birth_process(self, num_animals):
        """
        If birth takes place, a birth weight is returned and weight of mother
        is reduced according to given formula.

        :returns birth_weight or None
                 int, float
        """
        bool_birth = self.will_birth_take_place(num_animals)
        birth_weight = np.random.normal(
            self.params['w_birth'], self.params['sigma_birth']
        )
        if bool_birth is True and birth_weight > 0 and \
                self.weight > birth_weight * self.params['xi']:
            self.weight -= birth_weight * self.params['xi']
            return birth_weight

    def prob_death(self):
        """
        Finds probability of death, which depends on the fitness of the
        animal.
        """
        if self.fitness == 0:
            return 1
        else:
            return self.params['omega'] * (1 - self.fitness)

    def will_death_take_place(self):
        """
        Checks the probability of death. Returns True if the animal dies.
        :return bool
        """
        prob = self.prob_death()
        random_number = np.random.random()

        if random_number <= prob:
            return True


class Herbivore(Animal):
    """
    Class for herbivores.
    """
    params = {
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

    def __init__(self, properties):
        """
        Initializes herbivore animal with given properties.
        :param properties: dict storing age, weight and fitness of herbivore
        """
        super().__init__(properties)
