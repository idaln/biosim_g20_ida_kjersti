# -*- coding: utf-8 -*-

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idna@nmbu.no & kjkv@nmbu.no"

from biosim.animals import Herbivore
from biosim.landscape import Jungle
import textwrap


class IslandMap:
    """
    Class that contains all island cells.
    """
    geography = {}
    population = {}
    map = {}

    def __init__(self, geogr, ini_pop):
        """
        Initialize map class with given island map and initial population
        of the various cells.
        :param geogr: string
        :param ini_pop: list of dictionaries
        """
        self.geogr= textwrap.dedent(geogr)
        self.ini_pop = ini_pop

    def create_geography_dict(self):
        """
        Converts string map to a dictionary with coordinates as keys and
        the landscape types as values.
        """
        x_coord = 1
        for line in self.geogr.splitlines():
            y_coord = 1
            for landscape_type in line:
                self.geography[(x_coord, y_coord)] = landscape_type
                y_coord += 1
            x_coord += 1

    def create_population_dict(self):
        """
        Converts list of populations to a dictionary with coordinates as keys
        and lists of animals at this location as values.
        """
        for pop_info in self.ini_pop:
            self.population[pop_info["loc"]] = pop_info["pop"]

    def create_map_dict(self):
        """
        Creates dictionary of the entire map, with coordinates as keys and
        instances of landscape classes as values. The instances have the
        population of the coordinate as input.
        """
        self.create_geography_dict()
        self.create_population_dict()
        for loc, landscape_type in self.geography.items():
            if landscape_type is "J":
                if loc in self.population.keys():
                    self.map[loc] = Jungle(self.population[loc])
                else:
                    self.map[loc] = Jungle([])


if __name__ == "__main__":
    geogr = """\
               OOOOOOOOSMMMMJJJJJJJO
               OOOOOOOOOOOOOOOOOOOOO
               OSSSSSJJJJMMJJJJJJJOO
               OSSSSSSSSSMMJJJJJJOOO
               OSSSSSJJJJJJJJJJJJOOO
               OSSSSSJJJDDJJJSJJJOOO
               OSSJJJJJDDDJJJSSSSOOO
               OOSSSSJJJDDJJJSOOOOOO
               OSSSJJJJJDDJJJJJJJOOO
               OSSSSJJJJDDJJJJOOOOOO
               OOSSSSJJJJJJJJOOOOOOO
               OOOSSSSJJJJJJJOOOOOOO
               OOOOOOOOOOOOOOOOOOOOO"""

    t_geogr = """\
                    JJJJ
                    JJJJ
                    JJJJ
                    JJJJ"""

    ini_herbs = [
        {
            "loc": (1,2),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(3)
            ]
        },
        {
            "loc": (3,3),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(10)
            ]
        }

    ]

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

    i = IslandMap(test_geogr, test_ini_pop)
    #i.create_geography()
    #print(i.geography)
    #i.create_population()
    #print(i.population)
    i.create_map_dict()
    print(i.map)
