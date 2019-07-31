import mate.objects as mo
import numpy as np
from microscope import IO

# def scan_constraint

# def get_scan(channel_name, direction, num_lines):
#     global retraces, linescan
#     retraces = 0
#     linescan = None
#     dir_dict = {"up": "Fw",
#                 "down": "Bw"}
#
#     def view_xy_callback():
#         global retraces, linescan
#         retraces += 1
#         print(mo.view.Data_Size())
#         data_size = mo.view.Data_Size()
#         print(mo.view.Data())
#         print(mo.view.Run_Count(), mo.view.Cycle_Count(), mo.view.Packet_Count())
#         linescan = np.array(mo.sample_data(data_size))
#         mo.xy_scanner.resume()
#
#     IO.enable_channel(f"{channel_name}_{dir_dict[direction]}")
#     mo.xy_scanner.X_Retrace(False)
#     reset_value = mo.xy_scanner.X_Trace_Trigger()
#     mo.xy_scanner.X_Trace_Trigger(True)
#     mo.xy_scanner.X_Trace_Done(view_xy_callback)
#     mo.experiment.start()
#     mo.allocate_sample_memory(20)
#     while retraces < num_lines+1 and mo.mate.rc == mo.mate.rcs['RMT_SUCCESS']:
#         mo.wait_for_event()
#     mo.view.Data()
#
#     mo.experiment.stop()
#     mo.xy_scanner.X_Trace_Trigger()
#     mo.xy_scanner.X_Trace_Trigger(reset_value)
#     IO.disable_channel()

def try_again(channel_name, direction, num_lines):
    global retraces, linescan
    retraces = 0
    linescan = None
    dir_dict = {"up": "Fw",
                "down": "Bw"}
#
    def view_xy_callback():
        global retraces, linescan
        retraces += 1
        print(mo.view.Data_Size())
        data_size = mo.view.Data_Size()
        print(mo.view.Data())
        print(mo.view.Run_Count(), mo.view.Cycle_Count(), mo.view.Packet_Count())
        linescan = np.array(mo.sample_data(data_size))
        print(linescan)
        mo.xy_scanner.resume()
#
    def test():
        print('a')
        mo.view.Data(view_xy_callback)
        mo.allocate_sample_memory(20)
        while retraces < 1 and mo.mate.rc == mo.mate.rcs['RMT_SUCCESS']:
            mo.wait_for_event()
        mo.view.Data()

    IO.enable_channel(f"{channel_name}_{dir_dict[direction]}")
    mo.xy_scanner.X_Retrace(False)
    mo.xy_scanner.X_Trace_Trigger(True)
    mo.xy_scanner.X_Trace_Done(test)
    mo.experiment.restart()
    while retraces < 20 and mo.mate.rc == mo.mate.rcs['RMT_SUCCESS']:
        mo.wait_for_event()
    mo.view.Data()

    mo.experiment.stop()
    IO.disable_channel()


if __name__ == "__main__":
    IO.connect()
    try_again("Z", "up", 20)
