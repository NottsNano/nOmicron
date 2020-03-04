# Oliver Gordon, 2019
from itertools import product
from time import sleep

import numpy as np

import nOmicron.mate.objects as mo
from nOmicron.microscope import IO
from tqdm import tqdm


def get_continuous_signal(channel_names, sample_time, sample_points):
    """Acquire a continuous signal.

    Parameters
    -----------
    channel_names : str or list of str
        The continuous channel to view, e.g. I(t), Z(t), Df(t), Aux1(t)
    sample_time : float
        The time to acquire in seconds
    sample_points : int
        The number of points to acquire

    Returns
    -------
    x_data : Numpy array
    y_data : Numpy array

    Examples
    --------
    Acquire 60 points of I(t) data over 0.1 seconds
    >>> from nOmicron.microscope import IO
    >>> from nOmicron.utils.plotting import plot_linear_signal
    >>> IO.connect()
    >>> t, I = get_continuous_signal("I(t)", 1e-1, 60)
    >>> plot_linear_signal(v, I, "I(V)")
    >>> IO.disconnect()

    Acquire 100 points of Z(t) data over 5 seconds
    >>> from nOmicron.microscope import IO
    >>> from nOmicron.utils.plotting import plot_linear_signal
    >>> IO.connect()
    >>> t, I = get_continuous_signal("Z(t)", 5, 100)
    >>> plot_linear_signal(v, I, "I(V)")
    >>> IO.disconnect()

    Acquire both channels simultaneously
        >>> from nOmicron.microscope import IO
    >>> from nOmicron.utils.plotting import plot_linear_signal
    >>> IO.connect()
    >>> t, sigs = get_continuous_signal(["Z(t)", "I(t)"], 5, 100)
    >>> plot_linear_signal(v, sigs("I(t)"), "I(V)")
    >>> IO.disconnect()
    """

    global view_count, x_data, y_data
    x_data = None
    y_data = {}
    view_count = 0

    def view_continuous_callback():
        global view_count, x_data, y_data
        view_count += 1
        pbar.update(len(channel_names))
        data_size = mo.view.Data_Size()
        period = mo.clock.Period()
        x_data = np.linspace(0, (data_size - 1) * period, data_size)
        y_data[channel_names[view_count-1]] = np.array(mo.sample_data(data_size))

    if type(channel_names) is str:
        channel_names = [channel_names]

    for channel_name in channel_names:
        IO.enable_channel(channel_name)
        IO.set_clock(sample_time, sample_points)
        mo.allocate_sample_memory(sample_points)
        mo.view.Data(view_continuous_callback)

    pbar = tqdm(total=len(channel_names))
    while view_count < len(channel_names) and mo.mate.rc == mo.mate.rcs['RMT_SUCCESS']:
        mo.wait_for_event()

    for channel_name in channel_names:
        IO.disable_channel(channel_name)

    if len(y_data) == 1:
        y_data = np.array(list(y_data.values())).reshape((sample_points,))

    return x_data, y_data


def get_point_spectra(channel_name, start_end, sample_time, sample_points, target_position=None, grid_pts=None,
                      repeats=1, forward_back=True, return_filename=False):
    """
    Go to a position and perform fixed point spectroscopy.

    Parameters
    ----------
    channel_name : str
        The channel to acquire from, e.g. I(V), Z(V), Aux2(V)
    target_position : list or None
        [x, y] in the range -1,1. Can be converted from real nm units with utils.convert...
        Must be None if grid is enabled
    grid_pts : int or tuple of int
        The number of points to do grid spectroscopy on. Default None (i.e. off).
    start_end : tuple
        Start and end I/Z/Aux2
    sample_time : float
        The time to acquire in seconds
    sample_points : int
        The number of points to acquire
    repeats : int
        The number of repeat spectra to take for each point
    forward_back : bool
        Scan in both directions, or just one.
    return_filename : bool, optional
        If the full file name of the scan should be returned along with the data. Default is False

    Returns
    -------
    x_data : Numpy array
    y_data :
        If performing repeat spectra and:
            Scanning in both directions: list of list of Numpy arrays, where inner list is [0] forwards, [1] backwards
            Scanning in one direction: list of Numpy arrays
        If no repeat spectra and:
            Scanning in both directions: list of Numpy arrays, where list is [0] forwards, [1] backwards
            Scanning in one direction: single Numpy array

    Examples
    --------
    Acquire 60 points of I(V) data over 10 milliseconds, with tip placed in middle of scan window.
    >>> from nOmicron.microscope import IO
    >>> from nOmicron.utils.plotting import plot_linear_signal
    >>> IO.connect()
    >>> v, I = get_point_spectra("I(V)", start_end=[0, 1], target_position=[0, 0], ...
    >>>                   repeats=3, sample_points=50, sample_time=10e-3, forward_back=True)
    >>> plot_linear_signal(v, I, "I(V)")
    >>> IO.disconnect()
    """
    global view_count, grid_count, view_name, x_data, y_data

    modes = {"V": 0, "Z": 1, "Varied Z": 2}  # Varied Z not fully supported yet!
    view_count = 0
    grid_count = -1
    x_data = None
    y_data = []
    [y_data.append([None] * (bool(forward_back) + 1)) for i in range(repeats)]  # Can't use [] ** repeats
    return y_data

    def view_spectroscopy_callback():
        global view_count, grid_count, view_name, x_data, y_data
        pbar.update(1)
        view_count += 1
        grid_count += 1
        view_name = [mo.view.Run_Count(), mo.view.Cycle_Count()]
        cycle_count = mo.view.Cycle_Count() - 1
        packet_count = mo.view.Packet_Count() - 1
        data_size = mo.view.Data_Size()
        x_data = np.linspace(start_end[0], start_end[1], data_size)
        y_data[grid_count][cycle_count][packet_count] = np.array(mo.sample_data(data_size)) * 1e-9
        if packet_count == 1:
            y_data[grid_count][cycle_count][packet_count] = np.flip(y_data[cycle_count][packet_count])

    # Determine parameters for grid/non-grid spec
    if type(grid_pts) is int:
        grid_pts = [grid_pts, grid_pts]
    max_count = (repeats * (forward_back + 1))

    if grid_pts is not None:
        xpts = np.linspace(-1, 1, grid_pts[0])
        ypts = np.linspace(-1, 1, grid_pts[1])
        target_positions = product(xpts, ypts)
        tot_count = max_count * grid_pts[0] * grid_pts[1]
    else:
        target_positions = [target_position]
        tot_count = max_count

    # Set all the parameters
    mo.spectroscopy.Spectroscopy_Mode(modes[channel_name[-2]])
    getattr(mo.spectroscopy, f"Device_{modes[channel_name[-2]] + 1}_Points")(sample_points)
    getattr(mo.spectroscopy, f"Raster_Time_{modes[channel_name[-2]] + 1}")(sample_time)
    getattr(mo.spectroscopy, f"Device_{modes[channel_name[-2]] + 1}_Start")(start_end[0])
    getattr(mo.spectroscopy, f"Device_{modes[channel_name[-2]] + 1}_End")(start_end[1])
    getattr(mo.spectroscopy, f"Device_{modes[channel_name[-2]] + 1}_Repetitions")(repeats)
    getattr(mo.spectroscopy, f"Enable_Device_{modes[channel_name[-2]] + 1}_Ramp_Reversal")(forward_back)

    # Set up spec
    mo.xy_scanner.Store_Current_Position(True)

    pbar = tqdm(total=tot_count)
    IO.enable_channel(channel_name)
    mo.xy_scanner.Trigger_Execute_At_Target_Position(True)
    for target_position in target_positions:
        mo.xy_scanner.Target_Position(list(target_position))

        # Do it
        mo.xy_scanner.move()
        mo.allocate_sample_memory(sample_points)
        mo.view.Data(view_spectroscopy_callback)

        while view_count < max_count and mo.mate.rc == mo.mate.rcs['RMT_SUCCESS']:
            mo.wait_for_event()
        mo.view.Data()

    mo.xy_scanner.Trigger_Execute_At_Target_Position(False)
    IO.disable_channel()

    # Return to normal
    mo.xy_scanner.Return_To_Stored_Position(True)
    mo.xy_scanner.Store_Current_Position(False)

    # if not forward_back:
    #     y_data = [item[0] for item in y_data]
    # if repeats == 1:
    #     y_data = y_data[0]

    if return_filename:
        filename = f"{mo.experiment.Result_File_Path()}\\{mo.experiment.Result_File_Name()}--{view_count[0]}_{view_count[1]}.{channel_name}_mtrx"
        return x_data, y_data, filename
    else:
        return x_data, y_data


if __name__ == '__main__':
    from nOmicron.utils.plotting import plot_linear_signal

    IO.connect()
    t, I1 = get_continuous_signal("I(t)", sample_time=2, sample_points=50)

    # Do a fixed point spec
    # v, I2 = get_point_spectra("I(V)", start_end=(0.5, -0.5), target_position=[0, 0.5],
    #                           repeats=4, sample_points=100, sample_time=20e-3, forward_back=True)
    # plot_linear_signal(v, I2, "I(V)")
    # IO.disconnect()
