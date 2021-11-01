# Oliver Gordon, 2019
from time import sleep

import numpy as np

from nOmicron.mate import objects as mo


def tip_pulse(voltage, time, num_pulses=1, pos=None, feedback_loop=False):
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
    pos : None or tuple
        The position to do the pulse at, in normalised co-ords. If None, do it at the current tip position
    feedback_loop : bool
        If the feedback loop is on or not. Default False
    """

    mo.xy_scanner.Execute_Port_Colour("VPulse")
    if np.abs(voltage) >= 1:
        mo.gap_voltage_control.Tip_Cond_Pulse_Preamp_Range(1)
    else:
        mo.gap_voltage_control.Tip_Cond_Pulse_Preamp_Range(0)

    old_feedback_loop = mo.regulator.Feedback_Loop_Enabled()
    mo.regulator.Feedback_Loop_Enabled(feedback_loop)

    mo.gap_voltage_control.Tip_Cond_Pulse_Time(time)
    mo.gap_voltage_control.Tip_Cond_Pulse_Voltage(voltage)

    if pos is not None:
        # Do a pulse at position
        mo.xy_scanner.Store_Current_Position(True)
        mo.xy_scanner.Target_Position(pos)
        for i in range(num_pulses):
            mo.experiment.pause()
            mo.xy_scanner.Trigger_Execute_At_Target_Position(True)
            mo.xy_scanner.move()
            mo.xy_scanner.Trigger_Execute_At_Target_Position(False)
            mo.experiment.resume()
        mo.xy_scanner.Return_To_Stored_Position(True)
        mo.xy_scanner.Store_Current_Position(False)
        sleep(0.01)
    else:
        # Do a time period pulse - Tip_Cond_Pulse_Apply is super unreliable (?)
        for i in range(num_pulses):
            old_voltage = mo.gap_voltage_control.Voltage()
            mo.gap_voltage_control.Voltage(voltage)
            sleep(time)
            mo.gap_voltage_control.Voltage(old_voltage)
            # sleep(0.01)

    mo.regulator.Feedback_Loop_Enabled(old_feedback_loop)


def tip_crash(delta_z, pos=(-1, -1), delay=0, slew_rate=None):
    """
    Performs a controlled tip indendation.

    Parameters
    ----------
    delta_z : float
        The depth to ramp in meters.
    pos : tuple
        The position in normalised co-ordinate range(-1, 1) to perform the crash at.
        Default is (-1, -1), which corresponds to the bottom left corner of the scan window
    delay : float
        The time to continuously sample Z position before doing the crash. The average value is used as the start
        position to calculate delta_z from. Default is 0
    slew_rate : float or None
        The slew rate in metres/second. Not enabled in None (default)

    """
    assert delta_z > 0, "delta_z must be positive"
    # mo.experiment.pause()
    mo.xy_scanner.Execute_Port_Colour("ZRamp")
    mo.regulator.Enable_Z_Ramp_Slew_Rate(False)
    mo.regulator.Z_Ramp_Delay(delay)

    if slew_rate is not None:
        mo.regulator.Enable_Z_Ramp_Slew_Rate(True)
        mo.regulator.Z_Ramp_Slew_Rate(slew_rate)
    mo.regulator.Z_Ramp(-delta_z)

    mo.xy_scanner.Execute_Port_Colour("ZRamp")
    mo.xy_scanner.Store_Current_Position(True)
    mo.xy_scanner.Target_Position(pos)
    mo.xy_scanner.Trigger_Execute_At_Target_Position(True)

    mo.xy_scanner.move()

    mo.xy_scanner.Trigger_Execute_At_Target_Position(False)
    mo.xy_scanner.Return_To_Stored_Position(True)
    mo.xy_scanner.Store_Current_Position(False)
    mo.xy_scanner.Target_Position()
    mo.xy_scanner.Execute_Port_Colour("")
    # mo.experiment.resume()


def tip_scratch(delta_z, end_pos, start_pos=None):
    """
    Super destructive. Press the tip into the surface, move it, then come back out.

    Attributes
    ----------
    delta_z : float
        The depth to ramp in meters.
    start_pos : tuple or None
        The position in normalised co-ordinate range(-1, 1) to perform the initial crash at. Set to None (default)
        to start from the current position of the tip
    end_pos : tuple or None
        The position in normalised co-ordinate range(-1, 1) to finish the scratch at.
    """

    mo.xy_scanner.Store_Current_Position(True)
    mo.regulator.Feedback_Loop_Enabled(False)

    # Go to start position
    if start_pos is not None:
        mo.xy_scanner.Target_Position(start_pos)
        mo.xy_scanner.move()

    mo.regulator.Z_Offset(delta_z)  # Press in the tip

    mo.xy_scanner.Target_Position(end_pos)  # Move the tip
    mo.xy_scanner.move()

    mo.regulator.Z_Offset(0)  # Un-press the tip
    mo.regulator.Feedback_Loop_Enabled(True)

    # Return to start position
    mo.xy_scanner.Return_To_Stored_Position(True)
    mo.xy_scanner.Store_Current_Position(False)


def ink():
    pass


from nOmicron.microscope import IO
IO.connect()

# TO SATURATE
# Turn off feedback loop
mo.regulator.Feedback_Loop_Enabled(False)
# while True
    # Lower dZ on regulator by increment
    # Read current feedback loop for very short amount of time
    # If mean has not changed much since last 10? times round (i.e. are we asymptoptic?)
        # Take 5s reading
        # If std is low (10% of mean?) (i.e. are we definitely asymmptotic?)
            # Saturated
            # break
        # Else
            # Continue

# TO INK
# while True:
    # Increase dZ on regulator by increment
    # Read current feedback loop for very short amount of time
    # If mean has not changed much since last 10? times round (i.e. are we asymptoptic?)
        # Take 5s reading
        # If std is low (10% of mean?) (i.e. are we definitely asymmptotic?)
            # Fully retracted
            # Reenable feedback loop
            # Break
        # Else
            # Continue