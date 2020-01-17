# -*- coding: utf-8 -*-

"""
"""
from biosim.animals import Animal, Herbivore, Carnivore
from biosim.landscape import Landscape, Jungle, Savannah, Desert, Mountain, \
    Ocean
from biosim.island_map import IslandMap
import pandas
import random
__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idaln@hotmail.com & kjkv@nmbu.no"


class BioSim:
    def __init__(
        self,
        island_map,
        ini_pop,
        seed,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing
        animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal
        densities
        :param img_base: String with beginning of file name for figures,
        including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted
        automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        random.seed()
        self.island_map = IslandMap(island_map, ini_pop)
        self.island_map.create_map_dict()
        self.num_years_simulated = 0

    @staticmethod
    def reset_params():
        for class_name in [Landscape, Jungle, Savannah, Desert, Mountain,
                           Ocean, Animal, Herbivore, Carnivore]:
            class_name.reset_params()

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.
        All animal parameters shall be positive. However, DeltaPhiMax shall be
        strictly positive and eta shall lie between zero and one.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        class_names = {"Herbivore": Herbivore,
                       "Carnivore": Carnivore}
        for param_name in params.keys():
            if param_name in class_names[species].params:
                if params[param_name] >= 0 and param_name is not "DeltaPhiMax"\
                        and param_name is not "eta":
                    class_names[species].params[param_name] = params[
                        param_name]
                elif param_name is "eta" and 0 <= params[param_name] <= 1:
                    class_names[species].params[param_name] = params[
                        param_name]
                elif param_name is "DeltaPhiMax" and params[param_name] > 0:
                    class_names[species].params[param_name] = params[
                        param_name]
                else:
                    raise ValueError(f'{params[param_name]} is an invalid '
                                     f'parameter value!')
            else:
                raise ValueError(f'{param_name} is an invalid parameter name!')

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        class_names = {'J': Jungle, 'S': Savannah, 'D': Desert, 'M': Mountain,
                       'O': Ocean}
        for param_name in params.keys():
            if param_name in class_names[landscape].params.keys():
                if param_name is "f_max" and params[param_name] >= 0:
                    class_names[landscape].params[param_name] = params[
                        param_name]
                elif param_name is "alpha":
                    class_names[landscape].params[param_name] = params[
                        param_name]
                else:
                    raise ValueError(f'{params[param_name]} is an invalid '
                                     f'parameter value!')
            else:
                raise ValueError(f'{param_name} is an invalid parameter name!')

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files
        (default: vis_years)

        Image files will be numbered consecutively.
        """
        for year in range(num_years):
            self.island_map.run_all_seasons()
            self.num_years_simulated += 1

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.island_map.add_population(population)

    @property
    def year(self):
        """Last year simulated."""
        return self.num_years_simulated

    @property
    def num_animals(self):
        """Total number of animals on island."""
        num_animals = 0
        for cell in self.island_map.map.values():
            num_animals += len(cell.pop_herb)
            num_animals += len(cell.pop_carn)
        return num_animals

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        num_animals_per_species = {"Herbivore": 0, "Carnivore": 0}
        for cell in self.island_map.map.values():
            num_animals_per_species["Herbivore"] += len(cell.pop_herb)
            num_animals_per_species["Carnivore"] += len(cell.pop_carn)
        return num_animals_per_species

    @property
    def animal_distribution(self):
        """
        Pandas DataFrame with animal count per species for each cell on island.
        """
        data_all_cells = []
        i = 0
        for coord, cell in self.island_map.map.items():
            row = coord[0]
            col = coord[1]
            herb = len(cell.pop_herb)
            carn = len(cell.pop_carn)
            data_all_cells.append([row, col, herb, carn])
            i += 1
        return pandas.DataFrame(data=data_all_cells, columns=[
            'Row', 'Col', 'Herbivore', 'Carnivore'])

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""


if __name__ == "__main__":
    ini_pop = [
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 200}
                for _ in range(6)
            ]
        },
        {
            "loc": (1, 2),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(12)
            ]
        }
    ]

    island = "OOOO\nOJSO\nOSSO\nOOOO"
    biosim = BioSim(island, ini_pop, 1)
    print(biosim.animal_distribution)
    biosim.simulate(15)
    print(biosim.animal_distribution)
