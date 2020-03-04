# Oliver Gordon, 2019

import nOmicron.mate.objects as mo
from nOmicron.utils import utils
import re

def connect():
    """Connect to the Matrix. Matrix must be open and initalised."""

    print("Connecting to the Matrix...")
    mo.mate.testmode = False
    mo.mate.connect()
    utils.is_online()
    print("Connected Successfully!")


def disconnect():
    """Disconnect from the Matrix."""
    print("Disconnecting...")
    mo.experiment.stop()
    mo.mate.disconnect()
    print("Disconnected Successfully!")


def enable_channel(channel_name):
    """Enables a channel (e.g. Z_Fw, I_Bw, I_t, Aux1_t, I_V, I_Z) for measurement.
    Examples
    --------
    >>> from nOmicron.microscope import IO
    >>> IO.connect()
    >>> IO.enable_channel("I_t")
    """

    channel_name = channel_name.replace("(", "_").replace(")","")
    if channel_name[-1] == "w":
        utils.is_channel_real(channel_name[:-3])
    else:
        utils.is_channel_real(channel_name)

    if len(channel_name) != 1 and channel_name[-1] != "t" and channel_name[-1] != "w":
        channel_name += "_Spec"

    mo.channel_name = channel_name
    if channel_name[-1] == "t":
        mo.get_clock_name(mo.channel_name)

    mo.view.Deliver_Data(True)


def disable_channel(channel_name=None):
    """Disables a channel from passing data."""
    if channel_name:
        channel_name = channel_name.replace("(", "_").replace(")", "")
        if channel_name[-1] == "t":
            mo.channel_name = channel_name.replace("(", "_").replace(")","")
            mo.get_clock_name(mo.channel_name)
            mo.clock.Enable(False)
    elif mo.channel_name == '':
        raise IOError("No channel to disable")

    mo.view.Deliver_Data(False)
    mo.channel_name = ''


def set_clock(sample_time, sample_points):
    """Sets up the clock.

    Parameters
    ----------
    sample_time : float
    sample_points : int

    Warnings
    --------
    Only enable this with data channels with a Clock (i.e. only continuous channels like I_t, df_t)

    Examples
    --------
    >>> from nOmicron.microscope import IO
    >>> IO.connect()
    >>> IO.enable_channel("Z_t")
    >>> IO.set_clock(1e-2, 200)  # 100 milliseconds, 200 points will be acquired on next trigger
    """
    if "Clock" not in mo.mate.deployment_parameter(mo.mate.scope, mo.channel_name, 'Trigger'):
        raise IOError("Attempted to set a clock for a non-clock object")

    mo.clock.Enable(False)
    mo.clock.Period(sample_time / sample_points)
    mo.clock.Samples(sample_points)
    mo.clock.Enable(True)


def intercept_target_position():
    """Intercepts the tip target position set with the mouse tool

    Returns
    -------
    target_pos : tuple

    Warnings
    --------
    If using this function to call a routine e.g. continuous_spectra.get_point_spectra(), do NOT execute a spectroscopy
    in Matrix to exectute this function - this will very often result in one data packet being missed. Instead, perform
    a non-trigger task, such as a tip relocation.

    Examples
    --------
    Intercept the xy position of a manual spectroscopy, and allow the data to be passed into python
    >>> from nOmicron.microscope.continuous_spectroscopy import get_point_spectra
    >>> pos = intercept_target_position()
    >>> v, I = get_point_spectra("I(V)", start_end=(0.5, -0.5), target_position=pos,
    >>>                   repeats=1, sample_points=100, sample_time=20e-3, forward_back=False)
    """
    current_pos = old_pos = mo.xy_scanner.Target_Position()
    while old_pos == current_pos:
        current_pos = mo.xy_scanner.Target_Position()

    return current_pos


def enable_pll():
    mo.pll.PLL_Enable(True)


def disable_pll():
    mo.pll.PLL_Enable(False)
