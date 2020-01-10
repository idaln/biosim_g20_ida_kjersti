# -*- coding: utf-8 -*-

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idaln@hotmail.com & kjkv@nmbu.no"

from biosim.landscape import Landscape, Jungle
from biosim.animals import Animal, Herbivore
from pytest import approx
import numpy as np

test_properties_herb = {
    "species": "animal",
    "age": 5,
    "weight": 20
}

test_population = [
                    {"species": "Herbivore", "age": 1, "weight": 10.0},
                    {"species": "Herbivore", "age": 3, "weight": 50.0},
                    {"species": "Herbivore", "age": 5, "weight": 20.0},

]


class TestLandscape:
    """
    Tests for Landscape class
    """
    def test_constructor(self):
        """
        Asserts that the Landscape class enables creation of class
        instances and it's population attribute has correct length.
        """
        l = Landscape(test_population)
        assert isinstance(l, Landscape)
        assert len(l.pop_herb) == len(test_population)

    def test_sort_single_animal_by_fitness(self):
        """
        Tests that the sorting function works for a single-element list.
        """
        l = Landscape([{"species": "Herbivore", "age": 1, "weight": 10.0}])
        l.sort_population_by_fitness()
        assert l.pop_herb[0].fitness == approx(0.49979521641750696)

    def test_sort_several_animals_by_fitness(self):
        """
        Tests that the sorting method works on a list of several herbivores.
        """
        l = Landscape(test_population)
        l.sort_population_by_fitness()
        assert l.pop_herb[0].fitness > l.pop_herb[1].fitness
        assert l.pop_herb[1].fitness > l.pop_herb[2].fitness

    def test_regrowth(self):
        """
        Asserts that amount of fodder is equal f_max after each year.
        """
        l = Landscape(test_population)
        l.regrowth()
        assert l.fodder_amount == l.params['f_max']

    def test_enough_fodder_is_available(self):
        """
        Asserts that herbivore is provided with the amount it desires, when
        enough fodder is available. Asserts that the amount of fodder
        provided is substracted from the initial fodder amount.
        """
        l = Landscape(test_population)
        l.regrowth()
        old_fodder_amount = l.fodder_amount
        available_fodder_to_herb = l.available_fodder_herb()
        assert available_fodder_to_herb == Herbivore.params["F"]
        assert l.fodder_amount == old_fodder_amount - available_fodder_to_herb

    def test_restricted_amount_of_fodder_is_available(self):
        """
        Asserts that all of the fodder is provided to the herbivore when it's
        demand is larger than the amount of fodder available. Asserts that
        the amount of fodder left now is zero.
        """
        l = Landscape(test_population)
        l.fodder_amount = Herbivore.params["F"] / 2
        old_fodder_amount = l.fodder_amount
        available_fodder_to_herb = l.available_fodder_herb()
        assert available_fodder_to_herb == Herbivore.params["F"] / 2
        assert l.fodder_amount == old_fodder_amount - available_fodder_to_herb

    def test_no_fodder_available(self):
        """
        Asserts that no fodder is provided to the herbivore when there is no
        fodder available.
        """
        l = Landscape(test_population)
        l.fodder_amount = 0
        assert l.available_fodder_herb() == 0
        assert l.fodder_amount == 0

    def test_have_all_animals_been_fed(self):
        """
        Tests that all animals have gained weight in a situation where there
        is plenty of food available.
        """
        l = Landscape(test_population)
        l.feed_all_herbivores()
        assert l.pop_herb[0].weight > test_population[1]["weight"]
        assert l.pop_herb[1].weight > test_population[2]["weight"]
        assert l.pop_herb[2].weight > test_population[0]["weight"]

    def test_fittest_animal_eats_first(self):
        """
        Tests that the strongest animal has eaten first, in a situation
        where there is a limited supply of food.
        """
        l = Landscape(test_population)
        l.params["f_max"] = Herbivore.params["F"]
        l.feed_all_herbivores()
        assert l.pop_herb[0].weight > test_population[1]["weight"]
        assert l.pop_herb[1].weight == test_population[2]["weight"]
        assert l.pop_herb[2].weight == test_population[0]["weight"]

    def test_newborn_animals_have_been_created(self):
        """
        Asserts that in a situastion when all animals will give birth,
        the population list has been updated with the right number of animals.
        """
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
        assert len(l.pop_herb) == 2 * len(test_population)

    def test_have_all_animals_aged(self):
        """
        Test that all animals in the population has aged by one year.
        """
        l = Landscape(test_population)
        l.make_all_animals_older()
        assert l.pop_herb[0].age == test_population[0]["age"] + 1
        assert l.pop_herb[1].age == test_population[1]["age"] + 1
        assert l.pop_herb[2].age == test_population[2]["age"] + 1

    def test_have_all_animals_lost_weight(self):
        """
        Test that all animals in the population has lost some weight.
        """
        l = Landscape(test_population)
        l.make_all_animals_lose_weight()
        assert l.pop_herb[0].weight < test_population[0]["weight"]
        assert l.pop_herb[1].weight < test_population[1]["weight"]
        assert l.pop_herb[2].weight < test_population[2]["weight"]


class TestJungle:
    """
    Tests for Jungle class.
    """
    def test_constructor(self):
        """
        Asserts that class instance has been initialized with no fodder
        available.
        """
        j = Jungle(test_population)
        assert j.fodder_amount is None

