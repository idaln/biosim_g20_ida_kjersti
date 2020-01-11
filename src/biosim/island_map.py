# -*- coding: utf-8 -*-

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idna@nmbu.no & kjkv@nmbu.no"

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
        self.geogr = textwrap.dedent(geogr)
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

    def feeding_season(self):
        """
        Iterates through all landscape cells on the map,
        and feeds all herbivores in each cell.
        """
        for landscape in self.map.values():
            landscape.feed_all_herbivores()

    def procreation_season(self):
        """
        Iterates through all landscape cells on the map,
        and tries to procreate with all animals in each cell.
        """
        for landscape in self.map.values():
            landscape.add_newborn_animals()

    def migration_season(self):
        """
        Iterates through all landscape cells on the map,
        and tries to move all animals in each cell.
        """
        pass

    def aging_season(self):
        """
        Iterates through all landscape cells on the map,
        and makes all animals in each cell older.
        """
        for landscape in self.map.values():
            landscape.make_all_animals_older()

    def weight_loss_season(self):
        """
        Iterates through all landscape cells on the map,
        and makes all animals in each cell lose weight.
        """
        for landscape in self.map.values():
            landscape.make_all_animals_lose_weight()

    def dying_season(self):
        """
        Iterates through all landscape cells on the map,
        and removes all dead animals in each cell.
        """
        for landscape in self.map.values():
            landscape.remove_all_dead_animals()

    def run_all_seasons(self):
        """
        Runs all seasons for all landscape cells on the map.
        """
        self.feeding_season()
        self.procreation_season()
        self.migration_season()
        self.aging_season()
        self.weight_loss_season()
        self.dying_season()


if __name__ == "__main__":
    test_geogr = """\
                    JJ
                    JJ
                    """

    test_ini_pop = [
        {
            "loc": (1, 2),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(8)
            ]
        },
        {
            "loc": (2, 2),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(8)
            ]
        }

    ]

    i_m = IslandMap(test_geogr, test_ini_pop)
    i_m.create_map_dict()

    for year in range(10):
        i_m.run_all_seasons()

    for loc, cell in i_m.map.items():
        print(f"Size of population in cell {loc}: {len(cell.pop_herb)}")
        for herb in cell.pop_herb:
            herb.find_fitness()
            print(f"Fitness: {herb.fitness}, Age: {herb.age}")
