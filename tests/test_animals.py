# -*- coding: utf-8 -*-
import pytest

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idaln@hotmail.com & kjkv@nmbu.no"

from biosim.animals import Animal, Herbivore, Carnivore
from biosim.landscape import Jungle
from pytest import approx
import numpy


class TestAnimal:
    """
    Tests for Animal class.
    """
    @pytest.fixture
    def example_properties(self):
        return {
            "species": "animal",
            "age": 5,
            "weight": 20
        }

    @pytest.fixture
    def example_properties_w_40(self):
        return {
            "species": "animal",
            "age": 5,
            "weight": 40
        }

    @pytest.fixture
    def example_population(self):
        return [
            {"species": "Herbivore", "age": 1, "weight": 10.0},
            {"species": "Herbivore", "age": 1, "weight": 10.0},
            {"species": "Herbivore", "age": 1, "weight": 10.0}
        ]

    def test_constructor(self, example_properties):
        """
        Checks that class has been initialized and some parameters have
        been unpacked correctly.
        """
        # Animal.params = test_params
        # Det her går ann, men da må alle tester endres
        a = Animal(example_properties)
        assert a.age == 5
        assert a.params['a_half'] == 60
        assert a.params['omega'] == 0.9

    def test_is_animal_one_year_older(self, example_properties):
        """
        Checks that animal is one year older than last year.
        """
        a = Animal(example_properties)
        initial_age = a.age
        a.make_animal_one_year_older()
        assert a.age - initial_age == 1

    def test_has_animal_lost_weight(self, example_properties):
        """
        Checks that weight after weight loss is less than initial weight
        """
        a = Animal(example_properties)
        initial_weight = a.weight
        a.weight_loss()
        assert a.weight < initial_weight

    def test_has_animal_gained_weight(self, example_properties):
        """
        Checks that animal has gained weight after eating.
        """
        a = Animal(example_properties)
        test_fodder = 8
        initial_weight = a.weight
        a.add_eaten_fodder_to_weight(test_fodder)
        assert a.weight > initial_weight

    def test_fitness_between_zero_and_one(self, example_properties):
        """
        Checks that fitness is between 0 and 1.
        """
        a = Animal(example_properties)
        a.find_fitness()
        assert 0 <= a.fitness <= 1

    def test_fitness_zero_if_weight_zero(self):
        """
        Checks that fitness is zero if weight is zero.
        """
        test_properties_zero_fitness = {
            "species": "animal",
            "age": 5,
            "weight": 0
        }
        a = Animal(test_properties_zero_fitness)
        a.find_fitness()
        assert a.fitness == 0

    def test_correct_fitness(self, example_properties):
        """
        Checks that fitness formula yields correct value.
        """
        a = Animal(example_properties)
        a.find_fitness()
        assert a.fitness == approx(0.9983411986)

    def test_correct_prob_of_moving(self, example_properties):
        """
        Asserts that method calculates the probability of moving correctly.
        """
        animal = Animal(example_properties)
        animal.find_fitness()
        assert animal.prob_of_animal_moving() == approx(0.3993364794)

    def test_correct_bool_of_moving(self, example_properties, mocker):
        """
        Asserts that method returns True when a certain random number
        is drawn.
        """
        mocker.patch('numpy.random.random', return_value=0.1)
        animal = Animal(example_properties)
        animal.fitness = 1
        assert animal.will_animal_move() is True

    def test_prob_give_birth_one_animal_in_square(self, example_properties):
        """
        Asserts that if there is only one animal in the square, then the
        probability of giving birth is zero.
        """
        a = Animal(example_properties)
        a.find_fitness()
        assert a.prob_give_birth(num_animals=1) == 0

    def test_prob_give_birth_weight_less_than_limit(self, example_properties):
        """
        Asserts that probability of giving birth is zero if the mothers
        weight is less than a given limit.
        """
        a = Animal(example_properties)
        a.find_fitness()
        assert a.prob_give_birth(num_animals=6) == 0

    def test_correct_birth_prob(self, example_properties_w_40):
        """
        Asserts that the calculated probability is correct.
        """
        a = Animal(example_properties_w_40)
        a.find_fitness()
        assert a.prob_give_birth(num_animals=6) == 1

    def test_birth_prob_is_one(self, example_properties_w_40):
        """
        Tests will_birth_take_place method.
        Checks if True is returned if probability of giving birth is 1.
        """
        a = Animal(example_properties_w_40)
        a.find_fitness()
        assert a.will_birth_take_place(num_animals=6) is True

    def test_num_more_than_birth_prob(self, mocker):
        """
        Tests will_birth_take_place method.
        Checks if False is returned if random number larger than the
        probability is drawn.
        """
        test_properties_prob = {
            "species": "animal",
            "age": 63,
            "weight": 30
        }
        mocker.patch('numpy.random.random', return_value=0.95)
        a = Animal(test_properties_prob)
        a.find_fitness()
        assert a.will_birth_take_place(num_animals=6) is not True

    def test_num_less_than_birth_prob(self, mocker):
        """
        Tests will_birth_take_place method.
        Checks if True is returned if random number less than the
        probability is drawn.
        """
        test_properties_num_less = {
            "species": "animal",
            "age": 63,
            "weight": 30
        }
        mocker.patch('numpy.random.random', return_value=0.8)
        a = Animal(test_properties_num_less)
        a.find_fitness()
        assert a.will_birth_take_place(num_animals=6) is True

    def test_mothers_weight_large_enough(self, example_properties_w_40,
                                         mocker):
        """
        Tests birth_process method.
        After birth, we check that no birth took place if the predicted baby
        weight times xi is larger than the mother's weight.
        """
        mocker.patch('numpy.random.normal', return_value=5.5)
        a = Animal(example_properties_w_40)
        a.find_fitness()
        assert a.weight > a.birth_process(num_animals=6) * a.params['xi']

    def test_mother_loses_weight(self, example_properties_w_40, mocker):
        """
        Test birth_process method.
        Asserts that mother loses weight equal to xi * birth weight
        """
        mocker.patch('numpy.random.normal', return_value=5.5)
        a = Animal(example_properties_w_40)
        a.find_fitness()
        initial_weight = a.weight
        birth_weight = a.birth_process(num_animals=6)
        assert a.weight == initial_weight - (a.params['xi'] * birth_weight)

    def test_birth_weight_different_from_zero(self, example_properties_w_40,
                                              mocker):
        """
        Tests birth_process method.
        Asserts that no baby is born if the baby weight is equal to zero.
        """
        mocker.patch('numpy.random.normal', return_value=0)
        a = Animal(example_properties_w_40)
        a.find_fitness()
        assert a.birth_process(num_animals=6) is None

    def test_prob_death_is_one(self):
        """
        Asserts that the probability of dying is one if fitness equals zero.
        """
        test_properties = {
            "species": "animal",
            "age": 5,
            "weight": 0
        }
        a = Animal(test_properties)
        a.find_fitness()
        assert a.prob_death() == 1

    def test_correct_prob_death(self, example_properties):
        """
        Asserts that the probability of dying is calculated correctly.
        """
        a = Animal(example_properties)
        a.find_fitness()
        assert a.prob_death() == approx(0.0014929212599999687)

    def test_false_death_prob_is_one(self):
        """
        Assert that False is returned if probability of dying is one.
        """
        test_properties = {
            "species": "animal",
            "age": 5,
            "weight": 0
        }
        a = Animal(test_properties)
        a.find_fitness()
        assert a.will_animal_live() is not True

    def test_false_death_prob_is_zero(self, example_properties_w_40):
        """
        Assert that True is returned if probability of dying is zero.
        """
        numpy.random.seed(1)
        a = Animal(example_properties_w_40)
        assert a.will_animal_live() is True

    def test_num_less_than_death_prob(self, example_properties, mocker):
        """
        Asserts that True is not returned if the random number is less than
        the death probability.
        """
        mocker.patch('numpy.random.random', return_value=0.0005)
        a = Animal(example_properties)
        a.find_fitness()
        assert a.will_animal_live() is not True

    def test_num_more_than_death_prob(self, example_properties, mocker):
        """
        Asserts that True is returned if the random number is larger than
        the death probability.
        """
        mocker.patch('numpy.random.random', return_value=0.5)
        a = Animal(example_properties)
        a.find_fitness()
        assert a.will_animal_live() is True


class TestHerbivore:
    """
    Tests for Herbivore class.
    """
    @pytest.fixture
    def example_properties(self):
        return {
            "species": "Herbivore",
            "age": 5,
            "weight": 20
        }

    @pytest.fixture
    def example_population(self):
        return [
            {"species": "Herbivore", "age": 1, "weight": 10.0},
            {"species": "Herbivore", "age": 1, "weight": 10.0},
            {"species": "Herbivore", "age": 1, "weight": 10.0}
        ]

    def test_constructor(self, example_properties):
        """
        Checks that class is initialized with given weight and age.
        """
        h = Herbivore(example_properties)
        assert h.age == example_properties["age"]
        assert h.weight == example_properties["weight"]

    def test_correct_rel_abund_fodder_herb(self, example_population,
                                           example_properties):
        """
        Checks that method for calculating relative abundance of fodder
        returns the correct value.
        """
        jungle = Jungle(example_population)
        jungle.regrowth()
        herbivore = Herbivore(example_properties)
        rel_abund_fodder = herbivore.find_rel_abund_of_fodder(jungle)
        assert rel_abund_fodder == 20.0
        # 20 is rel abundance of fodder for this herbivore calculated by hand

    def test_propensity_dict_correct_types(self, example_properties,
                                           example_population):
        """
        Asserts that the propensity_of_each_neighbouring_cell method
        returns a dictionary with tuples as keys and floats as values.
        """
        herbivore = Herbivore(example_properties)
        dict_of_neighbours = {(1, 2): Jungle(example_population),
                              (2, 1): Jungle(example_population),
                              (2, 3): Jungle(example_population),
                              (3, 2): Jungle(example_population)
                              }
        for jungle in dict_of_neighbours.values():
            jungle.regrowth()
        prop_dict = herbivore.propensity_move_to_each_neighbour(
            dict_of_neighbours)
        assert type(prop_dict) is dict
        for loc, prop in prop_dict.items():
            assert type(loc) is tuple
            assert type(prop) is numpy.float64

    def test_dict_with_correct_key_and_value_types(self, example_population,
                                                   example_properties):
        """
        Asserts that the prob_move_to_each_neighbour method returns a
        dictionary with tuples as keys and floats as values.
        """
        herbivore = Herbivore(example_properties)
        dict_of_neighbours = {(1, 2): Jungle(example_population),
                              (2, 1): Jungle(example_population),
                              (2, 3): Jungle(example_population),
                              (3, 2): Jungle(example_population)
                              }
        for jungle in dict_of_neighbours.values():
            jungle.regrowth()
        prob_dict = herbivore.prob_move_to_each_neighbour(dict_of_neighbours)
        assert type(prob_dict) is dict
        for loc, prob in prob_dict.items():
            assert type(loc) is tuple
            assert type(prob) is numpy.float64

    def test_dict_converted_correctly_to_list_array(self, example_properties,
                                                    example_population):
        """
        Asserts that the output from convert_dict_to_list_and_array
        method are of the correct types.
        """
        herbivore = Herbivore(example_properties)
        dict_of_neighbours = {(1, 2): Jungle(example_population),
                              (2, 1): Jungle(example_population),
                              (2, 3): Jungle(example_population),
                              (3, 2): Jungle(example_population)
                              }
        for jungle in dict_of_neighbours.values():
            jungle.regrowth()
        prob_dict = herbivore.prob_move_to_each_neighbour(dict_of_neighbours)
        locs, probs = herbivore.convert_dict_to_list_and_array(prob_dict)
        assert type(locs) is list
        assert type(probs) is numpy.ndarray

    def test_tuple_returned(self, example_population, example_properties):
        """
        Asserts that the where_will_animal_move method returns a tuple
        """
        dict_of_neighbours = {(1, 2): Jungle(example_population),
                              (2, 1): Jungle(example_population),
                              (2, 3): Jungle(example_population),
                              (3, 2): Jungle(example_population)
                              }
        for jungle in dict_of_neighbours.values():
            jungle.regrowth()
        herbivore = Herbivore(example_properties)
        assert type(herbivore.find_new_coordinates(
            dict_of_neighbours)) is tuple

    def test_find_correct_coordinates(self):
        """
        Implements seeding to assert that animal returned correct location to
        move to.
        """
        numpy.random.seed(1)
        test_population_coords = [
            {"species": "Herbivore", "age": 1, "weight": 10.0}
        ]
        test_properties_coords = {
            "species": "Herbivore",
            "age": 1,
            "weight": 10
        }
        dict_of_neighbours = {(1, 2): Jungle(test_population_coords),
                              (2, 1): Jungle(test_population_coords),
                              (2, 3): Jungle(test_population_coords),
                              (3, 2): Jungle(test_population_coords)
                              }
        for jungle in dict_of_neighbours.values():
            jungle.regrowth()
        herbivore = Herbivore(test_properties_coords)
        assert herbivore.find_new_coordinates(dict_of_neighbours) == (2, 1)

    def test_coordinates_returned_when_true(self, mocker, example_properties):
        """
        Asserts that a tuple of coordinates is returned if the animal will
        move.
        """
        test_population_true = [
            {"species": "Herbivore", "age": 1, "weight": 10.0}
        ]
        dict_of_neighbours = {(1, 2): Jungle(test_population_true),
                              (2, 1): Jungle(test_population_true),
                              (2, 3): Jungle(test_population_true),
                              (3, 2): Jungle(test_population_true)
                              }
        for jungle in dict_of_neighbours.values():
            jungle.regrowth()
        herbivore = Herbivore(example_properties)
        herbivore.fitness = 1
        mocker.patch('numpy.random.random', return_value=0.1)
        new_coordinates = herbivore.return_new_coordinates(dict_of_neighbours)
        assert type(new_coordinates) == tuple


class TestCarnivore:
    """
    Tests for Carnivore class
    """
    @pytest.fixture
    def example_properties(self):
        return {
            "species": "animal",
            "age": 5,
            "weight": 20
        }

    @pytest.fixture
    def example_population_carn(self):
        return [
            {"species": "Herbivore", "age": 1, "weight": 10.0},
            {"species": "Herbivore", "age": 1, "weight": 10.0},
            {"species": "Herbivore", "age": 1, "weight": 10.0},
            {"species": "Carnivore", "age": 1, "weight": 10.0},
            {"species": "Carnivore", "age": 1, "weight": 10.0},
            {"species": "Carnivore", "age": 1, "weight": 10.0},
        ]

    @pytest.fixture
    def setup_class(cls):
        """
        This class is for use in test_kill_when_prob_is_one, where we need to
        change the DeltaPhiMax parameter. After test is run, we tear it down
        and set the parameter back to it's initial value.

        """
        default_params = Carnivore.params.copy()
        yield None
        Carnivore.params = default_params

    def test_constructor(self, example_properties):
        """
        Checks that class is initialized with given weight and age.
        """
        carnivore = Carnivore(example_properties)
        assert carnivore.age == example_properties["age"]
        assert carnivore.weight == example_properties["weight"]

    def test_correct_prob(self, example_properties):
        """
        Asserts that prob_kill returns correct probability.
        """
        herb_fitness = 0.5
        carnivore = Carnivore(example_properties)
        carnivore.params["DeltaPhiMax"] = 10.0
        carnivore.find_fitness()
        prob = carnivore.prob_kill(herb_fitness)
        assert prob == approx(0.04983411986)

    def test_kill_when_prob_is_one(self, setup_class, example_properties):
        """
        Asserts that kill method returns True when prob_kill is one.
        """
        herbivore = Herbivore(example_properties)
        carnivore = Carnivore(example_properties)
        herbivore.find_fitness()
        carnivore.find_fitness()
        carnivore.params["DeltaPhiMax"] = 0.1
        assert carnivore.kill(herbivore) is True

    def test_not_kill_when_prob_is_zero(self, example_properties):
        """
        Asserts that kill method returns False when prob_kill is zero.
        """
        herbivore = Herbivore(example_properties)
        carnivore = Carnivore(example_properties)
        herbivore.find_fitness()
        carnivore.fitness = 0.5
        assert carnivore.kill(herbivore) is False

    def test_carn_doesnt_eat_when_no_herbs(self, example_properties):
        """
        Asserts that carnivore hasn't gained weight when there are no
        herbivores to be eaten.
        """
        carnivore = Carnivore(example_properties)
        old_weight = carnivore.weight
        pop_herb = []
        carnivore.eat(pop_herb)
        new_weight = carnivore.weight
        assert new_weight == old_weight

    def test_carn_gained_weight_after_eating(self, example_properties):
        """
        Assert that carnivore has gained weight after eating.
        """
        carnivore = Carnivore(example_properties)
        carnivore.find_fitness()
        old_weight = carnivore.weight
        carnivore.params["DeltaPhiMax"] = 0.1
        herb = Herbivore(example_properties)
        herb.find_fitness()
        carnivore.eat([herb])
        assert old_weight < carnivore.weight

    def test_list_of_herbs_returned(self, example_properties):
        """
        Asserts that eat method returns a list of herbivore class instances.
        """
        carnivore = Carnivore(example_properties)
        carnivore.find_fitness()
        carnivore.params["DeltaPhiMax"] = 0.1
        herb = Herbivore(example_properties)
        herb.find_fitness()
        eaten_herbs = carnivore.eat([herb])
        assert type(eaten_herbs) is list

    def test_correct_rel_abund_fodder_carn(self, example_population_carn,
                                           example_properties):
        """
        Checks that method for calculating relative abundance of fodder
        returns the correct value.
        """
        jungle = Jungle(example_population_carn)
        carnivore = Carnivore(example_properties)
        rel_abund_fodder = carnivore.find_rel_abund_of_fodder(jungle)
        assert rel_abund_fodder == 0.15
        # 0.15 is rel abundance of fodder for this carnivore calculated by hand
