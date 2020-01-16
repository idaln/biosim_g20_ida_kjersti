# -*- coding: utf-8 -*-

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idaln@hotmail.com & kjkv@nmbu.no"

from biosim.landscape import Landscape, Jungle, Savannah, Desert, Mountain, \
    Ocean
from biosim.animals import Herbivore
from pytest import approx
import pytest
import numpy


class TestLandscape:
    """
    Tests for Landscape class
    """
    @pytest.fixture
    def example_pop_herb(self):
        return [
            {"species": "Herbivore", "age": 1, "weight": 10.0},
            {"species": "Herbivore", "age": 3, "weight": 50.0},
            {"species": "Herbivore", "age": 5, "weight": 20.0}
         ]

    @pytest.fixture
    def example_pop_carn(self):
        return [
            {"species": "Carnivore", "age": 1, "weight": 10.0},
            {"species": "Carnivore", "age": 3, "weight": 50.0},
            {"species": "Carnivore", "age": 5, "weight": 20.0}
        ]

    @pytest.fixture
    def example_properties_herb(self):
        return {
                "species": "Herbivore",
                "age": 5,
                "weight": 20
         }

    @pytest.fixture
    def setup_for_feed_test(self):
        """
        Sets up parameters for test_fittest_animal_eats_first method.
        """
        landscape_params = Landscape.params.copy()
        yield None
        Landscape.params = landscape_params

    def test_constructor(self, example_pop_herb):
        """
        Asserts that the Landscape class enables creation of class
        instances and it's population attribute has correct length.
        """
        landscape = Landscape(example_pop_herb)
        assert isinstance(landscape, Landscape)
        assert len(landscape.pop_herb) == len(example_pop_herb)

    def test_sort_single_animal_by_fitness(self):
        """
        Tests that the sorting function works for a single-element list.
        """
        landscape = Landscape([{"species": "Herbivore", "age": 1,
                                "weight": 10.0}])
        landscape.sort_herb_population_by_fitness()
        assert landscape.pop_herb[0].fitness == approx(0.49979521641750696)

    def test_sort_several_herbivores_by_fitness(self, example_pop_herb):
        """
        Tests that the sorting method works on a list of several herbivores.
        """
        landscape = Landscape(example_pop_herb)
        landscape.sort_herb_population_by_fitness()
        assert landscape.pop_herb[0].fitness > landscape.pop_herb[1].fitness
        assert landscape.pop_herb[1].fitness > landscape.pop_herb[2].fitness

    def test_sort_several_carnivores_by_fitness(self, example_pop_carn):
        """
        Tests that the sorting method works on a list of several herbivores.
        """
        landscape = Landscape(example_pop_carn)
        landscape.sort_carn_population_by_fitness()
        assert landscape.pop_carn[0].fitness > landscape.pop_carn[1].fitness
        assert landscape.pop_carn[1].fitness > landscape.pop_carn[2].fitness

    def test_regrowth(self, example_pop_herb):
        """
        Asserts that amount of fodder is equal f_max after each year.
        """
        landscape = Landscape(example_pop_herb)
        landscape.regrowth()
        assert landscape.fodder_amount == landscape.params["f_max"]

    def test_enough_fodder_is_available(self, example_pop_herb):
        """
        Asserts that herbivore is provided with the amount it desires, when
        enough fodder is available. Asserts that the amount of fodder
        provided is subtracted from the initial fodder amount.
        """
        landscape = Landscape(example_pop_herb)
        landscape.regrowth()
        old_fodder_amount = landscape.fodder_amount
        available_fodder_to_herb = landscape.available_fodder_herbivore()
        assert available_fodder_to_herb == Herbivore.params["F"]
        assert landscape.fodder_amount == old_fodder_amount - \
            available_fodder_to_herb

    def test_restricted_amount_of_fodder_is_available(self, example_pop_herb):
        """
        Asserts that all of the fodder is provided to the herbivore when it's
        demand is larger than the amount of fodder available. Asserts that
        the amount of fodder left now is zero.
        """
        landscape = Landscape(example_pop_herb)
        landscape.fodder_amount = Herbivore.params["F"] / 2
        old_fodder_amount = landscape.fodder_amount
        available_fodder_to_herb = landscape.available_fodder_herbivore()
        assert available_fodder_to_herb == Herbivore.params["F"] / 2
        assert landscape.fodder_amount == old_fodder_amount - \
            available_fodder_to_herb

    def test_no_fodder_available(self, example_pop_herb):
        """
        Asserts that no fodder is provided to the herbivore when there is no
        fodder available.
        """
        landscape = Landscape(example_pop_herb)
        landscape.fodder_amount = 0
        assert landscape.available_fodder_herbivore() == 0
        assert landscape.fodder_amount == 0

    def test_correct_fodder_carn(self, example_pop_herb, example_pop_carn):
        """
        Asserts that the fodder amount available for a carnivore is calculated
        correctly.
        """
        total_pop = example_pop_herb + example_pop_carn
        landscape = Landscape(total_pop)
        assert landscape.available_fodder_carnivore() == 80
        # 80 is total weight of herbivores in example_pop_herb

    def test_eaten_herbs_have_been_removed(self, example_pop_herb):
        """
        Asserts that eaten herbivores are removed from pop_herb in landscape
        cell.
        :param example_pop_herb: list
                List of herbivores
        """
        landscape = Landscape(example_pop_herb)
        landscape.remove_all_eaten_herbivores(landscape.pop_herb)
        assert len(landscape.pop_herb) == 0

    def test_carnivores_have_been_fed(self,example_pop_herb, example_pop_carn,
                                      mocker):
        """
        Assert that carnivore gains weight after eating, and that the eaten
        herbivore is removed from population.
        """
        # Adds one strong carnivore and one weak herbivore to population.
        landscape = Landscape([example_pop_herb[0]] + [example_pop_carn[1]])
        old_weight = landscape.pop_carn[0].weight
        mocker.patch('numpy.random.random', return_value=0.00001)
        landscape.feed_all_carnivores()
        assert old_weight < landscape.pop_carn[0].weight
        assert len(landscape.pop_herb) == 0

    def test_have_all_animals_been_fed(self):
        """
        Tests that all animals have gained weight in a situation where there
        is plenty of food available.
        """
        test_population_feed = [
            {"species": "Herbivore", "age": 3, "weight": 20.0},
            {"species": "Herbivore", "age": 3, "weight": 20.0},
            {"species": "Herbivore", "age": 3, "weight": 20.0},
        ]

        landscape = Landscape(test_population_feed)
        landscape.feed_all_herbivores()
        assert landscape.pop_herb[0].weight > test_population_feed[0]["weight"]
        assert landscape.pop_herb[1].weight > test_population_feed[1]["weight"]
        assert landscape.pop_herb[2].weight > test_population_feed[2]["weight"]

    def test_fittest_animal_eats_first(
            self, setup_for_feed_test, example_pop_herb
    ):
        """
        Tests that the strongest animal has eaten first, in a situation
        where there is a limited supply of food.
        """
        landscape = Landscape(example_pop_herb)
        landscape.params["f_max"] = Herbivore.params["F"]
        landscape.feed_all_herbivores()
        assert landscape.pop_herb[0].weight > example_pop_herb[1]["weight"]
        assert landscape.pop_herb[1].weight == example_pop_herb[2]["weight"]
        assert landscape.pop_herb[2].weight == example_pop_herb[0]["weight"]

    def test_newborn_animals_have_been_created(self):
        """
        Asserts that in a situation when all animals will give birth,
        the population list has been updated with the right number of animals.
        """
        numpy.random.seed(1)
        test_population_birth = [
            {"species": "Herbivore", "age": 2, "weight": 70.0},
            {"species": "Herbivore", "age": 3, "weight": 90.0},
            {"species": "Herbivore", "age": 3, "weight": 70.0},
            {"species": "Herbivore", "age": 3, "weight": 80.0},
            {"species": "Herbivore", "age": 3, "weight": 60.0},
            {"species": "Herbivore", "age": 5, "weight": 90.0}
        ]
        landscape = Landscape(test_population_birth)
        for animal in landscape.pop_herb:
            animal.find_fitness()
        landscape.add_newborn_animals()
        assert len(landscape.pop_herb) == 2 * len(test_population_birth)

    def test_have_all_animals_aged(self, example_pop_herb):
        """
        Test that all animals in the population has aged by one year.
        """
        landscape = Landscape(example_pop_herb)
        landscape.make_all_animals_older()
        assert landscape.pop_herb[0].age == example_pop_herb[0]["age"] + 1
        assert landscape.pop_herb[1].age == example_pop_herb[1]["age"] + 1
        assert landscape.pop_herb[2].age == example_pop_herb[2]["age"] + 1

    def test_have_all_animals_lost_weight(self, example_pop_herb):
        """
        Test that all animals in the population has lost some weight.
        """
        landscape = Landscape(example_pop_herb)
        landscape.make_all_animals_lose_weight()
        assert landscape.pop_herb[0].weight < example_pop_herb[0]["weight"]
        assert landscape.pop_herb[1].weight < example_pop_herb[1]["weight"]
        assert landscape.pop_herb[2].weight < example_pop_herb[2]["weight"]

    def test_has_dead_animal_been_removed(self):
        """
        Tests that a dead animal has been removed from population list because
        it has fitness equal to zero due to no weight.
        """
        numpy.random.seed(1)
        test_population = [
            {"species": "Herbivore", "age": 1, "weight": 10.0},
            {"species": "Herbivore", "age": 3, "weight": 50.0},
            {"species": "Herbivore", "age": 5, "weight": 0},
        ]
        landscape = Landscape(test_population)
        for animal in landscape.pop_herb:
            animal.find_fitness()
        landscape.remove_all_dead_animals()
        assert len(landscape.pop_herb) == 2


class TestJungle:
    """
    Tests for Jungle class.
    """
    def test_constructor(self):
        """
        Asserts that class instance has been initialized with no fodder
        available.
        """
        test_pop_jungle = [
            {"species": "Herbivore", "age": 1, "weight": 10.0},
            {"species": "Herbivore", "age": 3, "weight": 50.0},
            {"species": "Herbivore", "age": 5, "weight": 20.0}
        ]
        jungle = Jungle(test_pop_jungle)
        assert jungle.fodder_amount == 0


class TestSavannah:
    """
    Tests for Savannah class.
    """
    @pytest.fixture
    def example_pop_herb(self):
        return [
            {"species": "Herbivore", "age": 1, "weight": 10.0},
            {"species": "Herbivore", "age": 3, "weight": 50.0},
            {"species": "Herbivore", "age": 5, "weight": 20.0}
         ]

    def test_regrowth_savannah(self, example_pop_herb):
        """
        Asserts that the amount of fodder has been updated correctly after
        one year.
        """
        savannah = Savannah(example_pop_herb)
        savannah.regrowth()
        assert savannah.fodder_amount == 90

    def test_constructor(self, example_pop_herb):
        """
        Asserts that Savannah class enables initiation of class instances.
        :param example_pop_herb: list
        """
        savannah = Savannah(example_pop_herb)
        assert isinstance(savannah, Savannah)

class TestDesert:
    @pytest.fixture
    def example_pop_herb(self):
        return [
            {"species": "Herbivore", "age": 1, "weight": 10.0},
            {"species": "Herbivore", "age": 3, "weight": 50.0},
            {"species": "Herbivore", "age": 5, "weight": 20.0}
         ]

    def test_constructor(self, example_pop_herb):
        """
        Asserts that Desert class enables initiation of class instances.
        :param example_pop_herb: list
        """
        desert = Desert

