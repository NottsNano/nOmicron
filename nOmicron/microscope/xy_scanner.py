# Oliver Gordon, 2019

import warnings

import numpy as np
from tqdm import tqdm

import nOmicron.mate.objects as mo
from nOmicron.microscope import IO
from nOmicron.utils.plotting import plot_xy


def set_gap_voltage(voltage):
    mo.gap_voltage_control.Voltage(voltage)


def set_scan_position(xy_pos=None, width_height=None, angle=None):
    if width_height[0] != width_height[1]:
        mo.xy_scanner.Width_Height_Constrained(False)

    if width_height is not None:
        mo.xy_scanner.Width(width_height[0])
        mo.xy_scanner.Height(width_height[1])

    if xy_pos is not None:
        mo.xy_scanner.X_Offset(xy_pos[0])
        mo.xy_scanner.Y_Offset(xy_pos[1])

    if angle is not None:
        mo.xy_scanner.Angle(angle)


def set_points_lines(points=None, lines=None):
    """
    Sets the number of points and lines of the scan.

    Parameters
    ----------
    points : int or None
        Number of points
    lines : int or None
        Number of lines

    Examples
    --------
    Set both points and lines to 150
    >>> set_points_lines(150)

    Set both points and lines to 150
    >>> set_points_lines(points=150, lines=150)

    Set points and lines to different amounts
    >>> set_points_lines(110, 130)
    """
    mo.experiment.stop()
    mo.xy_scanner.Points_Lines_Constrained(True)
    if points != lines:
        if points is not None and lines is not None:
            mo.xy_scanner.Points_Lines_Constrained(False)
        else:
            lines = points

    mo.xy_scanner.Points(points)
    mo.xy_scanner.Lines(lines)


def get_xy_scan(channel_name, x_direction, y_direction, num_lines='all', mode='new'):
    """
    Perform and get an xy scan

    Parameters
    ----------
    channel_name : str
        The channel to acquire from, e.g. Z, I, Aux1, Aux2
    x_direction : str
        Must be one of 'Forward' or 'Back'. 'Back' is currently not tested
    y_direction : str
        Must be one of 'Up' or 'Up-Down'
    num_lines : int or str
        Number of lines to get. If an int, must be less than the number of lines in the scanner window.
    mode : str
        Must be one of ['new', 'pause', 'continue']. Default is 'new'


    Returns
    -------
    xydata : numpy array if y_direction == "Up", list of two numpy arrays if y_direction == "Down"

    Examples
    --------
    >>> from nOmicron.microscope import IO
    >>> from nOmicron.utils.plotting import plot_xy
    >>> IO.connect()
    >>> xydata = get_xy_scan("Z", x_direction="Forward", y_direction="Up-Down")
    >>> plot_xy(xydata, pixel_scale=mo.xy_scanner.Width() * 1e9 / mo.xy_scanner.Points())
    >>> IO.disconnect()
    """
    global line_count, view_count, xydata

    allowed = ["new", "pause", "continue"]
    if mode not in allowed:
        raise ValueError(f"Mode must be one of {allowed}")

    if num_lines == 'all':
        num_lines = mo.xy_scanner.Lines()

    xydata = np.zeros((2, num_lines, mo.xy_scanner.Points()))
    xydata[:] = np.nan

    lines_per = num_lines
    if y_direction == "Up-Down":
        if num_lines != 'all' and num_lines != mo.xy_scanner.Lines():  # Force set lines instead?
            raise ValueError("If scanning in both directions, num_lines cannot be set")
        num_lines = num_lines * 2
        mo.xy_scanner.Y_Retrace(True)
    else:
        mo.xy_scanner.Y_Retrace(False)

    if x_direction != "Forward":
        mo.xy_scanner.X_Retrace(True)
        #raise NotImplementedError
    else:
        mo.xy_scanner.X_Retrace(False)

    view_count = [None, None]
    line_count = 0
    dir_dict = {"Forward": "Fw",
                "Backward": "Bw"}

    def view_xy_callback():
        global line_count, view_count, xydata
        line_count += 1
        pbar.update(1)
        if mo.view.Packet_Count() != line_count:
            warnings.warn("Not all lines delivered in time. Matrix may be unstable.")

        data_size = mo.view.Data_Size()
        scan_dir = (line_count - 1) // mo.xy_scanner.Lines()
        test = np.array(mo.sample_data(data_size))
        xydata[scan_dir, (line_count - lines_per * scan_dir) - 1, :] = test
        view_count = [mo.view.Run_Count(), mo.view.Cycle_Count()]
        mo.xy_scanner.resume()

    IO.enable_channel(f"{channel_name}_{dir_dict[x_direction]}")
    mo.xy_scanner.X_Retrace(False)
    mo.xy_scanner.X_Trace_Trigger(True)
    mo.view.Data(view_xy_callback)
    mo.allocate_sample_memory(mo.xy_scanner.Points())
    if mode == 'new':
        mo.experiment.start()
    elif mode == 'pause':
        mo.experiment.resume()
    else:
        pass

    pbar = tqdm(total=num_lines)
    while line_count < num_lines and mo.mate.rc == mo.mate.rcs['RMT_SUCCESS']:
        mo.wait_for_event()

    if mode == 'new':
        mo.experiment.stop()
    elif mode == 'pause':
        mo.experiment.pause()
    else:
        pass

    IO.disable_channel()

    xydata[0, :, :] = np.flipud(xydata[0, :, :])
    if y_direction == "Up":
        xydata = xydata[0, :, :]
    else:
        xydata = list(xydata)

    return xydata


if __name__ == "__main__":
    #IO.connect()
    set_points_lines(100)
    xydata1 = get_xy_scan(channel_name="Z", x_direction="Forward", y_direction="Up", num_lines=1)

    plot_xy(xydata1, view_count, pixel_scale=mo.xy_scanner.Width() * 1e9 / mo.xy_scanner.Points())

    mo.experiment.Result_File_Name()
