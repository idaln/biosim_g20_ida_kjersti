# -*- coding: utf-8 -*-


__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idaln@hotmail.com & kjkv@nmbu.no"

from biosim.animals import Animal
from pytest import approx

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
    """Tests for Animal class"""
    def test_constructor(self):
        """
        Checks that class has been initialized and some parameters have
        been unpacked correctly.
        """
        a = Animal(test_params, test_properties, num_animals)
        assert a.age == 5
        assert a.a_half == 60
        assert a.omega == 0.9

    def test_ageing(self):
        """
        Checks that animal is one year older than last year.
        """
        a = Animal(test_params, test_properties, num_animals)
        initial_age = a.age
        a.ageing()
        assert a.age - initial_age == 1

    def test_weight_loss(self):
        """
        Checks that weight after weight loss is less than initial weight
        """
        a = Animal(test_params, test_properties, num_animals)
        initial_weight = a.weight
        a.weight_loss()
        assert a.weight < initial_weight


    def test_eat(self):
        """
        Checks that animal has gained weight after eating.
        """
        a = Animal(test_params, test_properties, num_animals)
        test_fodder = 8
        initial_weight = a.weight
        a.eat(test_fodder)
        assert a.weight > initial_weight



    def test_fitness_between_zero_and_one(self):
        """
        Checks that fitness is between 0 and 1.
        """
        a = Animal(test_params, test_properties, num_animals)
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
        a = Animal(test_params, test_properties, num_animals)
        a.find_fitness()
        assert a.fitness == 0

    def test_correct_fitness(self):
        """
        Checks that fitness formula yields correct value.
        """
        a = Animal(test_params, test_properties, num_animals)
        a.find_fitness()
        assert a.fitness == approx(0.9983411986)

    def test_prob_give_birth_one_animal_in_square(self):
        """
        Asserts that if there is only one animal in the square, then the
        probability of giving birth is zero.
        """
        a = Animal(test_params, test_properties, 1)
        a.find_fitness()
        assert a.prob_give_birth == 0

    def test_prob_give_birth_weight_less_than_limit(self):
        """
        Asserts that probability of giving birth is zero if the mothers
        weight is less than a given limit.
        """
        a = Animal(test_params, test_properties, num_animals)
        a.find_fitness()
        assert a.prob_give_birth == 0

    def test_correct_prob(self):
        """
        Asserts that the calculated probability is correct.
        """
        test_properties = {
            "species": "animal",
            "age": 5,
            "weight": 40
        }
        a = Animal(test_params, test_properties, num_animals)
        a.find_fitness()
        assert a.prob_give_birth == 1

    def test_mothers_weight_large_enough(self, mocker):
        """
        Tests birth_process method.
        After birth, we check that no birth took place if the predicted baby weight
        times xi is larger than the mother's weight.
        """
        test_properties = {
        "species": "animal",
        "age": 5,
        "weight": 40
        }
        mocker.patch('random.normalvariate', return_value=5.5)
        a = Animal(test_params, test_properties, num_animals)
        assert a.weight > a.give_birth() * a.xi


        def test_mother_loses_weight(self):
        """
        Test birth_process method.
        Asserts that mother loses weight equal to xi * birth weight
        """
        test_properties = {
        "species": "animal",
        "age": 5,
        "weight": 40
        }
        mocker.patch('random.normalvariate', return_value=5.5)
        a = Animal(test_params, test_properties, num_animals)
        initial_weight = a.weight
        birth_weight = a.birth_process()
        assert a.weight == initial_weight - (a.xi * birth_weight)

    def test_birth_weight_different_from_zero(self):
        """
        Tests birth_process method.
        Asserts that no baby is born with weight equal to zero.
        """
        pass


    def test_death():
        """ Asserts that animal dies if fitness equals zero.
        Assert that animal dies probability of dying is 1. """
        pass
