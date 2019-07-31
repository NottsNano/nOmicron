# Oliver Gordon, 2019

import warnings

import mate.objects as mo
import numpy as np
from microscope import IO
from tqdm import tqdm

def set_scan_position(xy_pos, width_height, angle):
    if width_height[0] != width_height[1]:
        mo.xy_scanner.Width_Height_Constrained(False)
    mo.xy_scanner.W

def get_xy_scan(channel_name, direction, num_lines):
    global line_count, xydata
    line_count = 0
    xydata = np.zeros((mo.xy_scanner.Points(), mo.xy_scanner.Lines()))
    xydata[:] = np.nan
    dir_dict = {"up": "Fw",
                "down": "Bw"}

    def view_xy_callback():
        global line_count, xydata
        if mo.view.Packet_Count() != line_count:
            warnings.warn("Not all lines delivered in time (?). Is the scan speed too fast?")

        data_size = mo.view.Data_Size()
        xydata[line_count, :] = np.array(mo.sample_data(data_size))

        line_count += 1
        pbar.update(1)

        mo.xy_scanner.resume()

    IO.enable_channel(f"{channel_name}_{dir_dict[direction]}")
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

    return xydata

if __name__ == "__main__":
    IO.connect()
    mo.xy_scanner.Points(300)
    mo.xy_scanner.Lines(300)
    get_xy_scan("Z", "up", 30)