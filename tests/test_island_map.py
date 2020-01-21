# -*- coding: utf-8 -*-

"""
Test set for IslandMap class interface.

This set of tests checks the interface and functionality of the IslandMap class
provided by the island_map module of the biosim package.
"""

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
                OOOO
                OJJO
                OJJO
                OOOO
                """

    @pytest.fixture
    def example_ini_pop(self):
        return [
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

    def test_constructor(self, example_geogr, example_ini_pop):
        """
        Asserts that an instance of the IslandMap class can be constructed.
        """
        island_map = IslandMap(example_geogr, example_ini_pop)
        assert isinstance(island_map, IslandMap)

    def test_geography_is_converted_correctly_to_dict(
            self, example_ini_pop
    ):
        """
        Asserts that the create_geography method creates a dictionary, and
        that the dictionary has correct keys and values.
        """
        geogr_convert = """\
                            OOOO
                            OJSO
                            ODMO
                            OOOO
                            """
        island_map = IslandMap(geogr_convert, example_ini_pop)
        island_map.create_geography_dict()
        assert type(island_map.geography) is dict
        assert island_map.geography == {
            (0, 0): 'O', (0, 1): 'O', (0, 2): 'O', (0, 3): 'O',
            (1, 0): 'O', (1, 1): 'J', (1, 2): 'S', (1, 3): 'O',
            (2, 0): 'O', (2, 1): 'D', (2, 2): 'M', (2, 3): 'O',
            (3, 0): 'O', (3, 1): 'O', (3, 2): 'O', (3, 3): 'O',
        }

    def test_population_is_converted_correctly_to_dict(
            self, example_geogr, example_ini_pop
    ):
        """
        Asserts that the create_population method created a dictionary and
        that the keys and values of the dictionary have been converted
        correctly.
        """
        island_map = IslandMap(example_geogr, example_ini_pop)
        island_map.create_population_dict()
        assert type(island_map.population) is dict
        assert island_map.population == {
            (1, 2): [
                {'species': 'Herbivore', 'age': 5, 'weight': 20},
                {'species': 'Herbivore', 'age': 5, 'weight': 20},
                {'species': 'Herbivore', 'age': 5, 'weight': 20}
            ],
            (2, 2): [
                {'species': 'Herbivore', 'age': 5, 'weight': 20},
                {'species': 'Herbivore', 'age': 5, 'weight': 20},
                {'species': 'Herbivore', 'age': 5, 'weight': 20}
            ]
        }

    def test_map_of_island_is_dict(self, example_geogr, example_ini_pop):
        """
        Asserts that the create_map_dict method created a dictionary.
        """
        island_map = IslandMap(example_geogr, example_ini_pop)
        island_map.create_map_dict()
        assert type(island_map.map) is dict

    def test_map_can_include_all_landscape_types(self, example_ini_pop):
        """
        Asserts that create_map_dict can create map from a geography string
        where all landscape types are included.
        """
        all_types = """\
                        OOOO
                        ODMO
                        OSJO
                        OOOO
                        """
        island_map = IslandMap(all_types, example_ini_pop)
        island_map.create_map_dict()
        assert type(island_map.map[(0, 0)]).__name__ is "Ocean"
        assert type(island_map.map[(1, 1)]).__name__ is "Desert"
        assert type(island_map.map[(1, 2)]).__name__ is "Mountain"
        assert type(island_map.map[(2, 1)]).__name__ is "Savannah"
        assert type(island_map.map[(2, 2)]).__name__ is "Jungle"

    def test_add_animals_to_existing_population(
            self, example_ini_pop, example_geogr
    ):
        """
        Tests add_population method.
        Asserts that additional animals can be added to an existing population.
        """
        island_map = IslandMap(example_geogr, initial_population=[])
        island_map.create_map_dict()
        island_map.add_population(example_ini_pop)

    def test_one_animal_in_each_cell_has_been_fed(
            self, example_geogr, example_ini_pop
    ):
        """
        Tests feeding_season method.
        Asserts that one animal in each cell of the test island
        have been fed.
        """
        island_map = IslandMap(example_geogr, example_ini_pop)
        island_map.create_map_dict()
        island_map.feeding_season()
        assert island_map.map[(1, 2)].pop_herb[0].weight > \
            example_ini_pop[0]["pop"][0]["weight"]
        assert island_map.map[(2, 2)].pop_herb[0].weight > \
            example_ini_pop[1]["pop"][0]["weight"]

    def test_all_animals_gave_birth_when_prob_birth_is_one(
            self, mocker, example_ini_pop, example_geogr
    ):
        """
        Tests procreation_season method.
        Asserts that all animals on island give birth when their probability
        of giving birth is one.
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
        # length of population has doubled when all animals have given birth

    def test_finds_no_neighbours_when_no_habitable_cells_around(
            self, example_ini_pop
    ):
        """
        Asserts that the neighbours_of_current_cell method handles a cell
        with no habitable neighbours.
        """
        geogr_one_cell = """\
                            OOO
                            OJO
                            OOO
                            """
        island_map = IslandMap(geogr_one_cell, example_ini_pop)
        island_map.create_map_dict()
        dict_with_neighbours = island_map.neighbours_of_current_cell((1, 1))
        assert dict_with_neighbours == {}

    def test_finds_two_correct_neighbours_when_two_habitable_cells_around(
            self, example_geogr, example_ini_pop
    ):
        """
        Asserts that the neighbours_of_current_cell method return the
        correct neighbours for a cell with only two neighbours.
        """
        island_map = IslandMap(example_geogr, example_ini_pop)
        island_map.create_map_dict()
        dict_with_neighbours = island_map.neighbours_of_current_cell((1, 1))
        neighbours = [(1, 2), (2, 1)]
        for neighbour in dict_with_neighbours.keys():
            assert neighbour in neighbours

    def test_finds_four_correct_neighbours_when_four_habitable_cells_around(
            self, example_ini_pop
    ):
        """
        Asserts that the neighbours_of_current_cell method return the
        correct neighbours for a cell with four neighbours.
        """
        test_geogr = """\
                            OOOOO
                            OJJJO
                            OJJJO
                            OJJJO
                            OOOOO
                            """
        island_map = IslandMap(test_geogr, example_ini_pop)
        island_map.create_map_dict()
        dict_with_neighbours = island_map.neighbours_of_current_cell((2, 2))
        neighbours = [(1, 2), (2, 1), (2, 3), (3, 2)]
        for neighbour in dict_with_neighbours.keys():
            assert neighbour in neighbours

    def test_all_animals_move_if_rand_num_less_than_prob(
            self, mocker, example_geogr
    ):
        """
        Tests move_single_animal on several animals.
        Asserts that all animal move if they have not moved this year and
        random number is less than their probability to move.
        """
        move_ini_pop = [
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
                    {"species": "Carnivore", "age": 5, "weight": 20}
                    for _ in range(3)
                ]
            }
        ]
        mocker.patch('numpy.random.random', return_value=0.01)
        island_map = IslandMap(example_geogr, move_ini_pop)
        island_map.create_map_dict()
        for loc, cell in island_map.map.items():
            for herbivore in cell.pop_herb:
                assert island_map.move_single_animal(loc, herbivore) is True
            for carnivore in cell.pop_carn:
                assert island_map.move_single_animal(loc, carnivore) is True

    def test_animal_moves_not_if_it_has_already_moved_this_year(
            self, example_geogr, example_ini_pop
    ):
        """
        Tests move_single_animal.
        Asserts that animal does not move if it has already moved this year.
        """
        island_map = IslandMap(example_geogr, example_ini_pop)
        island_map.create_map_dict()
        herbivore = island_map.map[(1, 2)].pop_herb[0]
        herbivore.has_moved_this_year = True
        assert island_map.move_single_animal((1, 2), herbivore) is None

    def test_single_animal_moves_not_if_rand_num_higher_than_prob(
            self, mocker, example_geogr, example_ini_pop
    ):
        """
        Tests move_single_animal.
        Asserts that animal does not move if it has not moved this year, but
        the random number is higher than the probability of moving.
        """
        mocker.patch('numpy.random.random', return_value=1)
        island_map = IslandMap(example_geogr, example_ini_pop)
        island_map.create_map_dict()
        herbivore = island_map.map[(1, 2)].pop_herb[0]
        assert island_map.move_single_animal((1, 2), herbivore) is None

    def test_all_animals_move_when_rand_num_less_than_prob(
            self, mocker, example_ini_pop, example_geogr
    ):
        """
        Tests move_all_animals_in_cell.
        Asserts that all animals move out of a cell when the random number is
        less than the probability for each to move.
        """
        mocker.patch('numpy.random.random', return_value=0.0001)
        island_map = IslandMap(example_geogr, [example_ini_pop[0]])
        island_map.create_map_dict()
        island_map.move_all_animals_in_cell((1, 2), island_map.map[(1, 2)])
        final_num_animals = len(island_map.map[(1, 2)].pop_herb) + \
            len(island_map.map[(1, 2)].pop_carn)
        assert final_num_animals == 0
        # length of population is zero when all animals have moved

    def test_no_animals_move(self, mocker, example_ini_pop, example_geogr):
        """
        Tests move_all_animals_in_cell.
        Asserts that no animals move out of a cell when mocking the random
        number makes sure they will not.
        """
        mocker.patch('numpy.random.random', return_value=1)
        island_map = IslandMap(example_geogr, [example_ini_pop[0]])
        island_map.create_map_dict()
        initial_num_animals = len(island_map.map[(1, 2)].pop_herb) + \
                            len(island_map.map[(1, 2)].pop_carn)
        island_map.move_all_animals_in_cell((1, 2), island_map.map[(1, 2)])
        final_num_animals = len(island_map.map[(1, 2)].pop_herb) + \
                            len(island_map.map[(1, 2)].pop_carn)
        assert final_num_animals == initial_num_animals

    def test_all_animals_migrate(self, mocker, example_ini_pop, example_geogr):
        """
        Asserts that all animals have moved after the migration season,
        by checking their has_moved_this_year attribute.
        """
        mocker.patch('numpy.random.random', return_value=0.0001)
        island_map = IslandMap(example_geogr, [example_ini_pop[0]])
        island_map.create_map_dict()
        island_map.migration_season()
        for loc, cell in island_map.map.items():
            for animal in cell.pop_herb+cell.pop_carn:
                assert animal.has_moved_this_year is True

    def test_all_animals_aged(self, example_ini_pop, example_geogr):
        """
        Asserts that all animals on the island on the island have aged.
        :param example_ini_pop: list
                Initial population of animals saved in one dict per animal.
        :param example_geogr: str
                Island island_geography
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
                Island island_geography
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
