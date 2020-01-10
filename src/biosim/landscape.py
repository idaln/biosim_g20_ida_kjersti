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
        lowest. Uses the Bubble Sort algorithm.
        """
        for individual in self.pop_herb:
            individual.find_fitness()
        n = len(self.pop_herb)
        while n > 0:
            i = 1
            while i < n:
                if self.pop_herb[i].fitness > self.pop_herb[i - 1].fitness:
                    self.pop_herb[i], self.pop_herb[i - 1] = \
                        self.pop_herb[i - 1], self.pop_herb[i]
                i += 1
            n -= 1

    def regrowth(self):
        """
        Sets amount of fodder for herbivores to maximum at the beginning of
        each year.
        """
        self.fodder_amount = self.params['f_max']

    def available_fodder_herb(self):
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

    def feed_all_herbivores(self):
        """
        Iterates over populations and feeds all animals, utilizing the eating
        method inherent to the animal instance.
        """
        self.regrowth()
        self.sort_population_by_fitness()
        for herb in self.pop_herb:
            herb.add_eaten_fodder_to_weight(self.available_fodder_herb())

    def attemps_procreating_all_animals(self):
        """
        Iterates over population lists and makes animal procreate utilizing
        their inherent birth process method.
        """
        num_animals = len(self.pop_herb)
        for animal in self.pop_herb[:num_animals]:
            baby_weight = animal.birth_process(num_animals)
            if type(baby_weight) is (float or int):
                self.pop_herb.append({"species": "Herbivore", "age": 0,
                                      "weight": baby_weight})

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

    def __init__(self, population):
        """
        Initializes class.
        """
        super().__init__(population)


if __name__ == "__main__":
    import numpy as np
    np.random.seed(1)
    test_population = [
        {"species": "Herbivore", "age": 2, "weight": 70.0},
        {"species": "Herbivore", "age": 3, "weight": 90.0},
        {"species": "Herbivore", "age": 3, "weight": 70.0},
        {"species": "Herbivore", "age": 3, "weight": 80.0},
        {"species": "Herbivore", "age": 3, "weight": 60.0},
        {"species": "Herbivore", "age": 5, "weight": 90.0}
    ]

    l = Landscape(test_population)
    for animal in l.pop_herb:
        animal.find_fitness()
    l.attemps_procreating_all_animals()
    print()
