# Oliver Gordon, 2019

import inspect
import json
import sys
import warnings

from nOmicron.mate import objects as mo
from bs4 import BeautifulSoup


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
        raise LookupError(f"'{channel_name}' does not exist/is not enabled. Allowed channels: {get_allowed_channels()}")

    return not response


def is_data_size_set():
    response = mo.view.Data_Size() is int
    if not response:
        warnings.warn("Data size has not been set/acknowledged by Matrix. No data will be sent!")

    return response


def is_parameter_within_allowed_range(parameter_name, parameter_value, config_file="control_limits.json"):
    # TODO: Include the minmax thing, and update the json file to match!
    data = json.loads(open(config_file).read())
    response = data[parameter_name][0] <= parameter_value <= data[parameter_name][1]

    if not response:
        raise ValueError(
            f"{parameter_name} is not allowed (requested {parameter_value}, should be within {data[parameter_name]})")

    return response


def _force_set_scope(scope_name):
    """Forcibly sets the experiment scope e.g. STM_Basic"""
    mo.mate.scope = scope_name
    mo.mate.lib_mate.setScopeName(scope_name)


def _friendly_name_to_mate(module_name):
    """Slightly hacky code to convert friendly mo.objects names to the mate4dummies mo.mate format"""
    all_modules = {"channel": "_Channel",
                   "clock": "_Clock",
                   "experiment": "_Experiment",
                   "gap_voltage_control": "_GapVoltageControl",
                   "pll": "_PLLControl",
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


def is_parameter_allowable(value, experiment_element, parameter, test=0):
    """
    Checks if a parameter is allowable within the reported operating range of the equipment.

    Using this before sending an out of range prevents possible locking up/hard crashes of Matrix.

    Attributes
    ----------
    experiment_element : str
        The experiment element that the desired parameter falls under
    parameter : str
        The parameter to be tested
    value :
        The value of the parameter

    Returns
    -------
    response : bool

    Examples
    --------
    >>> is_parameter_allowable(100, "xy_scanner", "Points")

    """
    if value is None:
        return True
    else:
        min_max = read_min_max(experiment_element, parameter, test)
        if min_max:
            response = min_max[0] <= value <= min_max[1]
            if not response:
                warnings.warn(
                    f"{parameter} ({value}) should be within range {min_max[0]} <= {parameter} <= {min_max[1]}. Matrix may die")
        else:
            response = None
    return response


def read_min_max(experiment_element, parameter, test=0):
    """
    Reads the minimum and maximum allowed values for settable parameters.

    Attributes
    ----------
    experiment_element : str
        The experiment element that the desired parameter falls under
    parameter : str
        The parameter to be tested

    Returns
    -------
    outs : tuple
        A tuple in the form [min, max]

    Examples
    --------
    >>> read_min_max("xy_scanner", "Points")
    """

    p = 'function'
    experiment_element = _friendly_name_to_mate(experiment_element)
    members = inspect.getmembers(sys.modules['nOmicron.mate.objects'], inspect.isclass)
    inspected = [item[1] for item in members if item[0] == experiment_element][0]

    def get_value(min_max):
        if experiment_element == "_Clock":
            out = mo._process(p, [inspected(1.0), min_max], parameter, test)
        else:
            out = mo._process(p, [inspected(), min_max], parameter, test)
        if type(out) is tuple:
            out = out[0]
        return out

    outs = [get_value("min"), get_value("max")]
    return outs


def restore_z_functionality():
    mo.xy_scanner.X_Trace_Trigger(False)
    mo.xy_scanner.X_Retrace_Trigger(False)
    mo.xy_scanner.Y_Retrace_Trigger(False)
    mo.experiment.stop()
    

def get_allowed_channels():
    experiment_name = mo.mate.scope
    install_path = mo.mate.installation_directory
    experiment_path = f"{install_path}\Templates\default\Experiments\{experiment_name}.expd"

    experiment_file = open(experiment_path, "r").read()
    soup = BeautifulSoup(experiment_file, "xml")

    raw_entries = soup.findAll(panelType="ChannelControl")
    allowed_channels = [line.attrs["experimentElementInstanceName"] for line in raw_entries]

    return allowed_channels
