#BIOSIM G20
##Exam Project in INF200 January 2020
###Authors: Ida Lunde Naalsund & Kjersti Rustad Kvisberg

### Description
***Background***

This package contains a modelling of the ecosystem of Rossumøya. The project
has been created upon request from The Environmental Protection Agency of 
Pylandia.
The ecosystem of Rossumøya includes the landscape types jungle, savannah, 
desert, mountain and ocean, and the two different animal species herbivore and 
carnivore.
Our quest has been to find out whether both species can survive in the long
term. 

### Contents
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

 

### Usage
```python
import biosim
```

To create an instance of the Herbivore class:
```python
animals.Herbivore(
{"species": "Herbivore", "age": 5, "weight": 20}
)
```
Similar for the Carnivore class. Each animal on the island is an instance of
one of these classes.

To create an instance of the Jungle class:
```python
landscape.Jungle(initial_population=[
    {"species": "Herbivore", "age": 1, "weight": 5.0},
    {"species": "Carnivore", "age": 5, "weight": 6.0}
]
)
```
Simular for all other landscape types. Each location on the map of Rossumøya 
is an instance of a landscape class.

Here we assign a small population to the location (1, 3) on the map.
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

To create an instance of the BioSim class:
```python
simulation.BioSim(island_geography, initial_population)
```
The BioSim class contains methods to run the simulation of the ecosystem.
The output from the simulation is a visualization of the development of
the ecosystem of the island, and shows how the number of each species and
their distribution throughout the island changes over time.

### Badges
All tests pass.
