# -*- coding: utf-8 -*-

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idna@nmbu.no & kjkv@nmbu.no"

from biosim.landscape import Jungle, Savannah, Desert, Mountain, Ocean
import textwrap


class IslandMap:
    """
    Class that contains all island cells.
    """
    def __init__(self, geogr, ini_pop):
        """
        Initialize map class with given island map and initial population
        of the various cells.
        :param geogr: string
        :param ini_pop: list of dictionaries
        """
        self.geography = {}
        self.population = {}
        self.map = {}
        self.geogr = textwrap.dedent(geogr)
        self.ini_pop = ini_pop

    def create_geography_dict(self):
        """
        Converts string map to a dictionary with coordinates as keys and
        the landscape types as values.
        """
        x_coord = 0
        for line in self.geogr.splitlines():
            y_coord = 0
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
            elif landscape_type is "S":
                if loc in self.population.keys():
                    self.map[loc] = Savannah(self.population[loc])
                else:
                    self.map[loc] = Savannah([])
            elif landscape_type is "D":
                if loc in self.population.keys():
                    self.map[loc] = Desert(self.population[loc])
                else:
                    self.map[loc] = Desert([])
            elif landscape_type is "O":
                self.map[loc] = Ocean([])
            else:
                self.map[loc] = Mountain([])

    def feeding_season(self):
        """
        Iterates through all landscape cells on the map,
        and feeds all herbivores in each cell.
        """
        for landscape in self.map.values():
            landscape.feed_all_herbivores()
            landscape.feed_all_carnivores()

    def procreation_season(self):
        """
        Iterates through all landscape cells on the map,
        and tries to procreate with all animals in each cell.
        """
        for landscape in self.map.values():
            landscape.add_newborn_animals()

    def neighbours_of_current_cell(self, current_coordinates):
        """
        Finds all neighbours of a given cell, and those an animal can
        move to are returned.
        :param current_coordinates: tuple
                Location of current cell
        :returns: dict
                Has locations as keys and landscape class instance as values.
        """
        neighbours_of_current_cell = {}
        n, m = current_coordinates[0], current_coordinates[1]
        neighbours = [(n-1, m), (n, m-1), (n, m+1), (n+1, m)]
        for neighbour in neighbours:
            if neighbour in self.map.keys():
                landscape_type = type(self.map[neighbour]).__name__
                if landscape_type is not "Mountain":
                    if landscape_type is not "Ocean":
                        neighbours_of_current_cell[neighbour] = \
                            self.map[neighbour]
        return neighbours_of_current_cell

    def move_single_animal(self, current_coordinates, single_animal):
        """
        Moves an animal to the chosen neighbouring cell. New and old cell get
        updated population lists.
        :param current_coordinates: tuple
        :param single_animal: class instance of animal class
        """
        if single_animal.has_moved_this_year is False:
            neighbours_of_current_cell = self.neighbours_of_current_cell(
                current_coordinates
            )
            new_coordinates = single_animal.return_new_coordinates(
                neighbours_of_current_cell
            )
            if new_coordinates is not None:
                if type(single_animal).__name__ is "Herbivore":
                    self.map[new_coordinates].pop_herb.append(single_animal)
                    return True
                else:
                    self.map[new_coordinates].pop_carn.append(single_animal)
                    return True

    def move_all_animals_in_cell(self, current_coordinates, current_landscape):
        """
        Iterates through the population of a cell, and moves all animals.
        :param current_coordinates: tuple
        :param current_landscape: class instance
        """
        current_landscape.pop_herb = [
            animal for animal in current_landscape.pop_herb
            if not self.move_single_animal(current_coordinates, animal)
        ]
        current_landscape.pop_carn = [
            animal for animal in current_landscape.pop_carn
            if not self.move_single_animal(current_coordinates, animal)
        ]

    def migration_season(self):
        """
        Iterates through all landscape cells on the map,
        and moves all animals in each cell.
        """
        for location, landscape in self.map.items():
            self.move_all_animals_in_cell(location, landscape)

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
                    SJSJO
                    SSJSS
                    JMJJJ
                    """

    test_ini_pop = [
        {
            "loc": (2, 2),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 20}
                for _ in range(6)
            ]
        },
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(12)
            ]
        }
    ]

    i_m = IslandMap(test_geogr, test_ini_pop)
    i_m.create_map_dict()
    for _ in range(10):
        sum_animals = 0
        #print(i_m.map)
        for loc, cell in i_m.map.items():
            print(f"Population of cell {loc} is "
                  f"{len(cell.pop_carn)+len(cell.pop_herb)}")
            sum_animals += len(cell.pop_carn)
            sum_animals += len(cell.pop_herb)
        i_m.run_all_seasons()
        print(f"Total population of island is {sum_animals}")
