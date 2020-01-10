# -*- coding: utf-8 -*-

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idaln@hotmail.com & kjkv@nmbu.no"

from biosim.animals import Animal, Herbivore


class Landscape:
    """
    Parent class for all landscape types.
    """
    params = {
        "f_max": 800,
        "alpha": None
    }

    def __init__(self, population):
        """
        Initializes class with given population.
        :param population: list of dictionaries
        """
        self.fodder_amount = None

        #pop_carn = []
        self.pop_herb = []
        for individual in population:
            if individual["species"] is "Herbivore":
                self.pop_herb.append(Herbivore(individual))
            #else:
                # pop_carn.append(Carnivore(individual))

    def sort_population_by_fitness(self):
        """
        Sorts carnivore and herbivore populations by fitness, from highest to
        lowest.
        """

    def available_fodder_herb(self, herbivore):
        """
        Returns amount of fodder available to the herbivore.
        :return available_fodder: float
        """
        desired_fodder = herbivore.params["F"]
        old_fodder = self.fodder_amount
        if self.fodder_amount >= desired_fodder:
            self.fodder_amount -= desired_fodder
            return desired_fodder
        elif 0 < self.fodder_amount < desired_fodder:
            self.fodder_amount = 0
            return old_fodder
        else:
            return 0

    def feed_all_animals(self):
        """
        Iterates over populations and feeds all animals, utilizing the eating
        method inherent to the animal instance.

        """

    def attemps_procreating_all_animals(self):
        """
        Iterates over population lists and makes animal procreate utilizing
        their inherent birth process method.
        """

    def move_all_animals(self):
        """
        Iterates over population lists and moves animals utilizing heir
        inherent migration method.
        """
        pass

    def make_all_animals_older(self):
        """
        Iterates over population lists and ages all animals one year
        utilizing their inherent aging method.
        """

    def make_all_animals_lose_weight(self):
        """
        Iterates over population lists and makes all animals lose weight
        utilizing their inherent weight loss method.
        """

    def attempt_dying_all_animals(self):
        """
        Iterates over population lists and runs inherent death method on all
        animals.
        """


class Jungle(Landscape):
    """
    Class for Jungle landscape type.
    """
    params = {
        "f_max": 800,
    }
    pop_carn = []
    pop_herb = []

    def __init__(self, population):
        """
        Initializes class.
        """
        super().__init__(population)
        self.fodder_amount = None
        self.num_carn = len(self.pop_carn)
        self.num_herb = len(self.pop_herb)

    def regrowth(self):
        """
        Sets amount of fodder for herbivores to maximum at the beginning of
        each year.
        """
        self.fodder_amount = self.params['f_max']
