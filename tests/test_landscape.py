# -*- coding: utf-8 -*-

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idaln@hotmail.com & kjkv@nmbu.no"

from biosim.landscape import Jungle


class TestJungle:
    """
    Tests for Jungle class.
    """
    def test_constructor(self):
        """
        Asserts that class instance has been initialized with given amount of
        fodder.
        """
        j = Jungle(fodder_amount=400)
        assert j.fodder_amount == 400

    def test_regrowth(self):
        """
        Asserts that amount of fodder is equal f_max after each year.
        """
        j = Jungle(fodder_amount=400)
        j.regrowth()
        assert j.fodder_amount == j.params['f_max']

    def test_enough_fodder_is_available(self):
        """
        Asserts that herbivore is provided with the amount it desires, when
        enough fodder is available
        """

    def test_restricted_amount_of_fodder_is_available(self):
        """
        Asserts that all of the fodder is provided to the herbivore when it's
        demand is larger than the amount of fodder available.
        """

    def test_no_fodder_available(self):
        """
        Asserts that no fodder is provided to the herbivore when there is no
        fodder available
        """

