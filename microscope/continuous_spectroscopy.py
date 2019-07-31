import numpy as np

import mate.objects as mo
from microscope import IO


def get_continuous_signal(channel_name, sample_time, sample_points):
    """Acquire a continuous signal.

    Parameters
    -----------
    channel_name : str
        The continuous channel to view, e.g. I_t, Z_t, Df_t, Aux1_t
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
    >>> IO.connect()
    >>> t, I = get_continuous_signal("I_t", 1e-1, 60)
    >>> IO.disconnect()

    Acquire 100 points of Z(t) data over 5 seconds
    >>> from nOmicron.microscope import IO
    >>> IO.connect()
    >>> t, I = get_continuous_signal("Z_t", 5, 100)
    >>> IO.disconnect()
    """

    global view_count, x_data, y_data
    x_data = y_data = None
    view_count = 0

    def view_continuous_callback():
        global view_count, x_data, y_data
        view_count += 1

        data_size = mo.view.Data_Size()
        period = mo.clock.Period()
        x_data = np.linspace(0, (data_size - 1) * period, data_size)
        y_data = np.array(mo.sample_data(data_size))

    IO.enable_channel(channel_name)
    IO.set_clock(sample_time, sample_points)

    mo.view.Data(view_continuous_callback)
    mo.allocate_sample_memory(sample_points)

    while view_count < 1 and mo.mate.rc == mo.mate.rcs['RMT_SUCCESS']:
        mo.wait_for_event()
    mo.clock.Enable(False)
    mo.view.Data()

    IO.disable_channel()

    return x_data, y_data


def get_point_spectra(channel_name, target_position, start_end, sample_time, sample_points,
                      repeats=1, forward_back=True):
    """
    Go to a position and perform fixed point spectroscopy.

    Parameters
    ----------
    channel_name : str
        The channel to acquire from, e.g. I_V, Z_V, Aux2_V
    target_position : list
        [x, y] in the range -1,1
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
    >>> IO.connect()
    >>> v, I = get_point_spectra("I_V", start_end=[0, 1], target_position=[0, 0], ...
    >>>                   repeats=3, sample_points=50, sample_time=10e-3, forward_back=True)
    >>> IO.disconnect()
    """

    global view_count, x_data, y_data
    modes = {"V": 0, "Z": 1, "Varied Z": 2}  # Varied Z not fully supported yet!
    max_count = (repeats * (forward_back + 1))
    view_count = 0
    x_data = None
    y_data = [[None] * (bool(forward_back) + 1)] * repeats

    def view_spectroscopy_callback():
        global view_count, x_data, y_data
        view_count += 1
        cycle_count = mo.view.Cycle_Count() - 1
        packet_count = mo.view.Packet_Count() - 1

        data_size = mo.view.Data_Size()
        x_data = np.linspace(start_end[0], start_end[1], data_size)
        y_data[cycle_count][packet_count] = np.array(mo.sample_data(data_size))

    # Set all the parameters
    IO.enable_channel(channel_name)
    mo.spectroscopy.Spectroscopy_Mode(modes[channel_name[-1]])
    getattr(mo.spectroscopy, f"Device_{modes[channel_name[-1]] + 1}_Points")(sample_points)
    getattr(mo.spectroscopy, f"Raster_Time_{modes[channel_name[-1]] + 1}")(sample_time)
    getattr(mo.spectroscopy, f"Device_{modes[channel_name[-1]] + 1}_Start")(start_end[0])
    getattr(mo.spectroscopy, f"Device_{modes[channel_name[-1]] + 1}_End")(start_end[1])
    getattr(mo.spectroscopy, f"Device_{modes[channel_name[-1]] + 1}_Repetitions")(repeats)
    getattr(mo.spectroscopy, f"Enable_Device_{modes[channel_name[-1]] + 1}_Ramp_Reversal")(forward_back)

    # Set up spec
    mo.xy_scanner.Store_Current_Position(False)
    mo.xy_scanner.Store_Current_Position(True)
    mo.xy_scanner.Target_Position(target_position)
    mo.xy_scanner.Trigger_Execute_At_Target_Position(True)

    # Do it
    mo.xy_scanner.move()
    mo.view.Data(view_spectroscopy_callback)
    mo.allocate_sample_memory(sample_points)
    while view_count < max_count and mo.mate.rc == mo.mate.rcs['RMT_SUCCESS']:
        mo.wait_for_event()
    mo.view.Data()

    # Return to normal
    mo.xy_scanner.Trigger_Execute_At_Target_Position(False)
    mo.xy_scanner.Return_To_Stored_Position(True)
    mo.xy_scanner.Store_Current_Position(False)
    IO.disable_channel()

    if not forward_back:
        y_data = [item[0] for item in y_data]
    if repeats == 1:
        y_data = y_data[0]
    return x_data, y_data


if __name__ == '__main__':
    IO.connect()
    t, I1 = get_continuous_signal("I_t", sample_time=1, sample_points=50)

    # Do a fixed point spec
    v, I2 = get_point_spectra("I_V", start_end=[0, 1], target_position=[0, 0],
                              repeats=3, sample_points=50, sample_time=10e-3, forward_back=True)
    IO.disconnect()
