import nOmicron.mate.objects as mo
import numpy as np
from nOmicron.microscope import IO


def get_continuous_signal(channel_name, sample_points=50, sample_time=1):
    """Acquire a continuous signal."""
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


def get_spectra(channel_name, target_position, start_end=(0, 1), sample_points=50, sample_time=1e-3,
                repeats=1, forward_back=True):
    """
    Go to a position and perform spectroscopy.

    Parameters
    ----------
    channel_name : str
    target_position : list
        [x, y] in range -1,1
    start_end : tuple
    sample_points : int
    sample_time : float
    repeats : int
    forward_back : bool
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

    return x_data, y_data

if __name__ == '__main__':
    IO.connect()
    t, I = get_continuous_signal("I_t")

    # Do a fixed point spec
    v, I = get_spectra("I_V", [0, 0], repeats=3, sample_time=10e-3, forward_back=True)