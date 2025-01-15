# functions/__init__.py
from . import genetic_algorithm as ga
from . import greedy_algorithm as gra
from . import linear_programming_algorithm as lpa

algorithms = {
    "genetic_algorithm": ga,
    "linear_programming_algorithm": lpa,
    "greedy_algorithm": gra,
}