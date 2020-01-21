# -*- coding: utf-8 -*-

"""
This module provides the class for implementing the island.
"""

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idna@nmbu.no & kjkv@nmbu.no"

from biosim.landscape import Jungle, Savannah, Desert, Mountain, Ocean
from biosim.animals import Animal, Herbivore, Carnivore
import textwrap


class IslandMap:
    """
    Implements the island map. Map has one cell per location, represented by
    instances of landscape types. There are several seasons for the animals
    on the island, e.g. for feeding and procreating, and all seasons run
    from the Island Map class.
    """
    def __init__(self, island_geography, initial_population):
        """
        Initialize map class with given island geography and initial population
        of the various cells.

        :param island_geography: Specifies island geography
        :type island_geography: multiline str
        :param initial_population: Specifies initial population of each cell
        :type initial_population: list of dicts
        """
        self.geography = {}
        self.population = {}
        self.map = {}
        self.geogr = textwrap.dedent(island_geography)
        self.ini_pop = initial_population

    def check_boundaries_are_ocean(self):
        """
        Checks that all boundary cells for the map are Ocean.

        :raise ValueError: if a boundary cell is other landscape type than
            Ocean
        """
        map_lines = []
        for line in self.geogr.splitlines():
            map_lines.append(line)

        for line_num in range(len(map_lines)):
            # checks all cells in first line of geography str
            if line_num == 0:
                for landscape_type in map_lines[line_num]:
                    if landscape_type is not "O":
                        raise ValueError("Map boundary has to be only 'O'")
            # checks left- and rightmost cell in middle lines of geography str
            elif 0 < line_num < (len(map_lines) - 1):
                if map_lines[line_num][0] is not "O":
                    raise ValueError("Map boundary has to be only 'O'")
                elif map_lines[line_num][-1] is not "O":
                    raise ValueError("Map boundary has to be only 'O'")
            # checks all cells in last line of geography str
            else:
                for landscape_type in map_lines[line_num]:
                    if landscape_type is not "O":
                        raise ValueError("Map boundary has to be only 'O'")

    def check_map_lines_have_equal_length(self):
        """
        Checks that all lines in the map's geography string are of equal
        length.

        :raise ValueError: if lines in map str are more than one length
        """
        line_lengths = []
        for line in self.geogr.splitlines():
            line_lengths.append(len(line))

        if len(set(line_lengths)) != 1:
            raise ValueError(f"Inconsistent line length.")

    def create_geography_dict(self):
        """
        Converts geography string to a dictionary with coordinates as keys and
        the landscape types as values. Coordinates are a tuple of x and y
        coordinates.
        """
        self.check_boundaries_are_ocean()
        self.check_map_lines_have_equal_length()

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
        and lists of the properties of the animals at this location as values.
        """
        for cell_info in self.ini_pop:
            if cell_info["loc"] in self.population.keys():
                self.population[cell_info["loc"]].extend(cell_info["pop"])
            else:
                self.population[cell_info["loc"]] = cell_info["pop"]

    def add_population(self, population):
        """
        Adds a new population to the already existing population of the island.
        First converts list of dictionaries to a dictionary with coordinates
        as keys and lists of the properties of the animals at this location as
        values.

        :param population: Specifies the new population of one or more cells
        :type population: list

        """
        new_pop = {}
        for pop_info in population:
            new_pop[pop_info["loc"]] = pop_info["pop"]

        for loc, pop in new_pop.items():
            for individual in pop:
                if individual["species"] == "Carnivore":
                    self.map[loc].pop_carn.append(Carnivore(individual))
                else:
                    self.map[loc].pop_herb.append(Herbivore(individual))

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
            elif landscape_type is "M":
                self.map[loc] = Mountain([])
            else:
                raise ValueError(f"Invalid landscape type {landscape_type}")

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
        Moves an animal to the chosen neighbouring cell. New cell get
        updated population lists.
        :param current_coordinates: tuple
                Contains x coordinate, y coordinate
        :param single_animal: class instance
                Either herbivore and carnivore
        :returns: bool
                True if animal has moved
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
        Iterates through the population of a cell. Attempt to move all animals,
        and updates animal population lists if an animal moved.
        :param current_coordinates: tuple
                Contains x coordinate, y coordinate
        :param current_landscape: class instance
                Either herbivore and carnivore
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
