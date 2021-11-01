# Oliver Gordon, 2019

from nOmicron.mate import objects as mo

# TODO get upper/lower values from .expd file containing calib.
# TODO user parameter for allowing selection between green/yellow/red


def is_z_range_valid():
    min_max = [-500e-9, 500e-9]
    return min_max[0] <= mo.regulator.Z_Out() <= min_max[1]