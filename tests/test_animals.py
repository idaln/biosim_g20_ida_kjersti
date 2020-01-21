# -*- coding: utf-8 -*-

"""
Test set for Animal class interface.

This set of tests checks the interface and functionality of the Animal class
provided by the animal module of the biosim package.
"""

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idaln@hotmail.com & kjkv@nmbu.no"

import pytest
from biosim.animals import Animal, Herbivore, Carnivore
from biosim.landscape import Jungle
from pytest import approx
import numpy


class TestAnimal:
    """
    Tests for Animal class.
    """
    @pytest.fixture
    def example_properties_w_20(self):
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

    def test_constructor_animal(self, example_properties_w_20):
        """
        Checks that animal class can been initialized and that some parameters
        have been unpacked correctly.
        """
        animal = Animal(example_properties_w_20)
        assert animal.age == 5
        assert animal.params['a_half'] == 60
        assert animal.params['omega'] == 0.9

    def test_error_raised_from_invalid_age(self):
        """
        Tests that ValueError is raised if animal with negative age is
        initialized.
        """
        properties_age = {
            "species": "animal",
            "age": -5,
            "weight": 40
        }
        with pytest.raises(ValueError):
            Animal(properties_age)

    def test_error_raised_from_negative_weight(self):
        """
        Tests that ValueError is raised if animal with negative weight is
        initialized.
        """
        properties_weight = {
            "species": "animal",
            "age": 5,
            "weight": -40
        }
        with pytest.raises(ValueError):
            Animal(properties_weight)

    def test_error_raised_from_weight_zero(self):
        """
        Tests that ValueError is raised if animal with weight zero is
        initialized.
        """
        properties_weight_zero = {
            "species": "animal",
            "age": 5,
            "weight": 0
        }
        with pytest.raises(ValueError):
            Animal(properties_weight_zero)

    def test_is_animal_one_year_older(self, example_properties_w_20):
        """
        Checks that animal is one year older than last year after running
        make_animal_one_year_older method.
        """
        animal = Animal(example_properties_w_20)
        initial_age = animal.age
        animal.make_animal_one_year_older()
        assert animal.age - initial_age == 1

    def test_has_animal_lost_weight(self, example_properties_w_20):
        """
        Checks that weight after weight loss is less than initial weight after
        running weight_loss method
        """
        animal = Animal(example_properties_w_20)
        initial_weight = animal.weight
        animal.weight_loss()
        assert animal.weight < initial_weight

    def test_has_animal_gained_weight_from_eating(
            self, example_properties_w_20
    ):
        """
        Checks that herbivore has gained weight after running
        add_eaten_fodder_to_weight method.
        """
        animal = Animal(example_properties_w_20)
        test_fodder = 8
        initial_weight = animal.weight
        animal.add_eaten_fodder_to_weight(test_fodder)
        assert animal.weight > initial_weight

    def test_fitness_between_zero_and_one(self, example_properties_w_20):
        """
        Checks that find_fitness method calculates a fitness between 0 and 1.
        """
        animal = Animal(example_properties_w_20)
        animal.find_fitness()
        assert 0 <= animal.fitness <= 1

    def test_fitness_zero_if_weight_zero(self, example_properties_w_20):
        """
        Checks that find_fitness method calculates a fitness of zero if
        weight of the animal is zero.
        """
        animal = Animal(example_properties_w_20)
        animal.weight = 0
        animal.find_fitness()
        assert animal.fitness == 0

    def test_correct_fitness_calculated(self, example_properties_w_20):
        """
        Checks that find_fitness method calculates correct value.
        """
        animal = Animal(example_properties_w_20)
        animal.find_fitness()
        assert animal.fitness == approx(0.9983411986)

    def test_correct_prob_of_moving(self, example_properties_w_20):
        """
        Asserts that prob_of_animal_moving calculates the correct probability
        of moving.
        """
        animal = Animal(example_properties_w_20)
        animal.find_fitness()
        assert animal.prob_of_animal_moving() == approx(0.3993364794)

    def test_correct_bool_of_moving(self, example_properties_w_20, mocker):
        """
        Asserts that will_animal_move method returns True for a certain
        probability and a specific random number.
        """
        mocker.patch('numpy.random.random', return_value=0.1)
        animal = Animal(example_properties_w_20)
        animal.fitness = 1
        assert animal.will_animal_move() is True

    def test_prob_of_birth_with_one_animal_in_cell(self,
                                                   example_properties_w_20
                                                   ):
        """
        Asserts that if there is only one animal in the cell, then the
        prob_give_birth method returns a probability of zero.
        """
        animal = Animal(example_properties_w_20)
        animal.find_fitness()
        assert animal.prob_give_birth(num_animals=1) == 0

    def test_prob_of_birth_if_weight_less_than_limit(self,
                                                     example_properties_w_20
                                                     ):
        """
        Asserts that prob_give_birth returns a probability of zero if the
        mothers weight is less than the given limit.
        """
        animal = Animal(example_properties_w_20)
        animal.find_fitness()
        assert animal.prob_give_birth(num_animals=6) == 0

    def test_correct_prob_of_birth(self, example_properties_w_40):
        """
        Asserts that prob_give_birth calculates the correct probability of
        giving birth.
        """
        animal = Animal(example_properties_w_40)
        animal.find_fitness()
        assert animal.prob_give_birth(num_animals=6) == 1

    def test_true_if_birth_prob_one(self, example_properties_w_40):
        """
        Tests the will_birth_take_place method by checking if True is returned
        when the probability of giving birth is 1.
        """
        animal = Animal(example_properties_w_40)
        animal.find_fitness()
        assert animal.will_birth_take_place(num_animals=6) is True

    def test_false_if_rand_num_more_than_birth_prob(self, mocker):
        """
        Tests will_birth_take_place method by checking if False is returned
        when a random number larger than a specific probability is drawn.
        """
        test_properties_prob = {
            "species": "animal",
            "age": 63,
            "weight": 30
        }
        mocker.patch('numpy.random.random', return_value=0.95)
        animal = Animal(test_properties_prob)
        animal.find_fitness()
        assert animal.will_birth_take_place(num_animals=6) is not True

    def test_true_if_rand_num_less_than_birth_prob(self, mocker):
        """
        Tests will_birth_take_place method. Checks if True is returned when
        random number less than a specific probability is drawn.
        """
        test_properties_num_less = {
            "species": "animal",
            "age": 63,
            "weight": 30
        }
        mocker.patch('numpy.random.random', return_value=0.8)
        animal = Animal(test_properties_num_less)
        animal.find_fitness()
        assert animal.will_birth_take_place(num_animals=6) is True

    def test_baby_weight_returned_when_mothers_weight_large_enough(
            self, example_properties_w_40, mocker
    ):
        """
        After running birth_process, we check that a birth took place by
        testing if baby's weight is a float of given value and that the baby's
        weight times xi was smaller than the mother's weight.
        """
        mocker.patch('numpy.random.normal', return_value=5.5)
        animal = Animal(example_properties_w_40)
        animal.find_fitness()
        baby_weight = animal.birth_process(num_animals=6)
        assert type(baby_weight) is float
        assert baby_weight == 5.5
        assert animal.weight > baby_weight * animal.params['xi']

    def test_no_birth_when_mothers_weight_small(
            self, example_properties_w_40, mocker
    ):
        """
        Asserts that no baby is born from running birth_process
        when mother's weight is less than xi times baby's weight.
        """
        mocker.patch('numpy.random.normal', return_value=50)
        animal = Animal(example_properties_w_40)
        animal.find_fitness()
        baby_weight = animal.birth_process(num_animals=6)
        assert baby_weight is None

    def test_mother_loses_weight_after_birth(
            self, example_properties_w_40, mocker
    ):
        """
        Test birth_process method.
        Asserts that mother loses weight equal to xi * baby's weight after
        giving birth.
        """
        mocker.patch('numpy.random.normal', return_value=5.5)
        animal = Animal(example_properties_w_40)
        animal.find_fitness()
        initial_weight = animal.weight
        birth_weight = animal.birth_process(num_animals=6)
        assert animal.weight == initial_weight - \
            (animal.params['xi'] * birth_weight)

    def test_no_birth_if_baby_weight_is_zero(
            self, example_properties_w_40, mocker
    ):
        """
        Tests birth_process method.
        Asserts that no baby is born if the baby's birth weight is
        equal to zero.
        """
        mocker.patch('numpy.random.normal', return_value=0)
        animal = Animal(example_properties_w_40)
        animal.find_fitness()
        assert animal.birth_process(num_animals=6) is None

    def test_prob_death_is_one_if_fitness_zero(self, example_properties_w_20):
        """
        Asserts that the probability calculated from prob_death is one
        if fitness equals zero.
        """
        animal = Animal(example_properties_w_20)
        animal.weight = 0
        animal.find_fitness()
        assert animal.prob_death() == 1

    def test_correct_prob_death(self, example_properties_w_20):
        """
        Asserts that prob_death calculates the correct probability of dying.
        """
        animal = Animal(example_properties_w_20)
        animal.find_fitness()
        assert animal.prob_death() == approx(0.0014929212599999687)

    def test_not_true_if_death_prob_is_one(self, example_properties_w_20):
        """
        Assert that will_animal_live does not return True if probability of
        dying is one.
        """
        animal = Animal(example_properties_w_20)
        animal.weight = 0
        animal.find_fitness()
        assert animal.will_animal_live() is not True

    def test_true_if_death_prob_is_zero(self, example_properties_w_40):
        """
        Assert that will_animal_live returns True if probability of dying
        is zero because of high fitness.
        """
        numpy.random.seed(1)
        animal = Animal(example_properties_w_40)
        assert animal.will_animal_live() is True

    def test_not_true_if_rand_num_less_than_death_prob(
            self, example_properties_w_20, mocker
    ):
        """
        Asserts that will_animal_live does not return True
        if the random number is less than the death probability.
        """
        mocker.patch('numpy.random.random', return_value=0.0005)
        animal = Animal(example_properties_w_20)
        animal.find_fitness()
        assert animal.will_animal_live() is not True

    def test_true_if_rand_num_more_than_death_prob(
            self, example_properties_w_20, mocker
    ):
        """
        Asserts that will_animal_live returns True if the random number is
        larger than the death probability.
        """
        mocker.patch('numpy.random.random', return_value=0.5)
        animal = Animal(example_properties_w_20)
        animal.find_fitness()
        assert animal.will_animal_live() is True


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

    def test_constructor_herbivore(self, example_properties):
        """
        Checks that Herbivore class is initialized with correct weight and age.
        """
        herbivore = Herbivore(example_properties)
        assert herbivore.age == example_properties["age"]
        assert herbivore.weight == example_properties["weight"]

    def test_correct_rel_abund_fodder_herb(
            self, example_population, example_properties
    ):
        """
        Checks that find_rel_abund_of_fodder returns correct amount of fodder
        for herb in Jungle cell.
        """
        jungle = Jungle(example_population)
        jungle.regrowth()
        herbivore = Herbivore(example_properties)
        rel_abund_fodder = herbivore.find_rel_abund_of_fodder(jungle)
        assert rel_abund_fodder == 20.0
        # 20 is rel abundance of fodder for this herbivore, calculated by hand

    def test_correct_types_in_propensity_dict(
            self, example_properties, example_population
    ):
        """
        Asserts that propensity_move_to_each_neighbour method
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
            assert type(prop) is float

    def test_correct_types_in_prob_move_dict(
            self, example_population, example_properties
    ):
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
            assert type(prob) is float

    def test_dict_converted_correctly_to_list_and_array(
            self, example_properties, example_population
    ):
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

    def test_animal_will_move_to_tuple_coordinates(
            self, example_population, example_properties
    ):
        """
        Asserts that the where_will_animal_move method returns a tuple.
        """
        neighbours_for_tuple = {(1, 2): Jungle(example_population),
                                (2, 1): Jungle(example_population),
                                (2, 3): Jungle(example_population),
                                (3, 2): Jungle(example_population)
                                }
        for jungle in neighbours_for_tuple.values():
            jungle.regrowth()
        herbivore = Herbivore(example_properties)
        assert type(herbivore.find_new_coordinates(
            neighbours_for_tuple)) is tuple

    def test_find_correct_coordinates(self):
        """
        Implements seeding to assert that find_new_coordinates returns
        correct location for the animal to move to.
        """
        numpy.random.seed(1)
        test_population_for_coords = [
            {"species": "Herbivore", "age": 1, "weight": 10.0}
        ]
        test_properties_for_coords = {
            "species": "Herbivore",
            "age": 1,
            "weight": 10
        }
        neighbours_for_coords = {(1, 2): Jungle(test_population_for_coords),
                                 (2, 1): Jungle(test_population_for_coords),
                                 (2, 3): Jungle(test_population_for_coords),
                                 (3, 2): Jungle(test_population_for_coords)
                                 }
        for jungle in neighbours_for_coords.values():
            jungle.regrowth()
        herbivore = Herbivore(test_properties_for_coords)
        assert herbivore.find_new_coordinates(neighbours_for_coords) == (2, 1)

    def test_coordinates_returned_when_animal_will_move_true(
            self, mocker, example_properties
    ):
        """
        Asserts that a tuple of coordinates is returned from
        return_new_coordinates if the animal will move because the random
        number is less than the probability of moving.
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
    def teardown_carnivore_tests(self):
        """
        This class is for use in several tests, where we need to change the
        DeltaPhiMax parameter. After a test is run, we reset all parameters
        to default values.
        """
        yield None
        Carnivore.reset_params()

    def test_constructor_carnivore(self, example_properties):
        """
        Checks that class is initialized with correct weight and age.
        """
        carnivore = Carnivore(example_properties)
        assert carnivore.age == example_properties["age"]
        assert carnivore.weight == example_properties["weight"]

    def test_correct_prob_of_killing(self, example_properties,
                                     teardown_carnivore_tests):
        """
        Asserts that prob_kill returns correct probability.
        """
        herb_fitness = 0.5
        carnivore = Carnivore(example_properties)
        carnivore.params["DeltaPhiMax"] = 10.0
        carnivore.find_fitness()
        prob = carnivore.prob_kill(herb_fitness)
        assert prob == approx(0.04983411986)

    def test_true_when_prob__of_killing_is_one(
            self, teardown_carnivore_tests, example_properties
    ):
        """
        Asserts that kill method returns True when prob_kill is one.
        """
        herbivore = Herbivore(example_properties)
        carnivore = Carnivore(example_properties)
        herbivore.find_fitness()
        carnivore.find_fitness()
        carnivore.params["DeltaPhiMax"] = 0.1
        assert carnivore.kill(herbivore) is True

    def test_false_when_prob_of_killing_is_zero(self, example_properties):
        """
        Asserts that kill method returns False when prob_kill is zero.
        """
        herbivore = Herbivore(example_properties)
        carnivore = Carnivore(example_properties)
        herbivore.find_fitness()
        carnivore.fitness = 0.5
        assert carnivore.kill(herbivore) is False

    def test_carn_doesnt_eat_when_no_herbs_available(self, example_properties):
        """
        Asserts that carnivore hasn't gained weight after eat method when there
        are no herbivores to be eaten.
        """
        carnivore = Carnivore(example_properties)
        old_weight = carnivore.weight
        pop_herb = []
        carnivore.attempt_eating_all_herbivores_in_cell(pop_herb)
        assert carnivore.weight == old_weight

    def test_carn_gained_weight_after_eating(
            self, example_properties, teardown_carnivore_tests
    ):
        """
        Assert that carnivore has gained weight after eat method
        when there is a weaker herbivore available.
        """
        carnivore = Carnivore(example_properties)
        carnivore.find_fitness()
        old_weight = carnivore.weight
        carnivore.params["DeltaPhiMax"] = 0.1
        herb = Herbivore(example_properties)
        herb.find_fitness()
        carnivore.attempt_eating_all_herbivores_in_cell([herb])
        assert old_weight < carnivore.weight

    def test_list_of_herbs_returned(self, example_properties,
                                    teardown_carnivore_tests):
        """
        Asserts that eat method returns a list of herbivore class instances
        when the carnivore has eaten a herbivore.
        """
        carnivore = Carnivore(example_properties)
        carnivore.find_fitness()
        carnivore.params["DeltaPhiMax"] = 0.1
        herb = Herbivore(example_properties)
        herb.find_fitness()
        eaten_herbs = carnivore.attempt_eating_all_herbivores_in_cell([herb])
        assert type(eaten_herbs) is list

    def test_correct_rel_abund_fodder_carn(self, example_population_carn,
                                           example_properties):
        """
        Checks that find_rel_abund_of_fodder returns correct value for
        carnivores.
        """
        jungle = Jungle(example_population_carn)
        carnivore = Carnivore(example_properties)
        rel_abund_fodder = carnivore.find_rel_abund_of_fodder(jungle)
        assert rel_abund_fodder == 0.15
        # 0.15 is rel abundance of fodder for this carnivore calculated by hand
