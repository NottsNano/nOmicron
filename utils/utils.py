import inspect
import json
import sys
import warnings
import inspect
import sys
import warnings

import mate.objects as mo


def is_online():
    """Tests if matrix is connected and running."""
    if not mo.mate.online or mo.experiment.Result_File_Name() == 'void':
        raise ConnectionError("Matrix is not running and initialised!")
    return mo.mate.online


def is_channel_real(channel_name):
    """Tests if chosen channel exists and is enabled.

    Parameters
    ----------
    channel_name : str
        The name of the channel
    """

    is_online()
    response = mo.mate.deployment_parameter(mo.mate.scope, channel_name, 'Trigger') == ''
    if response:
        raise LookupError(f"Requested channel '{channel_name}' does not exist/is not enabled in Matrix")

    return not response


def is_data_size_set():
    response = mo.view.Data_Size() is int
    if not response:
        raise ValueError("Data size has not been set/acknowledged by Matrix (?)")

    return response


def is_parameter_within_allowed_range(parameter_name, parameter_value, config_file="control_limits.json"):
    # TODO: Include the minmax thing, and update the json file to match!
    data = json.loads(open(config_file).read())
    response = data[parameter_name][0] <= parameter_value <= data[parameter_name][1]

    if not response:
        raise ValueError(
            f"{parameter_name} is not allowed (requested {parameter_value}, should be within {data[parameter_name]})")

    return response


def _friendly_name_to_mate(module_name):
    all_modules = {"channel": "_Channel",
                   "clock": "_Clock",
                   "experiment": "_Experiment",
                   "gap_voltage_control": "_GapVoltageControl",
                   "piezo_control": "_PiezoControl",
                   "regulator": "_Regulator",
                   "view": "_View",
                   "xy_scanner": "_XYScanner",
                   "spectroscopy": "_Spectroscopy"}

    if module_name in all_modules.keys():
        mate_name = all_modules[module_name]
    elif module_name in all_modules.values():
        mate_name = module_name
    else:
        raise ValueError(f"Requested module {module_name} must be one of {all_modules.keys()}")

    return mate_name


def is_parameter_allowable(a, module, parameter, test=0):
    min_max = mo.read_min_max(module, parameter, test)

    if a is not None:
        response = min_max[0] <= a <= min_max[1]
        if not response:
            warnings.warn(f"{parameter} should be within range {min_max[0]} <= {parameter} <= {min_max[1]}. Matrix may die")
    else:
        response = None
    return response


