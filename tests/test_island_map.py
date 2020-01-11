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
    """
    Tests for IslandMap class.
    """
    def test_contructor(self):
        """
        Asserts that an instance of the IslandMap class can be constructed.
        """
        i_m = IslandMap(test_geogr, test_ini_pop)
        assert isinstance(i_m, IslandMap)

    def test_geography_is_converted_correctly_to_dict(self):
        """
        Asserts that the create_geography method creates a dictionary that is
        converted correctly.
        """
        i_m = IslandMap(test_geogr, test_ini_pop)
        i_m.create_geography_dict()
        assert type(i_m.geography) is dict
        assert i_m.geography == {(1, 1): 'J', (1, 2): 'J', (2, 1): 'J', (2, 2): 'J'}

    def test_population_is_converted_correctly_to_dict(self):
        """
        Asserts that the create_population method created a dictionary that is
        converted correctly.
        """
        i_m = IslandMap(test_geogr, test_ini_pop)
        i_m.create_population_dict()
        assert type(i_m.population) is dict
        assert i_m.population == {(1, 2): [{'species': 'Herbivore', 'age': 5,
                                            'weight': 20},
                                           {'species': 'Herbivore', 'age': 5,
                                            'weight': 20},
                                           {'species': 'Herbivore', 'age': 5,
                                            'weight': 20}],
                                  (2, 2): [{'species': 'Herbivore', 'age': 5,
                                            'weight': 20},
                                           {'species': 'Herbivore', 'age': 5,
                                            'weight': 20},
                                           {'species': 'Herbivore', 'age': 5,
                                            'weight': 20}]}

    def test_map_is_dict(self):
        """
        Asserts that the create_landscape_cells_with_population created a
        dictionary
        """
        i_m = IslandMap(test_geogr, test_ini_pop)
        i_m.create_map_dict()
        assert type(i_m.map) is dict

    # def test_feeding_season(self):
    #    """
    #    Asserts that one animal in each cell of the test island
    #    have been fed.
    #    """
        # i_m = IslandMap(test_geogr, test_ini_pop)
        # i_m.create_map_dict()
        # i_m.feeding_season()
        # assert i_m.map[(1, 2)][0]["weight"] > \
        #    test_ini_pop[0]["pop"][0]["weight"]
        # assert i_m.map[(2, 2)][0]["weight"] > \
        #    test_ini_pop[1]["pop"][0]["weight"]

