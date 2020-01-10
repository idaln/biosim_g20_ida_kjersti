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
    pop_carn = []
    pop_herb = []

    def __init__(self):
        """
        Initializes class.
        """
        self.fodder_amount = None

    def regrowth(self):
        """
        Sets amount of fodder for herbivores to maximum at the beginning of
        each year.
        """
        self.fodder_amount = self.params['f_max']

    def available_fodder_herb(self, herbivore):
        """
        Returns amount of fodder available to the herbivore.
        :returns: available_fodder
                  float
        """
