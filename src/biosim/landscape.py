# -*- coding: utf-8 -*-

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idaln@hotmail.com & kjkv@nmbu.no"


class Jungle:
    """
    Class for Jungle landscape type.
    """
    params = {
        "f_max": 800,
    }

    def __init__(self, fodder_amount):
        """
        Initializes class with given properties.
        """
        self.fodder_amount = fodder_amount

    def regrowth(self):
        """
        Sets amount of fodder to maximum after each year.
        :return:
        """