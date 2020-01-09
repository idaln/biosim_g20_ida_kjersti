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
