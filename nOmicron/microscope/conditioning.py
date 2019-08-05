# Oliver Gordon, 2019
import numpy as np

from nOmicron.mate import objects as mo


def tip_pulse(voltage, time, num_pulses=1, feedback_loop=True):
    """
    Performs a tip voltage pulse.

    Parameters
    ----------
    voltage : float
        The voltage (in volts)
    time : float
        The time (in seconds)
    num_pulses : int
        The number of times to pulse. Default is 1
    feedback_loop : bool
        If the feedback loop is on or not. Default True
    """

    if np.abs(voltage) >= 1:
        mo.gap_voltage_control.Tip_Cond_Pulse_Preamp_Range(1)
    mo.gap_voltage_control.Tip_Cond_Enable_Feedback_Loop(True)

    if not feedback_loop:
        mo.gap_voltage_control.Tip_Cond_Enable_Feedback_Loop(False)

    mo.gap_voltage_control.Tip_Cond_Pulse_Time(time)
    mo.gap_voltage_control.Tip_Cond_Pulse_Voltage(voltage)

    for i in range(num_pulses):
        mo.experiment.pause()
        mo.gap_voltage_control.Tip_Cond_Pulse_Apply()
        mo.experiment.resume()


def tip_crash(delta_z, crash_position=(-1, -1), delay=0, slew_rate=None):
    """
    Performs a controlled tip indendation.

    Parameters
    ----------
    delta_z : float
        The depth to ramp in meters
    crash_position : tuple
        The position in normalised co-ordinate range(-1, 1) to perform the crash at.
        Default is (-1, -1), which corresponds to the bottom left corner of the scan window
    delay : float
        The time to continuously sample Z position before doing the crash. The average value is used as the start
        position to calculate delta_z from. Default is 0
    slew_rate : float or None
        The slew rate in metres/second. Not enabled in None (default)

    """
    mo.regulator.Enable_Z_Ramp_Slew_Rate(False)
    mo.regulator.Z_Ramp_Delay(delay)
    mo.regulator.Z_Ramp(delta_z)

    if slew_rate is not None:
        mo.regulator.Enable_Z_Ramp_Slew_Rate(True)
        mo.regulator.Z_Ramp_Slew_Rate(slew_rate)

    mo.experiment.pause()
    mo.xy_scanner.Execute_Port_Colour("ZRamp")
    mo.xy_scanner.Store_Current_Position(True)
    mo.xy_scanner.Target_Position(crash_position)
    mo.xy_scanner.Trigger_Execute_At_Target_Position(True)

    mo.xy_scanner.move()

    mo.xy_scanner.Trigger_Execute_At_Target_Position(False)
    mo.xy_scanner.Return_To_Stored_Position(True)
    mo.xy_scanner.Store_Current_Position(False)
    mo.xy_scanner.Execute_Port_Colour("")
    mo.experiment.resume()
