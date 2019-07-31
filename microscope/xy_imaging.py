import mate.objects as mo
import numpy as np
from microscope import IO
def get_scan(channel_name, direction, num_lines):
    global retraces
    retraces = 0
    dir_dict = {"up": "Fw",
                "down": "Bw"}

    def test(text):
        global retraces
        retraces += 1
        print(text)
        print('Retraces:', retraces)
        mo.xy_scanner.resume()

    reset_value = mo.xy_scanner.X_Retrace_Trigger()
    _ = mo.xy_scanner.X_Retrace_Trigger(True)
    mo.xy_scanner.X_Retrace_Done(test, 'Testing...')
    mo.experiment.restart()
    mo.esc = False
    while retraces < 20 and (mo.mate.rc == mo.mate.rcs['RMT_SUCCESS'] or
                             mo.mate.testmode) and not mo.esc:
        mo.wait_for_event()
    mo.experiment.stop()
    mo.xy_scanner.X_Retrace_Done()
    _ = mo.xy_scanner.X_Retrace_Trigger(reset_value)


if __name__ == "__main__":
    IO.connect()
    get_scan("Z", "up", 10)
    IO.disconnect()
