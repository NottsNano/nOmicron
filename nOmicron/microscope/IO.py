import warnings
import numpy as np

from nOmicron.utils import utils
import nOmicron.mate.objects as mo


def connect():
    mo.mate.testmode = False
    mo.mate.connect()
    utils.is_online()


def enable_channel(channel_name):
    utils.is_channel_real(channel_name)

    if len(channel_name) != 1 and channel_name[-1] != "t":
        channel_name += "_Spec"
    mo.channel_name = channel_name

    if channel_name[-1] == "t":
        mo.get_clock_name(mo.channel_name)

    mo.view.Deliver_Data(True)


def disable_channel():
    if mo.channel_name == '':
        raise IOError("No channel to disable")

    mo.view.Deliver_Data(False)
    mo.channel_name = ''


def set_clock(sample_time, sample_points):
    if "Clock" not in mo.mate.deployment_parameter(mo.mate.scope, mo.channel_name, 'Trigger'):
        raise IOError("Attempted to set a clock for a non-clock object")

    mo.clock.Enable(False)
    mo.clock.Period(sample_time / sample_points)
    mo.clock.Samples(sample_points)
    mo.clock.Enable(True)
