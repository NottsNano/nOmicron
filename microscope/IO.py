import mate.objects as mo
from utils import utils
from wrapt_timeout_decorator import *

@timeout(10, exception_message="Timed out while trying to connect. Try restarting Matrix/CU")
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


def disable_channel():
    """Disables a channel from passing data."""
    if mo.channel_name == '':
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
