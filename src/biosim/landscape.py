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
        """
        Returns a copy of the default landscape parameters.

        :return: Copy of default landscape parameters
        :rtype: dict
        """
        return cls._DEFAULT_PARAMS.copy()

    @classmethod
    def reset_params(cls):
        """
        Sets the landscape parameters equal to default.
        """
        cls.params = cls.GET_DEFAULT_PARAMS()

    def __init__(self, population):
        """
        Initializes class with given population. Creates instances of
        correct species for all elements in population list, and adds the
        instances to correct population list.

        :param population: Contains dictionaries containing
            information about each animal
        :type population: list
        """
        self.fodder_amount = 0
        self.pop_carn = []
        self.pop_herb = []
        
        for animal_info in population:
            if animal_info["species"] is "Herbivore":
                self.pop_herb.append(Herbivore(animal_info))
            else:
                self.pop_carn.append(Carnivore(animal_info))

    def sort_herb_population_by_fitness(self):
        """
        Sorts herbivore population by fitness, from highest to
        lowest. Uses lambda sorting.
        """
        for herb in self.pop_herb:
            if herb.fitness_must_be_updated is True:
                herb.find_fitness()
        self.pop_herb = sorted(self.pop_herb, key=lambda x: x.fitness,
                               reverse=True)

    def sort_carn_population_by_fitness(self):
        """
        Sorts carnivore population by fitness, from highest to
        lowest. Uses lambda sorting.
        """
        for carn in self.pop_carn:
            if carn.fitness_must_be_updated is True:
                carn.find_fitness()
        self.pop_carn = sorted(self.pop_carn, key=lambda x: x.fitness,
                               reverse=True)

    def regrowth(self):
        """
        Sets amount of fodder for herbivores to maximum.
        """
        self.fodder_amount = self.params["f_max"]

    def available_fodder_herbivore(self):
        """
        Returns amount of fodder available to an herbivore. If plenty of fodder
        is available in the cell, enough fodder will be returned to fulfill
        it's appetite F. If not, what's left will be returned.

        :return: Amount of fodder available to an herbivore.
        :rtype: float
        """
        desired_fodder_amount = Herbivore.params["F"]
        previous_fodder_amount = self.fodder_amount
        if self.fodder_amount >= desired_fodder_amount:
            self.fodder_amount -= desired_fodder_amount
            return desired_fodder_amount
        elif 0 < self.fodder_amount < desired_fodder_amount:
            self.fodder_amount = 0
            return previous_fodder_amount
        else:
            return 0

    def available_fodder_carnivore(self):
        """
        Returns amount of fodder available to a carnivore. That is, the total
        weight of the herbivores in the cell.

        :return: Amount of fodder available to a carnivore.
        :rtype: float
        """
        available_fodder_amount = 0
        for herb in self.pop_herb:
            available_fodder_amount += herb.weight
        return available_fodder_amount

    def feed_all_herbivores(self):
        """
        Updates fodder amount of the cell and sorts the herbivore population.
        Then, iterates over the population of herbivores and feeds all,
        utilizing the eating method.
        """
        self.regrowth()
        self.sort_herb_population_by_fitness()
        for herb in self.pop_herb:
            herb.add_eaten_fodder_to_weight(self.available_fodder_herbivore())

    def feed_all_carnivores(self):
        """
        Sorts carnivore population in the cell. Then, iterates over the
        carnivores and feeds them all, using their eating method.
        """
        self.sort_carn_population_by_fitness()
        for carn in self.pop_carn:
            self.sort_herb_population_by_fitness()
            eaten_herbivores = carn.eat(self.pop_herb)
            self.remove_all_eaten_herbivores(eaten_herbivores)

    def remove_all_eaten_herbivores(self, eaten_herbivores):
        """
        Removes herbivores that have been eaten from the
        herbivore population of the cell.

        :param eaten_herbivores: Herbivore instances that have been eaten
            during feeding of a carnivore.
        :type eaten_herbivores: list
        """
        self.pop_herb = [herb for herb in self.pop_herb
                         if herb not in eaten_herbivores]

    def add_newborn_animals(self):
        """
        Iterates over both population lists of grown animals, in turn, and
        makes all animals procreate using the animal's birth_process_method.
        If birth_process returns a weight, a new animal will be born.
        Thus, a new class instance is added to the
        correct population list.
        """
        initial_num_herbs = len(self.pop_herb)
        for animal in self.pop_herb[:initial_num_herbs]:
            baby_weight = animal.birth_process(initial_num_herbs)
            if type(baby_weight) is (float or int):
                self.pop_herb.append(
                    Herbivore({"species": "Herbivore",
                               "age": 0,
                               "weight": baby_weight})
                )
                self.pop_herb[-1].fitness_must_be_updated = True

        initial_num_carns = len(self.pop_carn)
        for animal in self.pop_carn[:initial_num_carns]:
            baby_weight = animal.birth_process(initial_num_carns)
            if type(baby_weight) is (float or int):
                self.pop_carn.append(
                    Carnivore({"species": "Carnivore",
                               "age": 0,
                               "weight": baby_weight})
                )
                self.pop_carn[-1].fitness_must_be_updated = True

    def make_all_animals_older(self):
        """
        Iterates over population lists and ages all animals one year.
        """
        for animal in (self.pop_herb + self.pop_carn):
            animal.make_animal_one_year_older()

    def make_all_animals_lose_weight(self):
        """
        Iterates over population lists and makes all animals lose weight.
        """
        for animal in (self.pop_herb + self.pop_carn):
            animal.weight_loss()

    def remove_all_dead_animals(self):
        """
        Iterates over population lists and runs the death method of all the
        animals. Updates the population lists to only contain living animals.
        """
        self.pop_herb = [herb for herb in self.pop_herb
                         if herb.will_animal_live() is True]
        self.pop_carn = [carn for carn in self.pop_carn
                         if carn.will_animal_live() is True]


class Jungle(Landscape):
    """
    Class for Jungle landscape type. All animals can stay in this landscape
    type, and there is food for herbivores.
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

        :param population: Contains dictionaries with
            information about each animal.
        :type population: list
        """
        super().__init__(population)


class Savannah(Landscape):
    """
    Class for Savannah landscape type. All animals can stay in this landscape
    type, and there is food for herbivores.
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

        :param population: Contains dictionaries with
            information about each animal.
        :type population: list
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
    Class for Desert landscape type. All animals can stay in this
    landscape type, but there is no food for herbivores.
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

        :param population: Contains dictionaries with
            information about each animal.
        :type population: list
        """
        super().__init__(population)


class Mountain(Landscape):
    """
    Class for Mountain landscape type.  This is a passive class where animals
    cannot stay, so no inherited methods should be used.
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

        :param population: Contains dictionaries with
            information about each animal. Should be empty.
        :type population: list
        """
        super().__init__(population)


class Ocean(Landscape):
    """
    Class for Ocean landscape type. This is a passive class where animals
    cannot stay, so no inherited methods should be used.
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

        :param population: Contains dictionaries with
            information about each animal. Should be empty.
        :type population: list
        """
        super().__init__(population)
