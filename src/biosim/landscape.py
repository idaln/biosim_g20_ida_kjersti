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
        self.fodder_amount = 0

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

    def add_newborn_animals(self):
        """
        Iterates over population lists and makes animal procreate utilizing
        their inherent birth process method.
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
        for animal in self.pop_herb:
            animal.make_animal_one_year_older()

    def make_all_animals_lose_weight(self):
        """
        Iterates over population lists and makes all animals lose weight
        utilizing their inherent weight loss method.
        """
        for animal in self.pop_herb:
            animal.weight_loss()

    def remove_all_dead_animals(self):
        """
        Iterates over population lists and runs inherent death method on all
        animals. Updates the population to only contain living animals.
        """
        self.pop_herb = [animal for animal in self.pop_herb
                         if animal.will_animal_live() is True]


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


class Savannah(Landscape):
    """
    Class for Savannah landscape type.
    """
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


if __name__ == "__main__":
    import numpy
    test_population = [
        {"species": "Herbivore", "age": 1, "weight": 10.0},
        {"species": "Herbivore", "age": 3, "weight": 50.0},
        {"species": "Herbivore", "age": 5, "weight": 20.0},
    ]
    numpy.random.seed(1)
    j = Jungle(test_population)
    for year in range(0):
        j.feed_all_herbivores()
        j.add_newborn_animals()
        j.make_all_animals_older()
        j.make_all_animals_lose_weight()
        j.remove_all_dead_animals()
        print(len(j.pop_herb))
    print(j.pop_herb)


    test_population = [
        {"species": "Herbivore", "age": 1, "weight": 10.0}
    ]
    test_properties = {
        "species": "Herbivore",
        "age": 1,
        "weight": 10
    }
    dict_of_neighbours = {(1, 2): Jungle(test_population),
                          (2, 1): Jungle(test_population),
                          (2, 3): Jungle(test_population),
                          (3, 2): Jungle(test_population)
                          }
    for jungle in dict_of_neighbours.values():
        jungle.regrowth()
    animal = Animal(test_properties)
    print(animal.prob_move_to_each_neighbour(dict_of_neighbours))
    for v in animal.prob_move_to_each_neighbour(dict_of_neighbours).values():
        print (type(v))
