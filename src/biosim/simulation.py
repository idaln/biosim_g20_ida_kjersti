# -*- coding: utf-8 -*-

"""
This module provides classes organizing entire simulation, including
visualization and saving graphics.
"""

from biosim.animals import Animal, Herbivore, Carnivore
from biosim.landscape import Landscape, Jungle, Savannah, Desert, Mountain, \
    Ocean
from biosim.island_map import IslandMap
import pandas
import numpy
import matplotlib.pyplot as plt
import subprocess
from examples.population_generator import Population

__author__ = "Ida Lunde Naalsund & Kjersti Rustad Kvisberg"
__email__ = "idaln@hotmail.com & kjkv@nmbu.no"

_DEFAULT_MOVIE_FORMAT = 'mp4'
# Update this variable to point to your ffmpeg binary
FFMPEG_BINARY = 'C:/Program Files/' \
                'ffmpeg-20200115-0dc0837-win64-static/bin/ffmpeg'


class BioSim:
    """
    Class for simulating the model of an ecosystem.
    """
    def __init__(
        self,
        island_geography,
        initial_population,
        seed,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_geography: Multi-line string specifying island
            geography
        :param initial_population: List of dictionaries specifying
            initial population
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
        numpy.random.seed(seed)
        self.img_base = img_base
        self.img_fmt = img_fmt
        self.img_no = 0

        self.ymax = ymax_animals
        if cmax_animals is None:
            self.cmax = {'Herbivore': 300, 'Carnivore': 100}
        else:
            self.cmax = cmax_animals

        self.island_map = IslandMap(island_geography, initial_population)
        self.island_map.create_map_dict()
        self.num_years_simulated = 0
        self.final_year = None

        # The following will be initialized by setup_graphics
        self._fig = None
        self._line_graph_ax = None
        self._line_graph_line_herb = None
        self._line_graph_line_carn = None
        self._map_ax = None
        self._img_axis = None
        self._heat_map_herb_ax = None
        self._img_herb_axis = None
        self._heat_map_carn_ax = None
        self._img_carn_axis = None

    @staticmethod
    def reset_params():
        """
        Resets parameters of all landscape and animal classes.
        """
        for class_name in [Landscape, Jungle, Savannah, Desert, Mountain,
                           Ocean, Animal, Herbivore, Carnivore]:
            class_name.reset_params()

    @staticmethod
    def set_animal_parameters(species, params):
        """
        Set parameters for animal species.
        All animal parameters shall be positive. However, DeltaPhiMax and
        F shall be strictly positive and eta shall lie between zero and one.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        :raise ValueError: if parameter has invalid value or name
        """
        class_names = {"Herbivore": Herbivore,
                       "Carnivore": Carnivore}
        for param_name in params.keys():
            if param_name in class_names[species].params:
                if params[param_name] >= 0 and param_name is not "DeltaPhiMax"\
                        and param_name is not "eta" and param_name is not "F":
                    class_names[species].params[param_name] = params[
                        param_name]
                # checks special criteria for eta
                elif param_name is "eta" and 0 <= params[param_name] <= 1:
                    class_names[species].params[param_name] = params[
                        param_name]
                # checks special criteria for F
                elif param_name is "F" and 0 < params[param_name]:
                    class_names[species].params[param_name] = params[
                        param_name]
                # checks special criteria for DeltaPhiMax
                elif param_name is "DeltaPhiMax" and params[param_name] > 0:
                    class_names[species].params[param_name] = params[
                        param_name]
                else:
                    raise ValueError(f'{params[param_name]} is an invalid '
                                     f'parameter value for parameter '
                                     f'{param_name}!')
            else:
                raise ValueError(f'{param_name} is an invalid parameter name!')

    @staticmethod
    def set_landscape_parameters(landscape, params):
        """
        Set parameters for landscape type. f_max must be positive.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        :raise ValueError: if parameter name or value is invalid
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

    def add_population(self, population):
        """
        Add a population to the island during simulation.

        :param population: List of dictionaries specifying population
        """
        self.island_map.add_population(population)

    @property
    def year(self):
        """
        Last year simulated.
        """
        return self.num_years_simulated

    @property
    def num_animals(self):
        """
        Total number of animals on island.
        """
        num_animals = 0
        for cell in self.island_map.map.values():
            num_animals += len(cell.pop_herb)
            num_animals += len(cell.pop_carn)
        return num_animals

    @property
    def num_animals_per_species(self):
        """
        Number of animals per species in island, as dictionary.
        """
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

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files
            (default: vis_years)

        Image files will be numbered consecutively.
        """
        if img_years is None:
            img_years = vis_years

        self.final_year = self.year + num_years
        self.setup_graphics()

        while self.year < self.final_year:

            if self.year % vis_years == 0:
                self.update_graphics()

            if self.year % img_years == 0:
                self.save_graphics()

            self.island_map.run_all_seasons()
            self.num_years_simulated += 1

    def setup_graphics(self):
        """
        Creates four subplots for visualization of geography, number of
        animals per species and distribution of each species.
        """
        # Create new figure window
        if self._fig is None:
            self._fig = plt.figure(figsize=(13, 8))
            self._fig.subplots_adjust(hspace=0.2, wspace=0.2)

        # Add upper left subplot with features for map of island
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(2, 2, 1)
            self._map_ax.set_position(pos=[0, 0.55, 0.4, 0.3])
            self.create_map_graphics()
            self._map_ax.title.set_text('Island')

        # Add upper right subplot for line graph of herbivore and carnivore
        # populations.
        if self._line_graph_ax is None:
            self._line_graph_ax = self._fig.add_subplot(2, 2, 2)
            self._line_graph_ax.set_position(pos=[0.5, 0.55, 0.35, 0.35])

        # Needs updating on subsequent calls to simulate()
        self._line_graph_ax.set_xlim(0, self.final_year + 1)

        # Line graph for herbivores
        if self._line_graph_line_herb is None:
            line_graph_plot_herb = self._line_graph_ax.plot(
                numpy.arange(0, self.final_year),
                numpy.full(self.final_year, numpy.nan)
            )
            self._line_graph_line_herb = line_graph_plot_herb[0]
        else:
            xdata, ydata = self._line_graph_line_herb.get_data()
            xnew = numpy.arange(xdata[-1] + 1, self.final_year)
            if len(xnew) > 0:
                ynew = numpy.full(xnew.shape, numpy.nan)
                self._line_graph_line_herb.set_data(
                    numpy.hstack((xdata, xnew)), numpy.hstack((ydata, ynew))
                )

        # Line graph for carnivores
        if self._line_graph_line_carn is None:
            line_graph_plot_carn = self._line_graph_ax.plot(
                numpy.arange(0, self.final_year),
                numpy.full(self.final_year, numpy.nan)
            )
            self._line_graph_line_carn = line_graph_plot_carn[0]
        else:
            xdata, ydata = self._line_graph_line_carn.get_data()
            xnew = numpy.arange(xdata[-1] + 1, self.final_year)
            if len(xnew) > 0:
                ynew = numpy.full(xnew.shape, numpy.nan)
                self._line_graph_line_carn.set_data(
                    numpy.hstack((xdata, xnew)),
                    numpy.hstack((ydata, ynew))
                )
        # Features for line graph
        self._line_graph_ax.yaxis.tick_right()
        self._line_graph_ax.yaxis.set_label_position('right')
        self._line_graph_ax.legend(["Herbivore", "Carnivore"], loc='best')
        self._line_graph_ax.title.set_text('Population dynamics')
        self._line_graph_ax.set_ylabel('Number of animals')
        self._line_graph_ax.set_xlabel('Year')

        # Add lower left heat map for herbivores
        if self._heat_map_herb_ax is None:
            self._heat_map_herb_ax = self._fig.add_subplot(2, 2, 3)
            self._heat_map_herb_ax.set_position(pos=[0, 0, 0.4, 0.4])
            self._img_herb_axis = None

        # Features for herbivore heat map
        self._heat_map_herb_ax.title.set_text('Herbivore distribution')
        self._heat_map_herb_ax.set_ylabel('y coordinate')
        self._heat_map_herb_ax.set_xlabel('x coordinate')

        # Add lower right heat map for carnivores
        if self._heat_map_carn_ax is None:
            self._heat_map_carn_ax = self._fig.add_subplot(2, 2, 4)
            self._heat_map_carn_ax.set_position(pos=[0.5, 0, 0.4, 0.4])
            self._img_carn_axis = None

        # Features for carnivore heat map
        self._heat_map_carn_ax.title.set_text('Carnivore distribution')
        self._heat_map_carn_ax.set_ylabel('y coordinate')
        self._heat_map_carn_ax.set_xlabel('x coordinate')

    def create_map_graphics(self):
        """
        Creates graphic of the map of the island's island_geography. The
        island map is static and the different landscape types are represented
        by different colours.
        """
        #                   R    G    B
        rgb_value = {'O': (0.0, 0.0, 1.0),  # blue
                     'M': (0.5, 0.5, 0.5),  # grey
                     'J': (0.0, 0.6, 0.0),  # dark green
                     'S': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        geogr_rgb = [[rgb_value[column] for column in row]
                     for row in self.island_map.geogr.splitlines()]

        axim = self._map_ax
        axim.imshow(geogr_rgb)
        axim.set_xticks(range(len(geogr_rgb[0])))
        axim.set_xticklabels(range(1, 1 + len(geogr_rgb[0])))
        axim.set_yticks(range(len(geogr_rgb)))
        axim.set_yticklabels(range(1, 1 + len(geogr_rgb)))
        axim.set_ylabel('y coordinate')
        axim.set_xlabel('x coordinate')

        axlg = self._fig.add_axes([0.4, 0.55, 0.1, 0.3])
        axlg.axis('off')
        for ix, name in enumerate(('Ocean', 'Mountain', 'Jungle',
                                   'Savannah', 'Desert')):
            axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                         edgecolor='none',
                                         facecolor=rgb_value[name[0]]))
            axlg.text(0.35, ix * 0.21, name,
                      transform=axlg.transAxes,
                      fontsize=8)

    def update_line_graph(self):
        """
        Updates line graph for both species.
        """
        # for herbivores
        ydata_herb = self._line_graph_line_herb.get_ydata()
        ydata_herb[self.num_years_simulated] = self.num_animals_per_species[
            "Herbivore"]
        self._line_graph_line_herb.set_ydata(ydata_herb)

        # for carnivores
        ydata_carn = self._line_graph_line_carn.get_ydata()
        ydata_carn[self.num_years_simulated] = self.num_animals_per_species[
            "Carnivore"]
        self._line_graph_line_carn.set_ydata(ydata_carn)

        # rescales y axis
        if self.ymax:
            self._line_graph_ax.set_ylim(0, self.ymax)
        else:
            self._line_graph_ax.set_ylim(0, self.num_animals * 1.3)

    def create_array_herbs(self):
        """
        Creates array used to create heat map of herbivore population. Each
        cell in the array represents a cell on the island map and contains
        number of herbivores at that location.
        """
        df = self.animal_distribution
        num_rows = df["Row"].iloc[-1] + 1
        num_cols = df["Col"].iloc[-1] + 1

        index = 0
        array_herbs = numpy.zeros(shape=(num_rows, num_cols))
        for row in range(num_rows):
            for col in range(num_cols):
                array_herbs[row, col] = df["Herbivore"].iloc[index]
                index += 1
        return array_herbs

    def update_heat_map_herbs(self):
        """
        Updates visualization of heat map for herbivores.
        """
        if self._img_herb_axis is not None:
            self._img_herb_axis.set_data(self.create_array_herbs())
        else:
            self._img_herb_axis = self._heat_map_herb_ax.imshow(
                self.create_array_herbs(),
                interpolation='nearest',
                vmin=0,
                vmax=self.cmax["Herbivore"]
            )
            plt.colorbar(self._img_herb_axis, ax=self._heat_map_herb_ax,
                         orientation='vertical'
                         )

    def create_array_carns(self):
        """
        Creates array used to create heat map of carnivore population. Each
        cell in the array represents a cell on the island map and contains
        number of carnivores at that location.
        """
        df = self.animal_distribution
        num_rows = df["Row"].iloc[-1] + 1
        num_cols = df["Col"].iloc[-1] + 1

        index = 0
        array_carns = numpy.zeros(shape=(num_rows, num_cols))
        for row in range(num_rows):
            for col in range(num_cols):
                array_carns[row, col] = df["Carnivore"].iloc[index]
                index += 1
        return array_carns

    def update_heat_map_carns(self):
        """
        Updates visualization of heat map for carnivores.
        """
        if self._img_carn_axis is not None:
            self._img_carn_axis.set_data(self.create_array_carns())
        else:
            self._img_carn_axis = self._heat_map_carn_ax.imshow(
                self.create_array_carns(),
                interpolation='nearest',
                vmin=0,
                vmax=self.cmax["Carnivore"]
            )
            plt.colorbar(self._img_carn_axis, ax=self._heat_map_carn_ax,
                         orientation='vertical')

    def update_graphics(self):
        """
        Updates all graphics with current data and title.
        """
        self.update_line_graph()
        self.update_heat_map_herbs()
        self.update_heat_map_carns()
        plt.suptitle(f"Simulation of year {self.year}", fontsize=26)
        plt.pause(1e-6)

    def save_graphics(self):
        """
        Saves graphics to file, if file name is given.

        The image is stored as img_base + img_no + img_fmt
        """
        if self.img_base is None:
            return

        plt.savefig(f"{self.img_base}_{self.img_no:05d}.{self.img_fmt}")

        self.img_no += 1

    def make_movie(self, movie_fmt=_DEFAULT_MOVIE_FORMAT):
        """
        Creates MPEG4 movie from visualization images saved.

        :param movie_fmt: str
            format for movie (default='mp4')

        :note: Requires ffmpeg to work. Update ffmpeg binary at top of this
            file.

        The movie is stored as img_base + movie_fmt.

        :raise RuntimeError: if img_base not defined or ffmpeg fails
        :raise ValueError: if movie format is unknown
        """

        if self.img_base is None:
            raise RuntimeError("No filename defined.")

        if movie_fmt == 'mp4':
            try:
                subprocess.check_call([FFMPEG_BINARY,
                                       '-i',
                                       '{}_%05d.png'.format(self.img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self.img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('ERROR: ffmpeg failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format: ' + movie_fmt)


if __name__ == '__main__':
    isl_geogr = """\
                   OOOOOOOOOOOOOOOOOOOOOO
                   OJJJJJJJJJJOOOOOOOOOOO
                   OOOSSSSSSJJJJJJJJJJJJO
                   OOSSSSJJJJJJJJJJJJJJOO
                   OOSSSSSSSSSSJJJJJJJOOO
                   OSSSSSJJJJJJJJJJJJJOOO
                   OSSSSSJJJDDDDJSSJJJOOO
                   OSSJJJJJDDDJJJSSSSSOOO
                   OOSSSSJJJDDJJJSSSOOOOO
                   OSSSJJJJJDDJJJJJJJSSOO
                   OSSSSJJJJMMMJJJOOSSSOO
                   OOSSSSJJJMMMMMSOOOSSOO
                   OOOSSSSJJJJMMMMOOOOOOO
                   OOOOOOOOOOOOOOOOOOOOOO"""
    ini_pop = Population(n_herbivores=30,
                         coord_herb=[(1, 10), (7, 5), (10, 13)]
                         )
    app_pop = Population(n_carnivores=20,
                         coord_carn=[(10, 1), (5, 7), (12, 10)])
    ini_pop = ini_pop.get_animals()
    app_pop = app_pop.get_animals()
    imgbase = '../../data/img'
    biosim = BioSim(isl_geogr, ini_pop, 1, img_base=imgbase,
                    cmax_animals={"Herbivore": 400, "Carnivore": 100})
    biosim.simulate(100, 1, 3)
    biosim.add_population(app_pop)
    biosim.simulate(100, 1, 3)
    biosim.make_movie()
