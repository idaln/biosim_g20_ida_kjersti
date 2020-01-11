# -*- coding: utf-8 -*-

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idna@nmbu.no & kjkv@nmbu.no"

from biosim.island_map import IslandMap
from biosim.landscape import Jungle
from biosim.animals import Herbivore

test_geogr = """\
                JJ
                JJ
                """
test_ini_pop = [
    {
        "loc": (1, 2),
        "pop": [
            {"species": "Herbivore", "age": 5, "weight": 20}
            for _ in range(3)
        ]
    },
    {
        "loc": (2, 2),
        "pop": [
            {"species": "Herbivore", "age": 5, "weight": 20}
            for _ in range(3)
        ]
    }

]

class TestIslandMap:

    def test_contructor(self):
        """
        Asserts that an instance of the IslandMap class can be constructed.
        """
        i_m = IslandMap(test_geogr, test_ini_pop)
        assert isinstance(i_m, IslandMap)
