# -*- coding: utf-8 -*-

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idna@nmbu.no & kjkv@nmbu.no"

from biosim.island_map import IslandMap
import pytest


class TestIslandMap:
    """
    Tests for IslandMap class.
    """
    @pytest.fixture
    def example_geogr(self):
        return """\
                JJ
                JJ
                """

    @pytest.fixture
    def example_ini_pop(self):
        return [
        {
            "loc": (0, 1),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(3)
            ]
        },
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(3)
            ]
        }
    ]

    def test_contructor(self, example_geogr, example_ini_pop):
        """
        Asserts that an instance of the IslandMap class can be constructed.
        """
        island_map = IslandMap(example_geogr, example_ini_pop)
        assert isinstance(island_map, IslandMap)

    def test_geography_is_converted_correctly_to_dict(
            self, example_ini_pop
    ):
        """
        Asserts that the create_geography method creates a dictionary that is
        converted correctly.
        """
        geogr_convert = """\
                           JO
                           DM
                           """
        island_map = IslandMap(geogr_convert, example_ini_pop)
        island_map.create_geography_dict()
        assert type(island_map.geography) is dict
        assert island_map.geography == {
            (0, 0): 'J', (0, 1): 'O', (1, 0): 'D', (1, 1): 'M'
        }

    def test_population_is_converted_correctly_to_dict(
            self, example_geogr, example_ini_pop
    ):
        """
        Asserts that the create_population method created a dictionary that is
        converted correctly.
        """
        island_map = IslandMap(example_geogr, example_ini_pop)
        island_map.create_population_dict()
        assert type(island_map.population) is dict
        assert island_map.population == {
            (0, 1): [
                {'species': 'Herbivore', 'age': 5, 'weight': 20},
                {'species': 'Herbivore', 'age': 5, 'weight': 20},
                {'species': 'Herbivore', 'age': 5, 'weight': 20}
            ],
            (1, 1): [
                {'species': 'Herbivore', 'age': 5, 'weight': 20},
                {'species': 'Herbivore', 'age': 5, 'weight': 20},
                {'species': 'Herbivore', 'age': 5, 'weight': 20}
            ]
        }

    def test_map_is_dict(self, example_geogr, example_ini_pop):
        """
        Asserts that the create_landscape_cells_with_population created a
        dictionary
        """
        island_map = IslandMap(example_geogr, example_ini_pop)
        island_map.create_map_dict()
        assert type(island_map.map) is dict

    def test_map_includes_all_landscape_types(self, example_ini_pop):
        """
        Asserts that map can be created with all landscape types.
        :param example_ini_pop: list
                Initial population
        """
        all_types = """\
                        JO
                        DM
                        SJ
                        """
        island_map = IslandMap(all_types, example_ini_pop)
        island_map.create_map_dict()
        assert type(island_map.map[(0, 0)]).__name__ is "Jungle"
        assert type(island_map.map[(0, 1)]).__name__ is "Ocean"
        assert type(island_map.map[(1, 0)]).__name__ is "Desert"
        assert type(island_map.map[(1, 1)]).__name__ is "Mountain"
        assert type(island_map.map[(2, 0)]).__name__ is "Savannah"

    def test_feeding_season(self, example_geogr, example_ini_pop):
        """
        Asserts that one animal in each cell of the test island
        have been fed.
        """
        island_map = IslandMap(example_geogr, example_ini_pop)
        island_map.create_map_dict()
        island_map.feeding_season()
        assert island_map.map[(0, 1)].pop_herb[0].weight > \
            example_ini_pop[0]["pop"][0]["weight"]
        assert island_map.map[(1, 1)].pop_herb[0].weight > \
            example_ini_pop[1]["pop"][0]["weight"]

    def test_all_animals_gave_birth(
            self, mocker, example_ini_pop, example_geogr
    ):
        """
        Asserts that all animals on island give birth when their probability
        of giving birth is one.
        :param example_ini_pop: list
                Initial population
        :param example_geogr: str
                Map
        :return:
        """
        mocker.patch("numpy.random.random", return_value=0.01)
        island_map = IslandMap(example_geogr, example_ini_pop)
        ini_sum_animals = 0
        for cell in island_map.map.values():
            ini_sum_animals += len(cell.pop_herb)
            ini_sum_animals += len(cell.pop_carn)
        island_map.procreation_season()
        sum_animals = 0
        for cell in island_map.map.values():
            sum_animals += len(cell.pop_herb)
            sum_animals += len(cell.pop_carn)
        assert sum_animals == 2 * ini_sum_animals

    def test_four_correct_neighbours(self, example_ini_pop):
        """
        Asserts that the neighbours_of_current_cell method return the
        correct neighbours of a cell with four neighbours.
        """
        geogr_neighbour = """\
                                  JJJ    
                                  JJJ
                                  JJJ
                                  """
        island_map = IslandMap(geogr_neighbour, example_ini_pop)
        island_map.create_map_dict()

        dict_with_neighbours = island_map.neighbours_of_current_cell((1, 1))
        neighbours = [(0, 1), (1, 0), (1, 2), (2, 1)]
        for neighbour in dict_with_neighbours.keys():
            assert neighbour in neighbours

    def test_two_correct_neighbours(self, example_geogr, example_ini_pop):
        """
        Asserts that the neighbours_of_current_cell method return the
        correct neighbours for a cell with only two neighbours.
        """
        island_map = IslandMap(example_geogr, example_ini_pop)
        island_map.create_map_dict()

        dict_with_neighbours = island_map.neighbours_of_current_cell((0, 0))
        neighbours = [(0, 1), (1, 0)]
        for neighbour in dict_with_neighbours.keys():
            assert neighbour in neighbours

    def test_zero_neighbours(self, example_ini_pop):
        """
        Asserts that the neighbours_of_current_cell method handles a cell
        with no neighbours.
        :param example_ini_pop: list of dicts
                Initial population of map
        """
        geogr_one_cell = """\
                            J
                            """
        island_map = IslandMap(geogr_one_cell, example_ini_pop)
        island_map.create_map_dict()
        dict_with_neighbours = island_map.neighbours_of_current_cell((0, 0))
        assert dict_with_neighbours == {}

    def test_all_animals_aged(self, example_ini_pop, example_geogr):
        """
        Asserts that all animals on the island on the island have aged.
        :param example_ini_pop: list
                Initial population of animals saved in one dict per animal.
        :param example_geogr: str
                Island geography
        :return:
        """
        island_map = IslandMap(example_geogr, example_ini_pop)
        island_map.create_map_dict()
        island_map.aging_season()
        initial_age_animal = example_ini_pop[0]["pop"][0]["age"]
        for cell in island_map.map.values():
            for animal in cell.pop_herb+cell.pop_carn:
                assert animal.age > initial_age_animal

    def test_all_animals_lost_weight(self, example_ini_pop, example_geogr):
        """
        Asserts that all animals on the island on the island has lost weight.
        :param example_ini_pop: list
                Initial population of animals saved in one dict per animal.
                All animals have same initial weight.
        :param example_geogr: str
                Island geography
        :return:
        """
        island_map = IslandMap(example_geogr, example_ini_pop)
        island_map.create_map_dict()
        island_map.weight_loss_season()
        initial_weight_animal = example_ini_pop[0]["pop"][0]["weight"]
        for cell in island_map.map.values():
            for animal in cell.pop_herb+cell.pop_carn:
                assert animal.weight < initial_weight_animal

    def test_all_animals_die(self, mocker, example_ini_pop, example_geogr):
        """
        Asserts that all animals on island die, when the random number that
        decides has been mocked to ensure all animals die.
        :param example_ini_pop: list
                Initial population
        :param example_geogr: str
                Map
        :return:
        """
        mocker.patch("numpy.random.random", return_value=1)
        island_map = IslandMap(example_geogr, example_ini_pop)
        island_map.dying_season()
        sum_animals = 0
        for cell in island_map.map.values():
            sum_animals += len(cell.pop_herb)
            sum_animals += len(cell.pop_carn)
        assert sum_animals == 0
