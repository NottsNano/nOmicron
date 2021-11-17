# Oliver Gordon, 2019

from time import sleep

import numpy as np

from nOmicron.mate import objects as mo


def retract_and_move() -> None:
    """Retract the tip, move a few coarse steps in a random direction, and reapproach"""
    from nOmicron.microscope import black_box

    mo.experiment.stop()
    black_box.backward()
    rand_dir = np.random.rand()
    rand_steps = np.random.randint(low=5, high=10)
    if rand_dir < 0.25:
        black_box.x_minus(rand_steps)
    elif rand_dir < 0.5:
        black_box.x_plus(rand_steps)
    elif rand_dir < 0.75:
        black_box.y_plus(rand_steps)
    else:
        black_box.y_minus(rand_steps)
    sleep(0.1)
    black_box.auto_approach()
    mo.experiment.start()


# TODO get upper/lower values from .expd file containing calib.
# TODO user parameter for allowing selection between green/yellow/red
def is_z_range_valid(min_max=(-650e-9, 650e-9)) -> bool:
    """Test if tip is regulating in the red/yellow/green part of the z regulation window"""
    return min_max[0] <= mo.regulator.Z_Out() <= min_max[1]
