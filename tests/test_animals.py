# -*- coding: utf-8 -*-


__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idaln@hotmail.com & kjkv@nmbu.no"

from biosim.animals import Animal

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


class TestAnimal:
    """Tests for Animal class"""
    def test_constructor(self):
        """
        Checks that class has been initialized and some parameters have
        been unpacked correctly.
        """
        a = Animal(test_params, test_properties)
        assert a.age == 5
        assert a.a_half == 60
        assert a.omega == 0.9

    def test_ageing(self):
        """ Checks that animal is one year older than last year."""
        a = Animal(test_params, test_properties)
        first_age = a.age
        a.ageing()
        second_age = a.age
        assert second_age - first_age == 1

    def test_weight_loss():
        """ Checks that weight after weight loss is less than initial weight"""
        pass

    def test_eat():
        """ Checks that animal has gained weight after eating."""
        pass

    def test_fitness():
        """ Checks that fitness is between 0 and 1."""
        pass

    def test_give_birth():
        """ Before birth we check that no birth takes place if there is only one
        animal in the cell or the mother's weight is less than a given limit.
        After birth, we check that no birth took place if the predicted baby weight
        times xi is larger than the mother's weight. If birth has taken place,
        we check that we mother has lost weight xi * baby's birth weight. """
        pass

    def test_death():
        """ Asserts that animal dies if fitness equals zero.
        Assert that animal dies probability of dying is 1. """
        pass
