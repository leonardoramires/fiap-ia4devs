# functions/__init__.py
from . import genetic_algorithm as ga
from . import greedy_algorithm as gra
from . import linear_programming_algorithm as lpa
from . import human_allocation as ha 

algorithms = {
    "genetic_algorithm": ga,
    "linear_programming_algorithm": lpa,
    "greedy_algorithm": gra,
    "human_allocation": ha
}