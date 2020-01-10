# -*- coding: utf-8 -*-

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idaln@hotmail.com & kjkv@nmbu.no"

from biosim.landscape import Jungle
from biosim.animals import Animal, Herbivore

test_properties_herb = {
    "species": "animal",
    "age": 5,
    "weight": 20
}


class TestJungle:
    """
    Tests for Jungle class.
    """
    def test_constructor(self):
        """
        Asserts that class instance has been initialized with no fodder
        available.
        """
        j = Jungle()
        assert j.fodder_amount is None

    def test_regrowth(self):
        """
        Asserts that amount of fodder is equal f_max after each year.
        """
        j = Jungle()
        j.regrowth()
        assert j.fodder_amount == j.params['f_max']

    def test_enough_fodder_is_available(self):
        """
        Asserts that herbivore is provided with the amount it desires, when
        enough fodder is available. Asserts that the amount of fodder
        provided is substracted from the initial fodder amount.
        """
        j = Jungle()
        h = Herbivore(test_properties_herb)
        j.regrowth()
        old_fodder_amount = j.fodder_amount
        available_fodder_to_herb = j.available_fodder_herb(h)
        assert available_fodder_to_herb == h.params["F"]
        assert j.fodder_amount == old_fodder_amount - available_fodder_to_herb

    def test_restricted_amount_of_fodder_is_available(self):
        """
        Asserts that all of the fodder is provided to the herbivore when it's
        demand is larger than the amount of fodder available. Asserts that
        the amount of fodder left now is zero.
        """
        j = Jungle()
        h = Herbivore(test_properties_herb)
        j.fodder_amount = 5
        old_fodder_amount = j.fodder_amount
        available_fodder_to_herb = j.available_fodder_herb(h)
        assert available_fodder_to_herb == 5
        assert j.fodder_amount == old_fodder_amount - available_fodder_to_herb

    def test_no_fodder_available(self):
        """
        Asserts that no fodder is provided to the herbivore when there is no
        fodder available.
        """
        j = Jungle()
        h = Herbivore(test_properties_herb)
        j.fodder_amount = 0
        assert j.available_fodder_herb(h) == 0
        assert j.fodder_amount == 0

