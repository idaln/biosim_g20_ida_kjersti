# -*- coding: utf-8 -*-

"""
"""
from biosim.animals import Animal, Herbivore, Carnivore
from biosim.landscape import Landscape, Jungle, Savannah, Desert, Mountain, \
    Ocean
from biosim.island_map import IslandMap
import pandas
import numpy
import matplotlib.pyplot as plt

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
        numpy.random.seed(seed)

        self.cmax = cmax_animals
        self.img_base = img_base
        self.img_fmt = img_fmt
        if ymax_animals is None:
            self.ymax = 1500
        else:
            self.ymax = ymax_animals

        self.island_map = IslandMap(island_map, ini_pop)
        self.island_map.create_map_dict()
        self.num_years_simulated = 0
        self._final_year = None

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

        self._final_year = self.year + num_years
        self.setup_graphics()

        while self.year < self._final_year:

            if self.year % vis_years == 0:
                self.update_graphics()

            if self.year % img_years == 0:
                self.save_graphics()

            self.island_map.run_all_seasons()
            self.num_years_simulated += 1

    def create_map_graphics(self):


        #                   R    G    B
        rgb_value = {'O': (0.0, 0.0, 1.0),  # blue
                     'M': (0.5, 0.5, 0.5),  # grey
                     'J': (0.0, 0.6, 0.0),  # dark green
                     'S': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        geogr_rgb = [[rgb_value[column] for column in row]
                     for row in self.island_map.geogr.splitlines()]

        axim = self._map_ax

        #axim = fig.add_axes([0.1, 0.1, 0.7, 0.8])  # llx, lly, w, h
        axim.imshow(geogr_rgb)
        axim.set_xticks(range(len(geogr_rgb[0])))
        axim.set_xticklabels(range(1, 1 + len(geogr_rgb[0])))
        axim.set_yticks(range(len(geogr_rgb)))
        axim.set_yticklabels(range(1, 1 + len(geogr_rgb)))

        #axlg = fig.add_axes([0.85, 0.1, 0.1, 0.8])  # llx, lly, w, h
        #axlg.axis('off')
        #for ix, name in enumerate(('Ocean', 'Mountain', 'Jungle',
        #                           'Savannah', 'Desert')):
        #    axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
        #                                 edgecolor='none',
        #                                 facecolor=rgb_value[name[0]]))
        #    axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

    def setup_graphics(self):
        """
        Creates subplots.
        :param num_years: number of years to simulate
        """
        # Create new figure window
        if self._fig is None:
            self._fig = plt.figure()

        # Add left subplot for images created with imshow().
        # We cannot create the actual ImageAxis object before we know
        # the size of the image, so we delay its creation.
        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(2, 2, 1)
            self.create_map_graphics()

        self._map_ax.title.set_text('Island')

        # Add right subplot for line graph of herbivore and carnivore
        # populations.
        if self._line_graph_ax is None:
            self._line_graph_ax = self._fig.add_subplot(2, 2, 2)
            self._line_graph_ax.set_ylim(0, self.ymax)

        # Needs updating on subsequent calls to simulate()
        self._line_graph_ax.set_xlim(0, self._final_year + 1)

        # Line for herbivores
        if self._line_graph_line_herb is None:
            line_graph_plot_herb = self._line_graph_ax.plot(
                numpy.arange(0, self._final_year),
                numpy.full(self._final_year, numpy.nan)
            )
            self._line_graph_line_herb = line_graph_plot_herb[0]
        else:
            xdata, ydata = self._line_graph_line_herb.get_data()
            xnew = numpy.arange(xdata[-1] + 1, self._final_year)
            if len(xnew) > 0:
                ynew = numpy.full(xnew.shape, numpy.nan)
                self._line_graph_line_herb.set_data(
                    numpy.hstack((xdata, xnew)), numpy.hstack((ydata, ynew))
                )

        # Line for carnivores
        if self._line_graph_line_carn is None:
            line_graph_plot_carn = self._line_graph_ax.plot(
                numpy.arange(0, self._final_year),
                numpy.full(self._final_year, numpy.nan)
            )
            self._line_graph_line_carn = line_graph_plot_carn[0]
        else:
            xdata, ydata = self._line_graph_line_carn.get_data()
            xnew = numpy.arange(xdata[-1] + 1, self._final_year)
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

        # Heat map for herbivores
        if self._heat_map_herb_ax is None:
            self._heat_map_herb_ax = self._fig.add_subplot(2, 2, 3)
            self._img_herb_axis = None

        # Heat map for carnivores
        if self._heat_map_carn_ax is None:
            self._heat_map_carn_ax = self._fig.add_subplot(2, 2, 4)
            self._img_carn_axis = None

    def update_graphics(self):
        """
        Updates all graphics with current data.
        """
        self.update_line_graph()
        self.update_heat_maps()
        plt.pause(1e-6)

    def update_line_graph(self):
        """
        Updates line graph. Line graph has one line for each species.
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

    def update_heat_maps(self):
        """
        Update visualization of heat maps for both species.
        """
        pass

    def save_graphics(self):
        """
        Saves graphics to file, if file name is given.
        """
        pass

    def make_movie(self):
        """
        Create MPEG4 movie from visualization images saved.
        """
        pass


if __name__ == "__main__":
    ini_pop = [
        {
            "loc": (1, 1),
            "pop": [
                {"species": "Carnivore", "age": 5, "weight": 200}
                for _ in range(10)
            ]
        },
        {
            "loc": (1, 2),
            "pop": [
                {"species": "Herbivore", "age": 5, "weight": 20}
                for _ in range(10)
            ]
        }
    ]

    island = "OOOOO\nOJMJO\nODJJO\nODSJO\nOJMDO\nOOOOO"
    biosim = BioSim(island, ini_pop, 1)
    #print(biosim.animal_distribution)
    #biosim.simulate(15)
    #print(biosim.animal_distribution)
    biosim.simulate(5, 1, 5)
    plt.show()








