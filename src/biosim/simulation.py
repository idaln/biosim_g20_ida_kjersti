# -*- coding: utf-8 -*-

"""
"""
from biosim.animals import Animal, Herbivore, Carnivore
from biosim.landscape import Landscape, Jungle, Savannah, Desert, Mountain, \
    Ocean
from biosim.island_map import IslandMap
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
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self.island_map = IslandMap(island_map, ini_pop)
        self.island_map.create_map_dict()

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

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """

    @property
    def year(self):
        """Last year simulated."""

    @property
    def num_animals(self):
        """Total number of animals on island."""

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell on island."""

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""


if __name__ == "__main__":
    Jungle.params["f_max"] = 800
    biosim = BioSim(island_map="OO\nOO", ini_pop=[], seed=1)
    biosim.set_landscape_parameters("S", {"f_max": 300, "alpha": 0.3})
    biosim.set_landscape_parameters("J", {"f_max": 800})
