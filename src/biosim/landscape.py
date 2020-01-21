# -*- coding: utf-8 -*-

"""
This module provides classes implementing landscape types for the Island.
"""

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idaln@hotmail.com & kjkv@nmbu.no"

from biosim.animals import Herbivore, Carnivore


class Landscape:
    """
    Parent class for all landscape types.
    """
    _DEFAULT_PARAMS = {
        "f_max": 800,
        "alpha": None
    }

    params = {
        "f_max": 800,
        "alpha": None
    }

    @classmethod
    def GET_DEFAULT_PARAMS(cls):
        return cls._DEFAULT_PARAMS.copy()

    @classmethod
    def reset_params(cls):
        cls.params = cls.GET_DEFAULT_PARAMS()

    def __init__(self, population):
        """Initializes class with given population.
        :param population: A list containing dictionaries containing
        information about each animal
        :type population: list
        """
        self.fodder_amount = 0
        self.pop_carn = []
        self.pop_herb = []
        
        for individual in population:
            if individual["species"] is "Herbivore":
                self.pop_herb.append(Herbivore(individual))
            else:
                self.pop_carn.append(Carnivore(individual))

    def sort_herb_population_by_fitness(self):
        """
        Sorts herbivore populations by fitness, from highest to
        lowest. Uses lambda sorting.
        """
        for individual in self.pop_herb:
            if individual.fitness_must_be_updated is True:
                individual.find_fitness()
        self.pop_herb = sorted(self.pop_herb, key=lambda x: x.fitness,
                               reverse=True)

    def sort_carn_population_by_fitness(self):
        """
        Sorts carnivore population by fitness, from highest to
        lowest. Uses lambda sorting.
        """
        for individual in self.pop_carn:
            if individual.fitness_must_be_updated is True:
                individual.find_fitness()
        self.pop_carn = sorted(self.pop_carn, key=lambda x: x.fitness,
                               reverse=True)

    def regrowth(self):
        """
        Sets amount of fodder for herbivores to maximum at the beginning of
        each year.
        """
        self.fodder_amount = self.params["f_max"]

    def available_fodder_herbivore(self):
        """
        Returns amount of fodder available to the herbivore.
        :return available_fodder: float
        """
        desired_fodder = Herbivore.params["F"]
        old_fodder = self.fodder_amount
        if self.fodder_amount >= desired_fodder:
            self.fodder_amount -= desired_fodder
            return desired_fodder
        elif 0 < self.fodder_amount < desired_fodder:
            self.fodder_amount = 0
            return old_fodder
        else:
            return 0

    def available_fodder_carnivore(self):
        """
        Returns amount of fodder available to carnivore. That is, the total
        weight of the herbivores in the cell.
        """
        available_fodder = 0
        for herb in self.pop_herb:
            available_fodder += herb.weight
        return available_fodder

    def feed_all_herbivores(self):
        """
        Iterates over the population of herbivores and feeds all animals,
        utilizing the eating method inherent to the animal instance.
        """
        self.regrowth()
        self.sort_herb_population_by_fitness()
        for herb in self.pop_herb:
            herb.add_eaten_fodder_to_weight(self.available_fodder_herbivore())

    def remove_all_eaten_herbivores(self, eaten_herbivores):
        """
        Removed herbivores that have been eaten from pop_herb
        :param eaten_herbivores: list
                List of herbivores that have been eaten
        """
        self.pop_herb = [herb for herb in self.pop_herb
                         if herb not in eaten_herbivores]

    def feed_all_carnivores(self):
        """
        Iterates over the population of carnivores in the cell, and feeds all
        carnivores using their inherent eating method.
        """
        self.sort_carn_population_by_fitness()
        for carn in self.pop_carn:
            self.sort_herb_population_by_fitness()
            eaten_herbivores = carn.eat(self.pop_herb)
            self.remove_all_eaten_herbivores(eaten_herbivores)

    def add_newborn_animals(self):
        """
        Iterates over both population lists in turn,
        and makes all animal procreate utilizing their
        inherent birth process method.
        """
        num_animals = len(self.pop_herb)
        for animal in self.pop_herb[:num_animals]:
            baby_weight = animal.birth_process(num_animals)
            if type(baby_weight) is (float or int):
                self.pop_herb.append(
                    Herbivore({"species": "Herbivore",
                               "age": 0,
                               "weight": baby_weight})
                )

        num_animals = len(self.pop_carn)
        for animal in self.pop_carn[:num_animals]:
            baby_weight = animal.birth_process(num_animals)
            if type(baby_weight) is (float or int):
                self.pop_carn.append(
                    Carnivore({"species": "Carnivore",
                               "age": 0,
                               "weight": baby_weight})
                )

    def make_all_animals_older(self):
        """
        Iterates over population lists and ages all animals one year
        utilizing their inherent aging method.
        """
        for animal in (self.pop_herb + self.pop_carn):
            animal.make_animal_one_year_older()

    def make_all_animals_lose_weight(self):
        """
        Iterates over population lists and makes all animals lose weight
        utilizing their inherent weight loss method.
        """
        for animal in (self.pop_herb + self.pop_carn):
            animal.weight_loss()

    def remove_all_dead_animals(self):
        """
        Iterates over population lists and runs inherent death method on all
        animals. Updates the population to only contain living animals.
        """
        self.pop_herb = [animal for animal in self.pop_herb
                         if animal.will_animal_live() is True]
        self.pop_carn = [animal for animal in self.pop_carn
                         if animal.will_animal_live() is True]


class Jungle(Landscape):
    """
    Class for Jungle landscape type.
    """
    _DEFAULT_PARAMS = {
        "f_max": 800,
    }

    params = {
        "f_max": 800,
    }

    def __init__(self, population):
        """
        Initializes class.
        """
        super().__init__(population)


class Savannah(Landscape):
    """
    Class for Savannah landscape type.
    """
    _DEFAULT_PARAMS = {
        "f_max": 300,
        "alpha": 0.3
    }

    params = {
        "f_max": 300,
        "alpha": 0.3
    }

    def __init__(self, population):
        """
        Initializes class.
        :param population: list of dicts
                 List of properties of the initial population of animals
        """
        super().__init__(population)

    def regrowth(self):
        """
        Sets amount of fodder for herbivores to the value given by formula (1).
        """
        self.fodder_amount = ((1 - self.params["alpha"]) * self.fodder_amount)\
            + (self.params["alpha"] * self.params["f_max"])


class Desert(Landscape):
    """
    Class for Desert landscape type.
    """
    _DEFAULT_PARAMS = {
        "f_max": 0
    }

    params = {
        "f_max": 0
    }

    def __init__(self, population):
        """
        Initializes class.
        :param population: list of dicts
                 List of properties of the initial population of animals
        """
        super().__init__(population)


class Mountain(Landscape):
    """
    Class for Mountain landscape type.
    """
    _DEFAULT_PARAMS = {
        "f_max": 0
    }

    params = {
        "f_max": 0
    }

    def __init__(self, population):
        """
        Initializes class.
        :param population: list of dicts
                 List of properties of the initial population of animals.
                 Should be empty.
        """
        super().__init__(population)


class Ocean(Landscape):
    """
    Class for Ocean landscape type.
    """
    _DEFAULT_PARAMS = {
        "f_max": 0
    }

    params = {
        "f_max": 0
    }

    def __init__(self, population):
        """
        Initializes class.
        :param population: list of dicts
                 List of properties of the initial population of animals.
                 Should be empty.
        """
        super().__init__(population)
