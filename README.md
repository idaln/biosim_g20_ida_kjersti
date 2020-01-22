# BIOSIM G20
## Exam Project in INF200 January 2020
### Authors: Ida Lunde Naalsund & Kjersti Rustad Kvisberg

## Description
***Background***

This package contains a modelling of the ecosystem of Rossumøya. The project
has been created upon request from The Environmental Protection Agency of 
Pylandia.
The ecosystem of Rossumøya includes the landscape types jungle, savannah, 
desert, mountain and ocean, and the two different animal species herbivore and 
carnivore.
Our quest has been to find out whether both species can survive in the long
term. 

## Contents
- examples
    * check_sim.py
    * population_generator.py
- src\biosim
    * animals.py
    * island_map.py
    * landscape.py
    * simulation.py
- tests
    * test_animals.py
    * test_biosim_interface.py
    * test_island_map.py
    * test_landscape.py

## Usage
```python
import biosim
```

The BioSim class contains methods to run the simulation of the ecosystem.
To create an instance of the BioSim class:
```python
biosim = simulation.BioSim(
island_geography, initial_population, seed, img_base
)
```

This is how you run a simple simulation:
```python
biosim.simulate(num_years, vis_years, img_years)
```
The output from this method is a visualization of the development of
the ecosystem of the island. The visualization includes a line graph that 
shows how the number of animals of each species changes over time, one heat
map per species that show their distribution throughout the island over time,
and a static map over the geography of the island. 

The information about the island is saved in the IslandMap class.
To create an instance of the IslandMap class:
```python
island_map.IslandMap(
    island_geography="OOO\nOJO\nOOO", 
    initial_population=[{
        "loc": (1, 3),
        "pop": [
        {"species": "Herbivore", "age": 1, "weight": 5.0},
        {"species": "Carnivore", "age": 5, "weight": 6.0}
        ]
    }]
)
```
Here we have assigned a small population to the location (1, 3) on the map.
The island map 'keeps track' of which landscape classes belong to 
which locations.

To create an instance of the Jungle class:
```python
landscape.Jungle(initial_population=[
    {"species": "Herbivore", "age": 1, "weight": 5.0},
    {"species": "Carnivore", "age": 5, "weight": 6.0}
]
)
```
Simular for the other landscape types. 
Each location on the map of Rossumøya is an instance of a landscape class. 
The landscape classes 'keep track' of which animals live on their location.

To create an instance of the Herbivore class:
```python
animals.Herbivore(
{"species": "Herbivore", "age": 5, "weight": 20}
)
```
Similarly for the Carnivore class. Each animal on the island is an instance of
one of these classes, and they have methods for e.g. eating and procreating.

## Badges
All tests pass.
