# Oliver Gordon, 2019

import warnings

import nOmicron.mate.objects as mo
import numpy as np
from nOmicron.microscope import IO
from nOmicron.utils.plotting import plot_xy
from tqdm.auto import tqdm
from time import sleep

def set_gap_voltage(voltage):
    mo.gap_voltage_control.Voltage(voltage)


def set_scan_position(xy_pos=None, width_height=None, angle=None):
    mo.xy_scanner.Enable_Scan(False)

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

    mo.xy_scanner.Enable_Scan(True)


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


def set_scan_speed(scan=None, move=None, speed_adjust_mode="Frequency"):
    """
    Sets the scan and move t-raster elements

    Parameters
    ----------
    scan : float or None
        Time span between two adjacent raster points, in seconds
    move : float or None
        Time span between movements of the y scan, in seconds
    speed_adjust_mode : str
        The adaption method to keep constant when changing the adjust the scan raster/speed time.
        Must be either ["Frequency", "Speed"]. Default is "Frequency".

    Examples
    --------
    Set both scan and move to 150ms
    >>> set_scan_speed(150e-3)

    Set both points and lines to 150ms
    >>> set_scan_speed(points=150e-3, lines=150e-3)

    Set points and lines to different amounts
    >>> set_scan_speed(110e-3, 130e-3)
    """
    speed_modes = {"Frequency": 1, "Speed": 2}
    if speed_adjust_mode not in speed_modes.values():
        raise ValueError(f"Must be one of {speed_modes.values()}")
    mo.xy_scanner.Speed_Adaption(speed_modes[speed_adjust_mode])

    mo.xy_scanner.Move_Raster_Time_Constrained(True)
    if scan != move:
        if scan is not None and move is not None:
            mo.xy_scanner.Move_Raster_Time_Constrained(False)
        else:
            move = scan

    mo.xy_scanner.Raster_Time(scan)
    mo.xy_scanner.Move_Raster_Time(move)


def get_xy_scan(channel_name, x_direction, y_direction, num_lines='all', mode='new', return_filename=False):
    """
    Perform and get an xy scan

    Parameters
    ----------
    channel_name : str
        The channel to acquire from, e.g. Z, I, Aux1, Aux2
    x_direction : str
        Must be one of 'Forward', 'Backward', or 'Forward-Backward'
    y_direction : str
        Must be one of 'Up' or 'Up-Down'
    num_lines : int or str
        Number of lines to get. If an int, must be less than the number of lines in the scanner window.
        Default is 'all'
    mode : str, optional
        Must be one of ['new', 'pause', 'continue']. Default is 'new'
    return_filename : bool, optional
        If the full file name of the scan should be returned along with the data. Default is False

    Returns
    -------
    xydata : ndarray
        Max 4 dimensions (y_up/y_down, x_up/x_down, x, y). First two dimensions will only appear if
        y_direction is "Up-Down" and x_direction is "Forward-Backward" - will be missing as appropriate

    Examples
    --------
    >>> from nOmicron.microscope import IO
    >>> from nOmicron.utils.plotting import plot_xy
    >>> IO.connect()
    >>> xydata = get_xy_scan("Z", x_direction="Forward", y_direction="Up-Down")
    >>> plot_xy(xydata, pixel_scale=mo.xy_scanner.Width() * 1e9 / mo.xy_scanner.Points())
    >>> IO.disconnect()

    Warnings
    --------
    Quite often (but unreliably!), running this function will get Matrix into a state in which it will return one/two
    lines (unless play/pause is clicked manually) when operating manually. To restore this functionality, run
    utils.utils.restore_z_functionality() and restart your scan.
    """
    global scan_dir_x, scan_dir_y, line_count_y, view_count, tot_packets, xydata

    # Setup and parsing parameters
    allowed = ["new", "pause", "continue"]
    if mode not in allowed:
        raise ValueError(f"Mode must be one of {allowed}")

    if num_lines == 'all':
        num_lines = mo.xy_scanner.Lines()

    x_dir_dict = {"Forward": "Fw",
                  "Backward": "Bw"}
    x_direction_strings = [x_dir_dict[x_dir] for x_dir in x_direction.split("-")]
    y_direction_strings = y_direction.split("-")

    # Set triggers
    if x_direction == "Forward-Backward":
        mo.xy_scanner.X_Retrace(True)
    else:
        mo.xy_scanner.X_Retrace(False)

    if y_direction == "Up-Down":
        if num_lines != 'all' and num_lines != mo.xy_scanner.Lines():  # Force set lines instead?
            raise ValueError("If scanning in both directions, num_lines cannot be set")
        mo.xy_scanner.Y_Retrace(True)
    else:
        mo.xy_scanner.Y_Retrace(False)

    # while not mo.xy_scanner.Enable_Scan():  # Enforce that we won't take data during relocation and confuse the CU
    #     print("waiting")
    #     sleep(0.1)

    # Set counters and pre-allocate
    view_count = [None, None]
    scan_dir_y = 0
    scan_dir_x = 1
    line_count_y = 0
    tot_packets = 0
    xydata = np.zeros((2, 2, num_lines, mo.xy_scanner.Points()))
    xydata[:] = np.nan

    def view_xy_callback():
        global scan_dir_x, scan_dir_y, line_count_y, view_count, tot_packets, xydata
        tot_packets += 1
        mo.tot_packets = tot_packets
        line_count_y += 1
        if x_direction == "Forward-Backward":
            scan_dir_x = int(not (bool(scan_dir_x)))
            line_count_y = line_count_y - scan_dir_x
        scan_dir_y = (line_count_y - 1) // num_lines

        data_size = mo.view.Data_Size()
        data_pts = np.array(mo.sample_data(data_size))

        xydata[scan_dir_y, int(not (bool(scan_dir_x))), (line_count_y - (num_lines * scan_dir_y)) - 1, :] = data_pts
        view_count = [mo.view.Run_Count(), mo.view.Cycle_Count()]

        pbar.update(1)
        # pbar.set_postfix({"Scanline": mo.view.Packet_Count()})
        # if tot_packets % 2 == 1:
        #     pbar.set_postfix({"Scanline": mo.view.Packet_Count()+1})

    # Enable channels
    for x_direction_string in x_direction_strings:
        IO.enable_channel(f"{channel_name}_{x_direction_string}")
        mo.view.Data(view_xy_callback)
        mo.allocate_sample_memory(mo.xy_scanner.Points())

    if mode == 'new':
        mo.experiment.start()
    elif mode == 'pause':
        mo.experiment.resume()
    else:
        pass

    # Get the data
    pbar = tqdm(total=num_lines * len(x_direction_strings) * len(y_direction_strings))
    while tot_packets < num_lines * len(x_direction_strings) * len(y_direction_strings) \
            and mo.mate.rc == mo.mate.rcs['RMT_SUCCESS']:
        mo.wait_for_event()

    if mode == 'new':
        mo.experiment.stop()
    elif mode == 'pause':
        mo.experiment.pause()
    else:
        pass

    # Pretty the output to make physical sense
    xydata = np.flip(xydata, axis=2)
    if len(x_direction_strings) != 2:
        xydata = xydata[:, 0, :, :]
    if len(y_direction_strings) != 2:
        xydata = xydata[0, :, :, :]
    np.squeeze(xydata)

    # Return nicely
    if return_filename:
        filename = f"{mo.experiment.Result_File_Path()}\\{mo.experiment.Result_File_Name()}--{mo.view.Run_Count()}_{mo.view.Cycle_Count()}.Z_mtrx"
        return xydata, filename
    else:
        return xydata


if __name__ == "__main__":
    IO.connect()
    set_points_lines(128)
    xydata1 = get_xy_scan(channel_name="Z", x_direction="Forward", y_direction="Up", num_lines=1)

    plot_xy(xydata1, view_count, pixel_scale=mo.xy_scanner.Width() * 1e9 / mo.xy_scanner.Points())

    mo.experiment.Result_File_Name()
