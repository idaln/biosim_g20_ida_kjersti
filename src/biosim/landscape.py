# -*- coding: utf-8 -*-

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idaln@hotmail.com & kjkv@nmbu.no"

from biosim.animals import Animal, Herbivore


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
        self.num_carn = len(self.pop_carn)
        self.num_herb = len(self.pop_herb)

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
        desired_fodder = herbivore.params["F"]
        old_fodder = self.fodder_amount
        if self.fodder_amount >= desired_fodder:
            self.fodder_amount -= desired_fodder
            return desired_fodder
        elif 0 < self.fodder_amount < desired_fodder:
            self.fodder_amount = 0
            return old_fodder
        else:
            return 0
