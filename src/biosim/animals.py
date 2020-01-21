# -*- coding: utf-8 -*-

"""
This module provides classes implementing the animals on the Island.
"""

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idna@nmbu.no & kjkv@nmbu.no"

import numpy as np
import math



class Animal:
    """
    Parent class for herbivores and carnivores.
    """
    _DEFAULT_PARAMS = {
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

    @classmethod
    def GET_DEFAULT_PARAMS(cls):
        """
        Returns a copy of the default animal parameters.

        :return: Copy of default animal parameters
        :rtype: dict
        """
        return cls._DEFAULT_PARAMS.copy()

    @classmethod
    def reset_params(cls):
        """
        Sets the animal parameters equal to default.
        """
        cls.params = cls.GET_DEFAULT_PARAMS()

    def __init__(self, properties):
        """
        Initializing Animal class by asserting property values are valid.

        :param properties: Contains animal properties species, fitness, age
            and weight.
        :type properties: dict

        """
        self.has_moved_this_year = False
        self.fitness_must_be_updated = True

        if "fitness" not in properties.keys():
            self.fitness = None
        else:
            self.fitness = properties["fitness"]

        if properties["age"] < 0:
            raise ValueError('Age must be nonnegative')
        else:
            self.age = properties["age"]

        if properties["weight"] <= 0:
            raise ValueError('Weight must be positive')
        else:
            self.weight = properties["weight"]

    def make_animal_one_year_older(self):
        """
        Adds 1 year to the age of the animal for each cycle.
        """
        self.age += 1
        self.fitness_must_be_updated = True

    def weight_loss(self):
        """
        Substracts given amount of weight from the animals
        total weight after each cycle, given by
        :math:`\\eta \\cdot weight`.
        """
        new_weight = (1 - self.params['eta']) * self.weight
        self.weight = new_weight
        self.fitness_must_be_updated = True

    def add_eaten_fodder_to_weight(self, fodder):
        """
        Adds amount of weight to animals total body weight given by
        :math:`\\beta \\cdot F`. Also resets have_moved_this_year to False.

        :param fodder: Amount of fodder available to the animal
        :type fodder: float

        """
        self.weight += self.params['beta'] * fodder
        self.fitness_must_be_updated = True
        self.has_moved_this_year = False

    def find_fitness(self):
        """
        Updates fitness.
        Fitness is zero if weight is zero, otherwise given by

        .. math:: q\\^{+}(a, a_{\\fraq{1}{2}}, \\phi_{age}) \\cdot q\\^{-}
        (w, w_{\\fraq{1}{2}}, \\phi_{weight}

        where

        .. math:: q\\^{\\pm}(x, x_{\\fraq{1}{2}, \\phi) = \\fraq{1}{1 + e\\^
        {\\pm \\phi(x-x_{\\fraq{1}{2}})}

        """

        q_plus = 1/(1 + math.exp(
            self.params["phi_age"]*(self.age - self.params["a_half"])
        ))
        q_minus = 1/(1 + math.exp(
            -self.params["phi_weight"]*(self.weight - self.params["w_half"])
        ))

        if self.weight <= 0:
            self.fitness = 0
            self.fitness_must_be_updated = False
        else:
            self.fitness = q_plus * q_minus
            self.fitness_must_be_updated = False

    def prob_of_animal_moving(self):
        """
        Computes the probability of moving at all, which depends on the
        animal's fitness.

        :return: Probability of moving
        :rtype: float
        """
        if self.fitness_must_be_updated is True:
            self.find_fitness()
        self.fitness_must_be_updated = False
        return self.fitness * self.params["mu"]

    def will_animal_move(self):
        """
        Compared probability of animal moving and a random number to decide
        whether the animal should move.

        :return: True if animal will move, False if not.
        :rtype: bool
        """
        prob = self.prob_of_animal_moving()
        random_number = np.random.random()

        if random_number <= prob:
            self.has_moved_this_year = True
            return True

    def find_rel_abund_of_fodder(self, landscape_cell):
        """
        Takes an instance of a landscape class and returns the relative
        abundance of fodder in that instance, given by

        .. math:: \\epsilon = \\fraq{f_k}{(n_k + 1)F^'}

        :param landscape_cell: Instance of landscape class
        :type landscape_cell: dict
        :return: Relative abundance of fodder
        :rtype: float
        """
        fodder_animal = landscape_cell.fodder_amount
        num_animals = len(landscape_cell.population)
        abund_fodder_animal = fodder_animal / \
            ((num_animals + 1) * self.params["F"])
        return abund_fodder_animal

    def propensity_move_to_each_neighbour(self, neighbours_of_current_cell):
        """
        Finds the propensity for the animal to move to each of it's neighbours.

        :param neighbours_of_current_cell: Contains neighbours of current cell.
            Location as keys, instance of landscape class as value
        :type neighbours_of_current_cell: dict
        :return: Maps location to it's propensity.
        :rtype: dict
        """

        loc_to_propensity_dict = {}
        for loc, landscape_instance in neighbours_of_current_cell.items():
            loc_to_propensity_dict[loc] = math.exp(
                self.params["lambda"] * self.find_rel_abund_of_fodder(
                    landscape_instance)
            )

        return loc_to_propensity_dict

    def prob_move_to_each_neighbour(self, neighbours_of_current_cell):
        """
        Iterates through the dict of neighbours to the current cell. Finds
        the probability of moving to each of the neighbouring cells. Returns
        a dict mapping cell locations to the probability of moving there.

        :param neighbours_of_current_cell: Neighbours of current cell.
            Locations as keys, instance of landscape class as value.
        :type neighbours_of_current_cell: dict
        :returns: Locations of each surrounding cell as keys, probabilities for
            the animal to move to each of them as values.
        :rtype: dict

        """
        moving_prob_for_each_loc = {}
        sum_prop = 0
        loc_to_prop_dict = self.propensity_move_to_each_neighbour(
            neighbours_of_current_cell
        )
        for propensity in loc_to_prop_dict.values():
            sum_prop += propensity

        for loc, propensity in loc_to_prop_dict.items():
            moving_prob_for_each_loc[loc] = propensity / sum_prop

        return moving_prob_for_each_loc

    @staticmethod
    def convert_dict_to_list_and_array(moving_prob_for_each_loc):
        """
        Converts dictionary with locations as keys and probabilities as
        values to a list of locations and a numpy array of probabilities.

        :param moving_prob_for_each_loc: Contains the locations of each
        surrounding cell as keys, and the probabilities for the animal to move
        to each of them as values.
        :type: dict
        :returns: List of locations of neighbouring cells, numpy array of the
            probabilities of moving to each.
        :rtype: list, array
        """
        locs = []
        probs = np.array([])
        for loc, prob in moving_prob_for_each_loc.items():
            locs.append(loc)
            probs = np.append(probs, np.array([prob]))
        return locs, probs

    def find_new_coordinates(self, neighbours_of_current_cell):
        """
        Uses cumulative probability to decide which of the neighbouring cells
        the animal will move to. Returns the coordinates of that cell.

        :param neighbours_of_current_cell: Neighbours of current cell.
            Locations as keys,
            instance of landscape class as value.
        :type neighbours_of_current_cell: dict
        :returns: The location the animal will move to.
        :rtype: tuple

        """
        moving_prob_for_each_loc = self.prob_move_to_each_neighbour(
                neighbours_of_current_cell
        )
        locs, probs = self.convert_dict_to_list_and_array(
            moving_prob_for_each_loc
        )

        cum_probs = np.cumsum(probs)
        random_number = np.random.random()

        if random_number < cum_probs[0]:
            return locs[0]
        elif cum_probs[0] < random_number < cum_probs[1]:
            return locs[1]
        elif cum_probs[1] < random_number < cum_probs[2]:
            return locs[2]
        else:
            return locs[3]

    def return_new_coordinates(self, neighbours_of_current_cell):
        """
        Checks whether the animal will move or not, and if so, returns the
        new coordinates.

        :param neighbours_of_current_cell: Neighbours of current cell.
            Locations as keys,
            instance of landscape class as value.
        :type neighbours_of_current_cell: dict
        :return: Location animal will move to.
        :rtype: tuple or None
        """
        if self.will_animal_move() is True:
            return self.find_new_coordinates(neighbours_of_current_cell)

    def prob_give_birth(self, num_animals):
        """
        Checks that weight of animal is more than given limit. If so,
        probability of giving birth is calculated from
        :math:`min(1, \\gamma \\cdot \\phi \\cdot (N-1)`

        :param num_animals: Number of animals of same species in cell
        :type num_animals: int
        :returns: The probability for the animal to give birth.
        :rtype: float
        """
        if self.fitness_must_be_updated is True:
            self.find_fitness()
        self.fitness_must_be_updated = False
        
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

        :returns True if animal shall give birth
        :rtype bool
        """
        prob = self.prob_give_birth(num_animals)
        random_number = np.random.random()

        if random_number <= prob:
            return True

    def birth_process(self, num_animals):
        """
        If birth takes place, a birth weight is returned and weight of mother
        is reduced according to given formula.

        :returns Returns weight of the baby that is born, or None if no baby
                is born.
        :rtype: float, None
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

        :return 1 if fitness is zero, :math:`\\omega \\cdot (1 - \\phi)`
            otherwise
        :rtype: float, int
        """
        if self.fitness_must_be_updated is True:
            self.find_fitness()
        self.fitness_must_be_updated = False
        if self.fitness == 0:
            return 1
        else:
            return self.params['omega'] * (1 - self.fitness)

    def will_animal_live(self):
        """
        Checks the probability of death. Returns True if the animal lives.

        :return True is animal lives
        :rtype bool
        """
        prob = self.prob_death()
        random_number = np.random.random()

        if random_number > prob:
            return True


class Herbivore(Animal):
    """
    Class for herbivores.
    """
    _DEFAULT_PARAMS = {
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

    def find_rel_abund_of_fodder(self, landscape_cell):
        """
        Takes an instance of a landscape class, and returns the relative
        abundance of fodder for herbivores in that instance, given by

        .. math:: \\epsilon = \\fraq{f_k}{(n_k + 1)F^'}

        :param landscape_cell: Instance of landscape class
        :type landscape_cell: dict
        :return: Relative abundance of fodder
        :rtype: float
        """
        fodder_herb = landscape_cell.fodder_amount
        num_herbs = len(landscape_cell.pop_herb)
        abund_fodder_herb = fodder_herb / ((num_herbs + 1) * self.params["F"])
        return abund_fodder_herb


class Carnivore(Animal):
    """
    Class for Carnivores.
    """
    _DEFAULT_PARAMS = {
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
        Initializes carnivore animal with given properties.

        :param properties: Contains age, weight and fitness of herbivore.
        :type properties: dict
        """
        super().__init__(properties)

    def prob_kill(self, fitness_herb):
        """
        Calculates the probability of a carnivore killing a herbivore.

        :param fitness_herb: Fitness of herbivore
        :type fitness_herb: float
        :return Probability of carnivore killing a herbivore
        :rtype: int, float
        """
        if self.fitness <= fitness_herb:
            return 0
        elif self.fitness - fitness_herb < self.params["DeltaPhiMax"]:
            return (self.fitness - fitness_herb) / self.params["DeltaPhiMax"]
        else:
            return 1

    def kill(self, herb):
        """
        Implements prob_kill and a random number to decide whether a
        carnivore kills or not.

        :param herb: Herbivore to be killed
        :type herb: class '__main__.Herbivore'
        :return: True if carnivore shall kill
        :rtype: bool
        """
        random_number = np.random.random()
        prob = self.prob_kill(herb.fitness)
        if random_number <= prob:
            return True
        else:
            return False

    def eat(self, pop_herb):
        """
        Iterates through list of herbivores, and implements kill method on one
        herbivore at the time until carnivore has satisfied it's appetite or
        has tried to kill all herbivores without luck.

        :param pop_herb: Herbivores available to the carnivore sorted by
                fitness
        :type pop_herb: list
        :return List of herbivores killed
        :rtype: list
        """
        amount_eaten = 0
        animals_eaten = []
        for herb in reversed(pop_herb):
            if amount_eaten < self.params["F"] and self.kill(herb) is True:
                animals_eaten.append(herb)
                amount_eaten += herb.weight
        self.weight += self.params["beta"] * amount_eaten
        self.find_fitness()
        self.fitness_must_be_updated = False
        return animals_eaten

    def find_rel_abund_of_fodder(self, landscape_cell):
        """
        Takes an instance of a landscape class, and returns the relative
        abundance of fodder in that instance, given by

        .. math:: \\epsilon = \\fraq{f_k}{(n_k + 1)F^'}

        :param landscape_cell: Instance of landscape class
        :type: dict
        :return: Relative abundance of fodder for the carnivore
        :rtype: float
        """
        fodder_carn = landscape_cell.available_fodder_carnivore()
        num_carns = len(landscape_cell.pop_carn)
        abund_fodder_carn = fodder_carn / ((num_carns + 1) * self.params["F"])
        return abund_fodder_carn
