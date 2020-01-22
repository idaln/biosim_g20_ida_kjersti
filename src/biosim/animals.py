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

        :param properties: Contains animal properties species, age
            and weight. May also contain fitness.
        :type properties: dict
        """
        self.has_moved_this_year = False
        self.fitness_must_be_updated = True

        if properties["age"] < 0:
            raise ValueError('Age must be nonnegative')
        else:
            self.age = properties["age"]

        if properties["weight"] <= 0:
            raise ValueError('Weight must be positive')
        else:
            self.weight = properties["weight"]

        if "fitness" not in properties.keys():
            self.fitness = None
        else:
            self.fitness = properties["fitness"]

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

        .. math::

            q^{+}(a, a_{\\frac{1}{2}}, \\phi_{age}) \\cdot q^{-}
            (w, w_{\\frac{1}{2}}, \\phi_{weight})

        where

        .. math::

            q^{\\pm}(x, x_{\\frac{1}{2}}, \\phi) = \\frac{1}{1 + e^{\\pm
            \\phi(x-x_{\\frac{1}{2}})}}

        """

        q_plus = 1/(1 + math.exp(
            self.params["phi_age"]*(self.age - self.params["a_half"])
        ))
        q_minus = 1/(1 + math.exp(
            -self.params["phi_weight"]*(self.weight - self.params["w_half"])
        ))

        if self.weight <= 0:
            self.fitness = 0
        else:
            self.fitness = q_plus * q_minus
        self.fitness_must_be_updated = False

    def prob_of_animal_moving(self):
        """
        Computes the probability of moving at all,
        given by :math:`\\mu \\cdot \\phi`.

        :return: Probability of moving
        :rtype: float
        """
        if self.fitness_must_be_updated is True:
            self.find_fitness()
            self.fitness_must_be_updated = False
        return self.fitness * self.params["mu"]

    def will_animal_move(self):
        """
        Compares probability of animal moving and a random number to decide
        whether the animal should move.

        :return: True if animal will move, False if not
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

        .. math::

            \\epsilon = \\frac{f_k}{(n_k + 1)F^{'}}

        where :math:`f_k` is the amount of relevant fodder and :math:`n_k` is
        the number of animals of same species in cell k.
        This method cannot be called upon by an instance of the Animal class,
        since there is no population for animals.
        This method will be overwritten by Herbivore and Carnivore classes,
        and can only be called upon from instances of herbivores and
        carnivores, as we have pop_herb and pop_carn in the landscape cells.

        :param landscape_cell: Instance of landscape class
        :type landscape_cell: '__main__.Jungle', '__main__.Desert',
            '__main__.Savannah'
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
        Finds the propensity for the animal to move to each of it's neighbours,
        given by

        .. math::

            \\pi_{i \\to j} =
            \\Biggl
            \\lbrace
            {
            0,\\text{ if j is Mountain or Ocean }
            \\atop
            e^{\\lambda \\epsilon j}, \\text{ otherwise }
            }

        :param neighbours_of_current_cell: Contains neighbours of current cell.
            Location as keys, instances of landscape classes as value
        :type neighbours_of_current_cell: dict
        :return: Locations of each surrounding cell as keys, propensities for
            the animal to move to each of them as values.
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
        Iterates through the dict of neighbours for the current cell. Finds
        the probability of moving to each of the neighbouring cells. Returns
        a dict mapping cell locations to the probability of moving there.
        The probability is given by

        .. math::

            p = \\frac{\\pi_{i \\to j}}{\\Sigma_{j \\in C^{(i)}}
            \\pi_{i \\to j}}

        where :math:`\\pi_{i \\to j}` is the propensity to move from cell i to
        cell j.

        :param neighbours_of_current_cell: Neighbours of current cell.
            Locations as keys, instances of landscape classes as values.
        :type neighbours_of_current_cell: dict
        :return: Locations of each surrounding cell as keys, probabilities for
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
            surrounding cell as keys, and the probabilities for the animal
            to move to each of them as values.
        :type moving_prob_for_each_loc: dict
        :return: List of locations of neighbouring cells, numpy array of the
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
            Locations as keys, instances of landscape classes as values.
        :type neighbours_of_current_cell: dict
        :return: The location the animal will move to.
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
        Checks whether the animal will move or not, and if it will move,
        returns the new coordinates.

        :param neighbours_of_current_cell: Neighbours of current cell.
            Locations as keys, instances of landscape classes as values.
        :type neighbours_of_current_cell: dict
        :return: Location animal will move to.
        :rtype: tuple or None
        """
        if self.will_animal_move() is True:
            return self.find_new_coordinates(neighbours_of_current_cell)

    def prob_give_birth(self, num_animals):
        """
        If neccessary, finds fitness of animal.
        Then, checks that weight of animal is more than given limit. If so,
        probability of giving birth is calculated from
        :math:`min(1, \\gamma \\cdot \\phi \\cdot (N-1)`. Probability of
        giving birth is zero if
        :math:`w < \\zeta  \\cdot (w_{\\text birth } +
        \\sigma_{\\text birth })`

        :param num_animals: Number of animals of same species in cell
        :type num_animals: int
        :return: The probability for the animal to give birth.
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
        Compares probability of giving birth with a random number,
        and returns True if a baby is to be born.

        :return: True if animal shall give birth
        :rtype: bool
        """
        prob = self.prob_give_birth(num_animals)
        random_number = np.random.random()

        if random_number <= prob:
            return True

    def birth_process(self, num_animals):
        """
        Finds out if a birth should take place, and then draws baby's birth
        weight from normal distribution.
        If a birth should take place, the birth weight is returned and
        weight of mother is reduced by :math:`\\xi \\cdot birth weight`

        :return: Returns weight of the baby that is born, or None if no baby
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
            self.fitness_must_be_updated = True
            return birth_weight

    def prob_death(self):
        """
        If neccessary, first finds fitness of animal.
        Then, finds probability of death, which depends on the fitness of the
        animal.

        :return: 1 if fitness is zero, :math:`\\omega \\cdot (1 - \\phi)`
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
        Compares the probability of death with a random number, and returns
        True if the animal lives.

        :return: True if animal lives
        :rtype: bool
        """
        prob = self.prob_death()
        random_number = np.random.random()

        if random_number > prob:
            return True


class Herbivore(Animal):
    """
    Class for herbivores. Herbivores feed on plant fodder.
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

        :param properties: Contains age, weight and species of herbivore. May
            also contain fitness.
        :type properties: dict
        """
        super().__init__(properties)

    def find_rel_abund_of_fodder(self, landscape_cell):
        """
        Takes an instance of a landscape class, and returns the relative
        abundance of fodder for herbivores in that instance, given by

        .. math::

            \\epsilon = \\frac{f_k}{(n_k + 1)F^{'}}

        where :math:`f_k` is the amount of relevant fodder and :math:`n_k` is
        the number of animals of same species in cell k.

        :param landscape_cell: Instance of landscape class
        :type landscape_cell: '__main__.Jungle', '__main__.Desert',
            '__main__.Savannah'
        :return: Relative abundance of fodder
        :rtype: float
        """
        fodder_herb = landscape_cell.fodder_amount
        num_herbs = len(landscape_cell.pop_herb)
        abund_fodder_herb = fodder_herb / ((num_herbs + 1) * self.params["F"])
        return abund_fodder_herb


class Carnivore(Animal):
    """
    Class for Carnivores. Carnivores feed on herbivores.
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

        :param properties: Contains age, weight and species of carnivore. May
            also contain fitness.
        :type properties: dict
        """
        super().__init__(properties)

    def prob_kill(self, fitness_herb):
        """
        Calculates the probability of a carnivore killing a herbivore.
        Probability is given by

        .. math::

            p =
            \\Biggl
            \\lbrace
            {
            0, \\text{ if } {\\phi_{\\text { carn } } \\leq \\phi_{\\text
            { herb } } }
            \\atop
            {\\frac{\\phi_{\\text { carn }} - \\phi_{\\text { herb } } }
            {{\\Delta \\phi}_{\\text { max } } },
            \\text{ if } { 0 < \\phi_{\\text { carn }} -
            \\phi_{\\text { herb }} < {\\Delta \\phi}_{\\text { max } } }
            \\atop
            1, \\text{ otherwise }
            }}

        :param fitness_herb: Fitness of herbivore
        :type fitness_herb: float
        :return: Probability of carnivore killing a herbivore
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
        carnivore kills a herbivore or not.

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

    def attempt_eating_all_herbivores_in_cell(self, pop_herb):
        """
        Iterates through list of herbivores. Implements kill method on one
        herbivore at a time until carnivore has satisfied it's appetite or
        has tried to kill all herbivores without luck. After a carnivore has
        eaten a herbivore, it's weight and fitness is updated.

        :param pop_herb: Herbivores available to the carnivore sorted by
                fitness
        :type pop_herb: list
        :return: Herbivores killed
        :rtype: list
        """
        amount_eaten = 0
        eaten_herbivores = []
        for herb in reversed(pop_herb):
            if amount_eaten < self.params["F"] and self.kill(herb) is True:
                eaten_herbivores.append(herb)
                amount_eaten += herb.weight
                self.weight += self.params["beta"] * amount_eaten
                self.find_fitness()
                self.fitness_must_be_updated = False
        return eaten_herbivores

    def find_rel_abund_of_fodder(self, landscape_cell):
        """
        Takes an instance of a landscape class, and returns the relative
        abundance of fodder for carnivores in that instance, given by

        .. math::

            \\epsilon = \\frac{f_k}{(n_k + 1)F^{'}}

        where :math:`f_k` is the amount of relevant fodder and :math:`n_k` is
        the number of animals of same species in cell k.

        :param landscape_cell: Instance of landscape class
        :type landscape_cell: '__main__.Jungle', '__main__.Desert',
            '__main__.Savannah'
        :return: Relative abundance of fodder for the carnivore
        :rtype: float
        """
        fodder_carn = landscape_cell.available_fodder_carnivore()
        num_carns = len(landscape_cell.pop_carn)
        abund_fodder_carn = fodder_carn / ((num_carns + 1) * self.params["F"])
        return abund_fodder_carn
