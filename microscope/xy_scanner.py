# Oliver Gordon, 2019

import warnings

import numpy as np
from tqdm import tqdm

import mate.objects as mo
from microscope import IO
from utils.plotting import plot_xy


def set_scan_position(xy_pos=None, width_height=None, angle=None):
    # Ignore anything set to None
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
    mo.experiment.stop()
    mo.xy_scanner.Points_Lines_Constrained(True)
    if points != lines:
        if points is not None and lines is not None:
            mo.xy_scanner.Points_Lines_Constrained(False)
        else:
            lines = points

    mo.xy_scanner.Points(points)
    mo.xy_scanner.Lines(lines)


def get_xy_scan(channel_name, x_direction, y_direction, num_lines='all'):
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


    Returns
    -------
    xydata : numpy array if y_direction == "Up", list of two numpy arrays if y_direction == "Down"

    Examples
    --------
    >>> from microscope import IO
    >>> from utils.plotting import plot_xy
    >>> IO.connect()
    >>> xydata = get_xy_scan("Z", x_direction="Forward", y_direction="Up-Down")
    >>> plot_xy(xydata, pixel_scale=mo.xy_scanner.Width() * 1e9 / mo.xy_scanner.Points())
    >>> IO.disconnect()
    """
    global line_count, xydata, view_count

    if num_lines == 'all':
        num_lines = mo.xy_scanner.Lines()
    lines_per = num_lines
    if y_direction == "Up-Down":
        if num_lines != 'all' and num_lines != mo.xy_scanner.Lines():  # Force set lines instead?
            raise ValueError("If scanning in both directions, num_lines cannot be set")
        num_lines = num_lines*2
        mo.xy_scanner.Y_Retrace(True)
    else:
        mo.xy_scanner.Y_Retrace(False)
    if x_direction != "Forward":
        raise NotImplementedError

    view_count = [None, None]
    line_count = 0
    xydata = np.zeros((2, mo.xy_scanner.Points(), mo.xy_scanner.Lines()))
    xydata[:] = np.nan
    dir_dict = {"Forward": "Fw",
                "Backward": "Bw"}

    def view_xy_callback():
        global line_count, xydata, view_count
        line_count += 1
        pbar.update(1)
        if mo.view.Packet_Count() != line_count:
            warnings.warn("Not all lines delivered in time. Matrix may be unstable.")

        data_size = mo.view.Data_Size()
        scan_dir = (line_count - 1) // mo.xy_scanner.Lines()
        xydata[scan_dir, (line_count - lines_per*scan_dir) - 1, :] = np.array(mo.sample_data(data_size))
        view_count = [mo.view.Run_Count(), mo.view.Cycle_Count()]
        mo.xy_scanner.resume()

    IO.enable_channel(f"{channel_name}_{dir_dict[x_direction]}")
    mo.xy_scanner.X_Retrace(False)
    mo.xy_scanner.X_Trace_Trigger(True)
    mo.view.Data(view_xy_callback)
    mo.allocate_sample_memory(mo.xy_scanner.Points())
    mo.experiment.start()

    pbar = tqdm(total=num_lines)
    while line_count < num_lines and mo.mate.rc == mo.mate.rcs['RMT_SUCCESS']:
        mo.wait_for_event()

    mo.experiment.stop()
    IO.disable_channel()

    xydata = list(np.flipud(xydata))
    if y_direction == "Up":
        xydata = xydata[0]

    return xydata


if __name__ == "__main__":
    IO.connect()
    set_points_lines(100)
    xydata = get_xy_scan(channel_name="Z", x_direction="Forward", y_direction="Up-Down")

    plot_xy(xydata, view_count, pixel_scale=mo.xy_scanner.Width() * 1e9 / mo.xy_scanner.Points())

    mo.experiment.Result_File_Name()
