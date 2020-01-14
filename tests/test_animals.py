# -*- coding: utf-8 -*-


__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idaln@hotmail.com & kjkv@nmbu.no"

from biosim.animals import Animal, Herbivore
from biosim.landscape import Jungle
from pytest import approx
import numpy

test_population = [
    {"species": "Herbivore", "age": 1, "weight": 10.0},
    {"species": "Herbivore", "age": 1, "weight": 10.0},
    {"species": "Herbivore", "age": 1, "weight": 10.0}
]
test_params = {
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
test_properties = {
    "species": "animal",
    "age": 5,
    "weight": 20
}
num_animals = 6


class TestAnimal:
    """
    Tests for Animal class.
    """

    def test_constructor(self):
        """
        Checks that class has been initialized and some parameters have
        been unpacked correctly.
        """
        # Animal.params = test_params
        # Det her går ann, men da må alle tester endres
        a = Animal(test_properties)
        assert a.age == 5
        assert a.params['a_half'] == 60
        assert a.params['omega'] == 0.9

    def test_is_animal_one_year_older(self):
        """
        Checks that animal is one year older than last year.
        """
        a = Animal(test_properties)
        initial_age = a.age
        a.make_animal_one_year_older()
        assert a.age - initial_age == 1

    def test_has_animal_lost_weight(self):
        """
        Checks that weight after weight loss is less than initial weight
        """
        a = Animal(test_properties)
        initial_weight = a.weight
        a.weight_loss()
        assert a.weight < initial_weight

    def test_has_animal_gained_weight(self):
        """
        Checks that animal has gained weight after eating.
        """
        a = Animal(test_properties)
        test_fodder = 8
        initial_weight = a.weight
        a.add_eaten_fodder_to_weight(test_fodder)
        assert a.weight > initial_weight

    def test_fitness_between_zero_and_one(self):
        """
        Checks that fitness is between 0 and 1.
        """
        a = Animal(test_properties)
        a.find_fitness()
        assert 0 <= a.fitness <= 1

    def test_fitness_zero_if_weight_zero(self):
        """
        Checks that fitness is zero if weight is zero.
        """
        test_properties = {
            "species": "animal",
            "age": 5,
            "weight": 0
        }
        a = Animal(test_properties)
        a.find_fitness()
        assert a.fitness == 0

    def test_correct_fitness(self):
        """
        Checks that fitness formula yields correct value.
        """
        a = Animal(test_properties)
        a.find_fitness()
        assert a.fitness == approx(0.9983411986)

    def test_correct_prob_of_moving(self):
        """
        Asserts that method calculates the probability of moving correctly.
        """
        animal = Animal(test_properties)
        animal.find_fitness()
        assert animal.prob_of_animal_moving() == approx(0.3993364794)

    def test_correct_bool_of_moving(self, mocker):
        """
        Asserts that method returns True when a certain random number
        is drawn.
        """
        mocker.patch('numpy.random.random', return_value=0.1)
        animal = Animal(test_properties)
        animal.fitness = 1
        assert animal.will_animal_move() is True

    def test_correct_rel_abund_fodder(self):
        """
        Checks that method for calculating relative abundance of fodder
        returns the correct value.
        """
        jungle = Jungle(test_population)
        jungle.regrowth()
        animal = Animal(test_properties)
        rel_abund_fodder = animal.find_rel_abund_of_fodder(jungle)
        assert rel_abund_fodder == 4.0

    def test_propensity_dict_correct_types(self):
        """
        Asserts that the propensity_of_each_neighbouring_cell method
        returns a dictionary with tuples as keys and floats as values.
        """
        animal = Animal(test_properties)
        dict_of_neighbours = {(1, 2): Jungle(test_population),
                              (2, 1): Jungle(test_population),
                              (2, 3): Jungle(test_population),
                              (3, 2): Jungle(test_population)
                              }
        for jungle in dict_of_neighbours.values():
            jungle.regrowth()
        prop_dict = animal.propensity_move_to_each_neighbour(
            dict_of_neighbours)
        assert type(prop_dict) is dict
        for loc, prop in prop_dict.items():
            assert type(loc) is tuple
            assert type(prop) is numpy.float64

    def test_dict_with_correct_key_and_value_types(self):
        """
        Asserts that the prob_move_to_each_neighbour method returns a
        dictionary with tuples as keys and floats as values.
        """
        animal = Animal(test_properties)
        dict_of_neighbours = {(1, 2): Jungle(test_population),
                              (2, 1): Jungle(test_population),
                              (2, 3): Jungle(test_population),
                              (3, 2): Jungle(test_population)
                              }
        for jungle in dict_of_neighbours.values():
            jungle.regrowth()
        prob_dict = animal.prob_move_to_each_neighbour(dict_of_neighbours)
        assert type(prob_dict) is dict
        for loc, prob in prob_dict.items():
            assert type(loc) is tuple
            assert type(prob) is numpy.float64
            
    def test_dict_converted_correctly_to_list_array(self):
        """
        Asserts that the output from convert_dict_to_list_and_array
        method are of the correct types.
        """
        animal = Animal(test_properties)
        dict_of_neighbours = {(1, 2): Jungle(test_population),
                              (2, 1): Jungle(test_population),
                              (2, 3): Jungle(test_population),
                              (3, 2): Jungle(test_population)
                              }
        for jungle in dict_of_neighbours.values():
            jungle.regrowth()
        prob_dict = animal.prob_move_to_each_neighbour(dict_of_neighbours)
        locs, probs = animal.convert_dict_to_list_and_array(prob_dict)
        assert type(locs) is list
        assert type(probs) is numpy.ndarray

    def test_tuple_returned(self):
        """
        Asserts that the where_will_animal_move method returns a tuple
        """
        dict_of_neighbours = {(1, 2): Jungle(test_population),
                              (2, 1): Jungle(test_population),
                              (2, 3): Jungle(test_population),
                              (3, 2): Jungle(test_population)
                              }
        for jungle in dict_of_neighbours.values():
            jungle.regrowth()
        animal = Animal(test_properties)
        assert type(animal.find_new_coordinates(dict_of_neighbours)) is tuple

    def test_find_correct_coordinates(self):
        """
        Implements seeding to assert that animal returned correct location to
        move to.
        """
        numpy.random.seed(1)
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
        assert animal.find_new_coordinates(dict_of_neighbours) == (2, 1)

    def test_coordinates_returned_when_true(self, mocker):
        """
        Asserts that a tuple of coordinates is returned if the animal will
        move.
        """
        test_population = [
            {"species": "Herbivore", "age": 1, "weight": 10.0}
        ]
        dict_of_neighbours = {(1, 2): Jungle(test_population),
                              (2, 1): Jungle(test_population),
                              (2, 3): Jungle(test_population),
                              (3, 2): Jungle(test_population)
                              }
        for jungle in dict_of_neighbours.values():
            jungle.regrowth()
        animal = Animal(test_properties)
        animal.fitness = 1
        mocker.patch('numpy.random.random', return_value=0.1)
        new_coordinates = animal.return_new_coordinates(dict_of_neighbours)
        assert type(new_coordinates) == tuple

    def test_prob_give_birth_one_animal_in_square(self):
        """
        Asserts that if there is only one animal in the square, then the
        probability of giving birth is zero.
        """
        a = Animal(test_properties)
        a.find_fitness()
        assert a.prob_give_birth(num_animals=1) == 0

    def test_prob_give_birth_weight_less_than_limit(self):
        """
        Asserts that probability of giving birth is zero if the mothers
        weight is less than a given limit.
        """
        a = Animal(test_properties)
        a.find_fitness()
        assert a.prob_give_birth(num_animals=6) == 0

    def test_correct_birth_prob(self):
        """
        Asserts that the calculated probability is correct.
        """
        test_properties = {
            "species": "animal",
            "age": 5,
            "weight": 40
        }
        a = Animal(test_properties)
        a.find_fitness()
        assert a.prob_give_birth(num_animals=6) == 1

    def test_birth_prob_is_one(self):
        """
        Tests will_birth_take_place method.
        Checks if True is returned if probability of giving birth is 1.
        """
        test_properties = {
            "species": "animal",
            "age": 5,
            "weight": 40
        }
        a = Animal(test_properties)
        a.find_fitness()
        assert a.will_birth_take_place(num_animals=6) is True

    def test_num_more_than_birth_prob(self, mocker):
        """
        Tests will_birth_take_place method.
        Checks if False is returned if random number larger than the
        probability is drawn.
        """
        test_properties = {
            "species": "animal",
            "age": 63,
            "weight": 30
        }
        mocker.patch('numpy.random.random', return_value=0.95)
        a = Animal(test_properties)
        a.find_fitness()
        assert a.will_birth_take_place(num_animals=6) is not True

    def test_num_less_than_birth_prob(self, mocker):
        """
        Tests will_birth_take_place method.
        Checks if True is returned if random number less than the
        probability is drawn.
        """
        test_properties = {
            "species": "animal",
            "age": 63,
            "weight": 30
        }
        mocker.patch('numpy.random.random', return_value=0.8)
        a = Animal(test_properties)
        a.find_fitness()
        assert a.will_birth_take_place(num_animals=6) is True

    def test_mothers_weight_large_enough(self, mocker):
        """
        Tests birth_process method.
        After birth, we check that no birth took place if the predicted baby
        weight times xi is larger than the mother's weight.
        """
        test_properties = {
            "species": "animal",
            "age": 5,
            "weight": 40
        }
        mocker.patch('numpy.random.normal', return_value=5.5)
        a = Animal(test_properties)
        a.find_fitness()
        assert a.weight > a.birth_process(num_animals=6) * a.params['xi']

    def test_mother_loses_weight(self, mocker):
        """
        Test birth_process method.
        Asserts that mother loses weight equal to xi * birth weight
        """
        test_properties = {
            "species": "animal",
            "age": 5,
            "weight": 40
        }
        mocker.patch('numpy.random.normal', return_value=5.5)
        a = Animal(test_properties)
        a.find_fitness()
        initial_weight = a.weight
        birth_weight = a.birth_process(num_animals=6)
        assert a.weight == initial_weight - (a.params['xi'] * birth_weight)

    def test_birth_weight_different_from_zero(self, mocker):
        """
        Tests birth_process method.
        Asserts that no baby is born if the baby weight is equal to zero.
        """
        test_properties = {
            "species": "animal",
            "age": 5,
            "weight": 40
        }
        mocker.patch('numpy.random.normal', return_value=0)
        a = Animal(test_properties)
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

    def test_correct_prob_death(self):
        """
        Asserts that the probability of dying is calculated correctly.
        """
        a = Animal(test_properties)
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

    def test_false_death_prob_is_zero(self):
        """
        Assert that True is returned if probability of dying is zero.
        """
        numpy.random.seed(1)
        test_properties = {
            "species": "animal",
            "age": 5,
            "weight": 40
        }
        a = Animal(test_properties)
        assert a.will_animal_live() is True

    def test_num_less_than_death_prob(self, mocker):
        """
        Asserts that True is not returned if the random number is less than
        the death probability.
        """
        mocker.patch('numpy.random.random', return_value=0.0005)
        a = Animal(test_properties)
        a.find_fitness()
        assert a.will_animal_live() is not True

    def test_num_more_than_death_prob(self, mocker):
        """
        Asserts that True is returned if the random number is larger than
        the death probability.
        """
        mocker.patch('numpy.random.random', return_value=0.5)
        a = Animal(test_properties)
        a.find_fitness()
        assert a.will_animal_live() is True


class TestHerbivore:
    """
    Tests for Herbivore class.
    """
    def test_constructor(self):
        """
        Checks that class is initialized with given weight and age.
        """
        h = Herbivore(test_properties)
        assert h.age == test_properties["age"]
        assert h.weight == test_properties["weight"]
