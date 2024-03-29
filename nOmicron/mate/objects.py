#   Code up to mate4dummies 0.4.2 (at time of branch) is Copyright © 2015 - 2018 Stephan Zevenhuizen
#   MATE, (20-08-2018).
#   Additional changes by Oliver Gordon, 2019

import ctypes as _ctypes
import inspect as _inspect
import time as _time
from msvcrt import getch, kbhit
from random import random
from time import sleep

from nOmicron.utils.utils import is_parameter_allowable

from .mate import MATE as _MATE
from ..utils.errors import MatrixNotInitialisedError


class _Text(object):

    def __init__(self, text):
        self.text = text

    def AppendText(self, text):
        self.text += text


class _Channel(object):
    """Acquires and pre-processes measurement data."""

    def Enable(self, a=None, test=True):
        """Determines the state of the data acquisition facility. If True, the element will produce a data stream
        whenever it gets triggered.

        Warnings
        --------
        This parameter must not be changed if the channel is currently active, i.e. produces data
        """
        p = 'boolean'
        a = _process(p, [self, "Enable"], a, test)
        return a


class _Clock(object):
    """Generates a continuous clock signal at a variable frequency, for use as a trigger source for data acquisition.
     Data cannot be streamed live, only sent in selected buffer chunks."""

    def __init__(self, period):
        self.period = period

    def Enable(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, "Enable"], a, test)
        return a

    def Period(self, a=None):
        if mate.testmode and a:
            self.period = a
        test = self.period
        p = 'double'
        a = _process(p, [self, "Period"], a, test)
        return a

    def Samples(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, "Samples", test)
        a = _process(p, [self, "Samples"], a, test)
        return a


class _Experiment(object):
    """Core features of the experiment. Can read/change the state of the experiment."""

    def Bricklet_Ready(self, test=''):
        p = 'string'
        a = _process(p, [self, "Bricklet_Ready"], None, test)
        return a

    def Bricklet_Written(self, test=''):
        p = 'string'
        a = _process(p, [self, "Bricklet_Written"], None, test)
        return a

    def Name(self, test=''):
        p = 'string'
        a = _process(p, [self, "Name"], None, test)
        return a

    def Result_File_Name(self, test=''):
        p = 'string'
        a = _process(p, [self, "Result_File_Name"], None, test)
        return a

    def Result_File_Path(self, test=''):
        p = 'string'
        a = _process(p, [self, "Result_File_Path"], None, test)
        return a

    def State(self, test='test mode'):
        p = 'string'
        a = _process(p, [self, "State"], None, test)
        return a

    def pause(self):
        p = 'function'
        out = _process(p, [self, "pause"], None)

    def resume(self):
        p = 'function'
        out = _process(p, [self, "resume"], None)

    def start(self):
        p = 'function'
        out = _process(p, [self, "start"], None)

    def stop(self):
        p = 'function'
        out = _process(p, [self, "stop"], None)

    def restart(self):
        p = 'function'
        out = _process(p, [self, "restart"], None)

    def upload(self):
        p = 'function'
        out = _process(p, [self, "upload"], None)

    def unload(self):
        p = 'function'
        out = _process(p, [self, "unload"], None)


class _GapVoltageControl(object):
    """Control the gap voltage between the STM probe and the sample."""

    def Preamp_Range(self, a=None, test=0):
        p = 'enum'
        a = _process(p, [self, "Preamp_Range"], a, test)
        return a

    def Voltage(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Voltage", test)
        a = _process(p, [self, "Voltage"], a, test)
        return a

    def Tip_Cond_Enable_Feedback_Loop(self, a=None, test=True):
        p = 'boolean'
        a = _process(p, [self, "Tip_Cond_Enable_Feedback_Loop"], a, test)
        return a

    def Tip_Cond_Pulse_Time(self, a=None, test=0.0):
        """Tip pulse time."""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Tip_Cond_Pulse_Time", test)
        a = _process(p, [self, "Tip_Cond_Pulse_Time"], a, test)
        return a

    def Tip_Cond_Pulse_Voltage(self, a=None, test=0.0):
        """Tip pulse voltage."""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Tip_Cond_Pulse_Voltage", test)
        a = _process(p, [self, "Tip_Cond_Pulse_Voltage"], a, test)
        return a

    def Tip_Cond_Pulse_Preamp_Range(self, a=None, test=0.0):
        """Tip pulse voltage range. 0 -> (-1,1). 1-> (-10, 10)."""
        p = 'enum'
        # is_parameter_allowable(a, self.__class__.__name__, "ASDasd", test)
        a = _process(p, [self, "Tip_Cond_Pulse_Preamp_Range"], a, test)
        return a

    # def Tip_Cond_Pulse_Apply(self, f=None, *args, **kwargs):
    #     """Does a tip conditioning"""
    #     p = 'set_observed'
    #     out = _process(p, [self, "ASDASDASDASD"], f, *args, **kwargs)

    def Tip_Cond_Pulse_Apply(self):
        """Super powerful. Do something, then run the trigger function on completion"""
        p = 'function'
        out = _process(p, [self, "Tip_Cond_Pulse_Apply"], None)

    def Execute(self):
        """Execute spectroscopy"""
        p = 'function'
        out = _process(p, [self, "Execute"], None)


class _PiezoControl(object):
    """Controls tip approach."""

    def Approach(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, "Approach", test)
        a = _process(p, [self, "Approach"], a, test)
        return a

    def Move_Auto(self, a=None, test=True):
        p = 'boolean'
        a = _process(p, [self, "Move_Auto"], a, test)
        return a

    def Move_Backward(self, a=None, test=True):
        p = 'boolean'
        a = _process(p, [self, "Move_Backward"], a, test)
        return a

    def Move_Forward(self, a=None, test=True):
        p = 'boolean'
        a = _process(p, [self, "Move_Forward"], a, test)
        return a

    def Move_Tip_X_Minus(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, "Move_Tip_X_Minus", test)
        a = _process(p, [self, "Move_Tip_X_Minus"], a, test)
        return a

    def Move_Tip_X_Plus(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, "Move_Tip_X_Plus", test)
        a = _process(p, [self, "Move_Tip_X_Plus"], a, test)
        return a

    def Move_Tip_Y_Minus(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, "Move_Tip_Y_Minus", test)
        a = _process(p, [self, "Move_Tip_Y_Minus"], a, test)
        return a

    def Move_Tip_Y_Plus(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, "Move_Tip_Y_Plus", test)
        a = _process(p, [self, "Move_Tip_Y_Plus"], a, test)
        return a

    def Retract(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, "Retract", test)
        a = _process(p, [self, "Retract"], a, test)
        return a

    def isLocked(self, s, test=0):
        p = 'function'
        out = _process(p, [self, "isLocked"], s, test)
        return out


class _Regulator(object):
    """Controls the Z position of the probe."""

    def TP_Disable(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, "TP_Disable"], a, test)
        return a

    def Enable_Z_Offset_Slew_Rate(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, "Enable_Z_Offset_Slew_Rate"], a, test)
        return a

    def Z_Ramp(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Z_Ramp", test)
        a = _process(p, [self, "Z_Ramp"], a, test)
        return a

    def Z_Ramp_Delay(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Z_Ramp_Delay", test)
        a = _process(p, [self, "Z_Ramp_Delay"], a, test)
        return a

    def Enable_Z_Ramp_Slew_Rate(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, "Enable_Z_Ramp_Slew_Rate"], a, test)
        return a

    def Z_Ramp_Slew_Rate(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Z_Ramp_Slew_Rate", test)
        a = _process(p, [self, "Z_Ramp_Slew_Rate"], a, test)
        return a

    def Feedback_Loop_Enabled(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, "Feedback_Loop_Enabled"], a, test)
        return a

    def Loop_Gain_1_I(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Loop_Gain_1_I", test)
        a = _process(p, [self, "Loop_Gain_1_I"], a, test)
        return a

    def Loop_Gain_2_I(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Loop_Gain_2_I", test)
        a = _process(p, [self, "Loop_Gain_2_I"], a, test)
        return a

    def Preamp_Range_1(self, a=None, test=0):
        p = 'enum'
        # is_parameter_allowable(a, self.__class__.__name__, "ASDasd", test)
        a = _process(p, [self, "Preamp_Range_1"], a, test)
        return a

    def Preamp_Range_2(self, a=None, test=0):
        p = 'enum'
        # is_parameter_allowable(a, self.__class__.__name__, "ASDasd", test)
        a = _process(p, [self, "Preamp_Range_2"], a, test)
        return a

    def Setpoint_1(self, a=None, test=0.0):
        p = 'double'
        # is_parameter_allowable(a, self.__class__.__name__, "ASDasd", test)
        a = _process(p, [self, "Setpoint_1"], a, test)
        return a

    def Setpoint_2(self, a=None, test=0.0):
        p = 'double'
        # is_parameter_allowable(a, self.__class__.__name__, "ASDasd", test)
        a = _process(p, [self, "Setpoint_2"], a, test)
        return a

    def Z_Offset(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Z_Offset", test)
        a = _process(p, [self, "Z_Offset"], a, test)
        return a

    def Z_Offset_Slew_Rate(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Z_Offset_Slew_Rate", test)
        a = _process(p, [self, "Z_Offset_Slew_Rate"], a, test)
        return a

    def Z_Out(self, test=0.0):
        p = 'double'
        a = _process(p, [self, "Z_Out"], None, test)
        return a

    def Setpoint_Detected(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, "Setpoint_Detected"], a, test)
        return a


class _View(object):
    """Allows for the delivery of data. Open the channel with IO.py, set Deliver_Data to True and return data
    with Data() and a callback if desired."""

    def Data(self, f=None, *args, **kwargs):
        p = 'set_observed'
        out = _process(p, [self, "Data"], f, *args, **kwargs)

    def Data_Size(self, test=None):
        if mate.testmode and not test:
            test = _p_values[0].values[0].realArray[0][0].length
        p = 'unsigned_integer'
        a = _process(p, [self, "Data_Size"], None, test)
        return a

    def Deliver_Data(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, "Deliver_Data"], a, test)
        return a

    def Run_Count(self, test=0):
        p = 'unsigned_integer'
        a = _process(p, [self, "Run_Count"], None, test)
        return a

    def Cycle_Count(self, test=0):
        p = 'unsigned_integer'
        a = _process(p, [self, "Cycle_Count"], None, test)
        return a

    def Packet_Count(self, test=0):
        p = 'unsigned_integer'
        a = _process(p, [self, "Packet_Count"], None, test)
        return a


class _XYScanner(object):
    """Controls general scan parameters, tip relocation, and triggering of functions after tip relocation"""

    def Angle(self, a=None, test=0):
        """Integer describing angle of scan"""
        p = 'integer'
        is_parameter_allowable(a, self.__class__.__name__, "Angle", test)
        a = _process(p, [self, "Angle"], a, test)
        return a

    def Area(self, a=None, test=[0.0, 0.0]):
        """Scan area in metres"""
        p = 'pair'
        is_parameter_allowable(a, self.__class__.__name__, "Area", test)
        a = _process(p, [self, "Area"], a, test)
        return a

    def Execute_Port_Colour(self, a=None, test=0):
        """Here be dragons."""
        p = 'string'
        a = _process(p, [self, "Execute_Port_Colour"], a, test)
        return a

    def Points(self, a=None, test=0):
        """Integer number of points to scan with. Fixed to Lines unless Points_Lines_Constrained = False"""
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, "Points", test)
        # print(self, "ASDasd")
        a = _process(p, [self, "Points"], a, test)
        return a

    def Lines(self, a=None, test=0):
        """Integer number of lines to scan per image. Fixed to Points unless Points_Lines_Constrained = False"""
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, "Lines", test)
        a = _process(p, [self, "Lines"], a, test)
        return a

    def Points_Lines_Constrained(self, a=None, test=False):
        """Boolean of if scan points and lines should be locked together"""
        p = 'boolean'
        a = _process(p, "Points_Lines_Constrained", a, test)
        return a

    def Enable_Scan(self, a=None, test=False):
        """Enable/Disable the scan"""
        p = 'boolean'
        a = _process(p, [self, "Enable_Scan"], a, test)
        return a

    def Offset(self, a=None, test=[0.0, 0.0]):
        """Scan-sample offset, in metres. Identical to setting X_Offset and Y_Offset separately."""
        p = 'pair'
        is_parameter_allowable(a, self.__class__.__name__, "Offset", test)
        a = _process(p, [self, "Offset"], a, test)
        return a

    def Enable_Drift_Compensation(self, a=None, test=False):
        """Boolean to enable drift compensation."""
        p = 'boolean'
        a = _process(p, [self, "Enable_Drift_Compensation"], a, test)
        return a

    def Enable_Plane_Slope(self, a=None, test=False):
        """Boolean for sample tilt correction. See also Plane_X_Slope, Plane_Y_Slope and Detect_Slope."""
        p = 'boolean'
        a = _process(p, [self, "Enable_Plane_Slope"], a, test)
        return a

    def Plane_X_Slope(self, a=None, test=0.0):
        """Sample slope in X direction. Percentage in range(-100, 100)"""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Plane_X_Slope", test)
        a = _process(p, [self, "Plane_X_Slope"], a, test)
        return a

    def Plane_Y_Slope(self, a=None, test=0.0):
        """Sample slope in Y direction. Percentage in range(-100, 100)"""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Plane_Y_Slope", test)
        a = _process(p, [self, "Plane_Y_Slope"], a, test)
        return a

    def Move_Raster_Time_Constrained(self, a=None, test=False):
        """Boolean of if scan raster and move should be locked together"""
        p = 'boolean'
        a = _process(p, [self, "Move_Raster_Time_Constrained"], a, test)
        return a

    def Raster_Time(self, a=None, test=0.0):
        """Time in seconds to move between scanning points. Identical to XYScanner.Move_Raster_Time. Real value is
        shown with Scan_Speed"""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Raster_Time", test)
        a = _process(p, [self, "Raster_Time"], a, test)
        return a

    def Move_Raster_Time(self, a=None, test=0.0):
        """Time in seconds to move between scanning points. Identical to XYScanner.Move_Raster_Time. Real value is
        shown with Scan_Speed"""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Move_Raster_Time", test)
        a = _process(p, [self, "Move_Raster_Time"], a, test)
        return a

    def Speed_Adaption(self, a=None, test=0):
        """Pick the speed adaption mode. 0 = constant line freq., 1 = constant scan speed"""
        p = 'enum'
        a = _process(p, [self, "Speed_Adaption"], a, test)
        return a

    def Scan_Speed(self, a=None, test=0.0):
        """Time in seconds to move between scanning points. Identical to XYScanner.Move_Raster_Time. Real value is
        shown with Scan_Speed"""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Scan_Speed", test)
        a = _process(p, [self, "Scan_Speed"], a, test)
        return a

    def Enable_Execute_Port(self, a=None, test=False):
        """Set to True to return the probe to the position set by XYScanner.Store_Current_Position"""
        p = 'boolean'
        a = _process(p, [self, "Enable_Execute_Port"], a, test)
        return a

    def Return_To_Stored_Position(self, a=None, test=False):
        """Set to True to return the probe to the position set by XYScanner.Store_Current_Position"""
        p = 'boolean'
        a = _process(p, [self, "Return_To_Stored_Position"], a, test)
        return a

    def Store_Current_Position(self, a=None, test=False):
        """Set to True to store the current scan position in hardware, to later recall with
        XYScanner.Return_To_Stored_Position"""
        p = 'boolean'
        a = _process(p, [self, "Store_Current_Position"], a, test)
        return a

    def Target_Position(self, a=None, test=[0.0, 0.0]):
        """Target position for tip within scanning window. NOT in metres, but co-ordinates in range (-1, 1)"""
        p = 'pair'
        a = _process(p, [self, "Target_Position"], a, test)
        return a

    def Trigger_Execute_At_Target_Position(self, a=None, test=False):
        """Boolean of if some function (e.g. spectroscopy) should be executed when the tip reaches the position
        described by XYScanner.Target_Position([x, y]), and beginning the movement with XYScanner.move()"""
        p = 'boolean'
        a = _process(p, [self, "Trigger_Execute_At_Target_Position"], a, test)
        return a

    def Width_Height_Constrained(self, a=None, test=False):
        """Boolean of if scan width and height should be locked together"""
        p = 'boolean'
        a = _process(p, [self, "Width_Height_Constrained"], a, test)
        return a

    def Width(self, a=None, test=0.0):
        """Scan width in metres"""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Width", test)
        a = _process(p, [self, "Width"], a, test)
        return a

    def Height(self, a=None, test=0.0):
        """Scan height in metres"""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Height", test)
        a = _process(p, [self, "Height"], a, test)
        return a

    def XY_Position_Report(self, test=[0.0, 0.0]):
        p = 'pair'
        a = _process(p, [self, "XY_Position_Report"], None, test)
        return a

    def X_Offset(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "X_Offset", test)
        a = _process(p, [self, "X_Offset"], a, test)
        return a

    def X_Drift(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "X_Drift", test)
        a = _process(p, [self, "X_Drift"], a, test)
        return a

    def X_Retrace(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, "X_Retrace"], a, test)
        return a

    def X_Retrace_Done(self, f=None, *args, **kwargs):
        p = 'set_observed'
        out = _process(p, [self, "X_Retrace_Done"], f, *args, **kwargs)

    def X_Retrace_Trigger(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, "X_Retrace_Trigger"], a, test)
        return a

    def X_Trace_Done(self, f=None, *args, **kwargs):
        p = 'set_observed'
        out = _process(p, [self, "X_Trace_Done"], f, *args, **kwargs)

    def X_Trace_Trigger(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, "X_Trace_Trigger"], a, test)
        return a

    def Y_Drift(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Y_Drift", test)
        a = _process(p, [self, "Y_Drift"], a, test)
        return a

    def Y_Offset(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Y_Offset", test)
        a = _process(p, [self, "Y_Offset"], a, test)
        return a

    def Y_Retrace(self, a=None, test=False):
        """If we should trigger and do something (e.g. acquire data) after a complete upwards (False) or upwards AND
        downwards (True) scan"""
        p = 'boolean'
        a = _process(p, [self, "Y_Retrace"], a, test)
        return a

    def Y_Retrace_Done(self, f=None, *args, **kwargs):
        """Allows us to call a callback (e.g. for data acquisition) after completing an entire forward AND backward
        scan. Y_Retrace_Trigger must first be set to True."""
        p = 'set_observed'
        out = _process(p, [self, "Y_Retrace_Done"], f, *args, **kwargs)

    def Y_Retrace_Trigger(self, a=None, test=False):
        """If we want to trigger and do something (e.g. acquire data) after completing an entire
        forward AND backward scan"""
        p = 'boolean'
        a = _process(p, [self, "Y_Retrace_Trigger"], a, test)
        return a

    def Y_Trace_Done(self, f=None, *args, **kwargs):
        """Allows us to call a callback (e.g. for data acquisition) after completing an entire forward scan.
        Y_Trace_Trigger must first be set to True."""
        p = 'set_observed'
        out = _process(p, [self, "Y_Trace_Done"], f, *args, **kwargs)

    def Y_Trace_Trigger(self, a=None, test=False):
        """If we want to trigger and do something (e.g. acquire data) after completing an entire forward scan"""
        p = 'boolean'
        a = _process(p, [self, "Y_Trace_Trigger"], a, test)
        return a

    def move(self):
        """Move the tip to the position set with Target_Position"""
        p = 'function'
        out = _process(p, [self, "move"], None)

    def resume(self):
        """Resume the imaging scan"""
        p = 'function'
        out = _process(p, [self, "resume"], None)

    def execute(self):
        """Super powerful. Do something, then run the trigger function on completion"""
        p = 'function'
        out = _process(p, [self, "execute"], None)

    def Operation_Cancelled(self):
        """Move the tip to the position set with Target_Position"""
        p = 'function'
        out = _process(p, [self, "Operation_Cancelled"], None)


class _Spectroscopy:
    """Controls spectroscopy. Device 1&2 are the first two channels in the Matrix window (?)."""

    def Enable_Feedback_Loop(self, a=None, test=False):
        """Enable the feedback loop"""
        p = 'boolean'
        a = _process(p, [self, "Enable_Feedback_Loop"], a, test)
        return a

    def Disable_Feedback_Loop(self, a=None, test=False):
        """Disable the feedback loop"""
        p = 'boolean'
        a = _process(p, [self, "Disable_Feedback_Loop"], a, test)
        return a

    def Spectroscopy_Mode(self, a=None, test=0):
        """Pick the channel to perform the spectroscopy on when calling Spectroscopy.execute().
         0->channel 1, 1->channel 2, 2->dragons"""
        p = 'enum'
        a = _process(p, [self, "Spectroscopy_Mode"], a, test)
        return a

    def execute(self):
        """Execute spectroscopy"""
        p = 'function'
        out = _process(p, [self, "execute"], None)

    def Device_1_Repetitions(self, a=None, test=0):
        """Integer describing number of repeats of spectra on channel 1"""
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, "Device_1_Repetitions", test)
        a = _process(p, [self, "Device_1_Repetitions"], a, test)
        return a

    def Device_1_Start(self, a=None, test=0.0):
        """Spectroscopy start value on channel 1"""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Device_1_Start", test)
        a = _process(p, [self, "Device_1_Start"], a, test)
        return a

    def Device_1_End(self, a=None, test=0.0):
        """Spectroscopy end value on channel 1"""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Device_1_End", test)
        a = _process(p, [self, "Device_1_End"], a, test)
        return a

    def Device_1_Points(self, a=None, test=0):
        """Spectroscopy points on channel 1"""
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, "Device_1_Points", test)
        a = _process(p, [self, "Device_1_Points"], a, test)
        return a

    def Raster_Time_1(self, a=None, test=0):
        """Time in seconds to acquire data at each spectroscopy step on channel 1."""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Raster_Time_1", test)
        a = _process(p, [self, "Raster_Time_1"], a, test)
        return a

    def Device_1_Offset_Delay(self, a=None, test=0.0):
        """Offset time"""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Device_1_Offset_Delay", test)
        a = _process(p, [self, "Device_1_Offset_Delay"], a, test)
        return a

    def Enable_Device_1_Ramp_Reversal(self, a=None, test=False):
        """More dragons."""
        p = 'boolean'
        a = _process(p, [self, "Enable_Device_1_Ramp_Reversal"], a, test)
        return a

    def Device_2_Repetitions(self, a=None, test=0):
        """Integer describing number of repeats of spectra on channel 2"""
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, "Device_2_Repetitions", test)
        a = _process(p, [self, "Device_2_Repetitions"], a, test)
        return a

    def Device_2_Start(self, a=None, test=0.0):
        """Spectroscopy start value on channel 2"""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Device_2_Start", test)
        a = _process(p, [self, "Device_2_Start"], a, test)
        return a

    def Device_2_End(self, a=None, test=0.0):
        """Spectroscopy end value on channel 2"""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Device_2_End", test)
        a = _process(p, [self, "Device_2_End"], a, test)
        return a

    def Device_2_Points(self, a=None, test=0):
        """Spectroscopy points on channel 2"""
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, "Device_2_Points", test)
        a = _process(p, [self, "ASDASDASDASD"], a, test)
        return a

    def Raster_Time_2(self, a=None, test=0):
        """Time in seconds to acquire data at each spectroscopy step on channel 2."""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Raster_Time_2", test)
        a = _process(p, [self, "Raster_Time_2"], a, test)
        return a

    def Device_2_Offset_Delay(self, a=None, test=0.0):
        """Offset time"""
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Device_2_Offset_Delay", test)
        a = _process(p, [self, "Device_2_Offset_Delay"], a, test)
        return a

    def Enable_Device_2_Ramp_Reversal(self, a=None, test=False):
        """More dragons."""
        p = 'boolean'
        a = _process(p, [self, "Enable_Device_2_Ramp_Reversal"], a, test)
        return a

class _CRTCService(object):
    def RCSC(self, a=None, test=False):
        p = 'unsigned_integer'
        a = _process(p, [self, "RCSC"], a, test)
        return a

class _PLLControl(object):
    """Controls the PLL regulator"""

    def Enable_Tip_Protection(self, a=None, test=False):
        is_parameter_allowable(a, self.__class__.__name__, "Enable_Tip_Protection", test)
        p = 'boolean'
        a = _process(p, [self, "Enable_Tip_Protection"], a, test)
        return a

    def Enable_Constant_Excitation_Mode(self, a=None, test=False):
        is_parameter_allowable(a, self.__class__.__name__, "Enable_Constant_Excitation_Mode", test)
        p = 'boolean'
        a = _process(p, [self, "Enable_Constant_Excitation_Mode"], a, test)
        return a

    def PLL_Enable(self, a=None, test=False):
        is_parameter_allowable(a, self.__class__.__name__, "PLL_Enable", test)
        p = 'boolean'
        a = _process(p, [self, "PLL_Enable"], a, test)
        return a

    def Auto_Phase(self, a=None, test=False):
        is_parameter_allowable(a, self.__class__.__name__, "Auto_Phase", test)
        p = 'boolean'
        a = _process(p, [self, "Auto_Phase"], a, test)
        return a

    def PLL_Centre_Frequency(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "PLL_Centre_Frequency", test)
        a = _process(p, [self, "PLL_Centre_Frequency"], a, test)
        return a

    def Amplitude_Detection_Mode(self, a=None, test=0):
        """0 = frequency selective, 1 = broadband"""
        p = 'enum'
        # is_parameter_allowable(a, self.__class__.__name__, "ASDasd", test)
        a = _process(p, [self, "Amplitude_Detection_Mode"], a, test)
        return a

    def Sensor_Resonance_Frequency_Range(self, a=None, test=0):
        """0 = 12.5-40 kHz, 1 = 15-60 kHz, 2 = 50-200 kHz, 3 = 150-500 kHz, 4 = 375-1250 kHz"""
        p = 'enum'
        # is_parameter_allowable(a, self.__class__.__name__, "ASDasd", test)
        a = _process(p, [self, "Sensor_Resonance_Frequency_Range"], a, test)
        return a

    def Non_Contact_Mode(self, a=None, test=0):
        """0 = constant amplitude, 1 = constant excitation, 2 = self excitation"""
        p = 'enum'
        # is_parameter_allowable(a, self.__class__.__name__, "ASDasd", test)
        a = _process(p, [self, "Non_Contact_Mode"], a, test)
        return a

    def Excitation_Attenuation_Constant_Amplitude(self, a=None, test=0):
        """0 = no attenuation, 1 = 0.1, 2 = 0.01, 3 = 0.001"""
        p = 'enum'
        # is_parameter_allowable(a, self.__class__.__name__, "ASDasd", test)
        a = _process(p, [self, "Excitation_Attenuation_Constant_Amplitude"], a, test)
        return a

    def Excitation_Attenuation_Constant_Excitation(self, a=None, test=0):
        """0 = no attenuation, 1 = 0.1, 2 = 0.01, 3 = 0.001"""
        p = 'enum'
        # is_parameter_allowable(a, self.__class__.__name__, "ASDasd", test)
        a = _process(p, [self, "Excitation_Attenuation_Constant_Excitation"], a, test)
        return a

    def Excitation_Attenuation_Self_Excitation(self, a=None, test=0):
        """0 = no attenuation, 1 = 0.1, 2 = 0.01, 3 = 0.001"""
        p = 'enum'
        # is_parameter_allowable(a, self.__class__.__name__, "ASDasd", test)
        a = _process(p, [self, "Excitation_Attenuation_Self_Excitation"], a, test)
        return a

    def Amplitude_Loop_Gain_I_Constant_Amplitude(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Amplitude_Loop_Gain_I_Constant_Amplitude", test)
        a = _process(p, [self, "Amplitude_Loop_Gain_I_Constant_Amplitude"], a, test)
        return a

    def Amplitude_Loop_Gain_P_Constant_Amplitude(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Amplitude_Loop_Gain_P_Constant_Amplitude", test)
        a = _process(p, [self, "Amplitude_Loop_Gain_P_Constant_Amplitude"], a, test)
        return a

    def Amplitude_Loop_Gain_I_Self_Excitation(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Amplitude_Loop_Gain_I_Self_Excitation", test)
        a = _process(p, [self, "Amplitude_Loop_Gain_I_Self_Excitation"], a, test)
        return a

    def Amplitude_Loop_Gain_P_Self_Excitation(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "Amplitude_Loop_Gain_P_Self_Excitation", test)
        a = _process(p, [self, "Amplitude_Loop_Gain_P_Self_Excitation"], a, test)
        return a

    def PLL_Loop_Gain_I(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "PLL_Loop_Gain_I", test)
        a = _process(p, [self, "PLL_Loop_Gain_I"], a, test)
        return a

    def PLL_Loop_Gain_P(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, "PLL_Loop_Gain_P", test)
        a = _process(p, [self, "PLL_Loop_Gain_P"], a, test)
        return a

    def Amplitude(self, test=0.0):
        """PLL amplitude. Read only"""
        p = 'double'
        a = _process(p, [self, "Amplitude"], None, test)
        return a

    def Delta_f(self, test=0.0):
        """PLL delta_f (Hz). Read only"""
        p = 'double'
        a = _process(p, [self, "Delta_f"], None, test)
        return a

    def Sensor_Frequency(self, test=0.0):
        """PLL sensor frequency (Hz). Read only"""
        p = 'double'
        a = _process(p, [self, "Sensor_Frequency"], None, test)
        return a

    def Damping(self, test=0.0):
        """PLL damping voltage (V). Read only"""
        p = 'double'
        a = _process(p, [self, "Damping"], None, test)
        return a

    def PLL_Locked(self, test=False):
        """See if the phase has been locked. Read only"""
        p = 'boolean'
        a = _process(p, [self, "PLL_Locked"], None, test)
        return a


def _process(p, caller, a, *args, **kwargs):
    global event_objects, _test_event_object
    if not hasattr(mate, "lib_mate"):
        raise MatrixNotInitialisedError()

    if caller[0].__class__.__name__ == '_Experiment':
        obj = mate.scope + '.' + caller[1]
    elif caller[0].__class__.__name__ == '_Channel':
        obj = channel_name + '.' + caller[1]
    elif caller[0].__class__.__name__ == '_Clock':
        obj = clock_name + '.' + caller[1]
    elif caller[0].__class__.__name__ == '_View':
        obj = 'View.' + channel_name + '.' + caller[1]
    else:
        obj = caller[0].__class__.__name__[1:] + '.' + caller[1]
    if p == 'string':
        if isinstance(a, str):
            func_params = [None, 'setString', obj, a]
            _, mate.rc = mate.remote_access(func_params, mate.rc)
        func_params = [args[0], 'getString', obj]
        a, mate.rc = mate.remote_access(func_params, mate.rc)
    elif p == 'boolean':
        if isinstance(a, bool):
            func_params = [None, 'setBoolean', obj, a]
            _, mate.rc = mate.remote_access(func_params, mate.rc)
        func_params = [args[0], 'getBoolean', obj]
        a, mate.rc = mate.remote_access(func_params, mate.rc)
    elif p == 'integer':
        if isinstance(a, int):
            func_params = [None, 'setInteger', obj, a]
            _, mate.rc = mate.remote_access(func_params, mate.rc)
        func_params = [args[0], 'getInteger', obj]
        a, mate.rc = mate.remote_access(func_params, mate.rc)
    elif p == 'unsigned_integer':
        if isinstance(a, int):
            func_params = [None, 'setInteger', obj, a]
            _, mate.rc = mate.remote_access(func_params, mate.rc)
        func_params = [args[0], 'getInteger', obj, _ctypes.c_uint()]
        a, mate.rc = mate.remote_access(func_params, mate.rc)
    elif p == 'enum':
        if isinstance(a, int):
            func_params = [None, 'setEnum', obj, a]
            _, mate.rc = mate.remote_access(func_params, mate.rc)
        func_params = [args[0], 'getEnum', obj]
        a, mate.rc = mate.remote_access(func_params, mate.rc)
    elif p == 'double':
        if isinstance(a, (int, float)):
            func_params = [None, 'setDouble', obj, a]
            _, mate.rc = mate.remote_access(func_params, mate.rc)
        func_params = [args[0], 'getDouble', obj]
        a, mate.rc = mate.remote_access(func_params, mate.rc)
    elif p == 'pair':
        if (isinstance(a, (list, tuple)) and len(a) == 2 and
                isinstance(a[0], (int, float)) and
                isinstance(a[1], (int, float))):
            func_params = [None, 'setPair', obj, a[0], a[1]]
            _, mate.rc = mate.remote_access(func_params, mate.rc)
        func_params = [args[0], 'getPair', obj]
        a, mate.rc = mate.remote_access(func_params, mate.rc)
    elif p == 'function':
        flat_value = mate.flat_values(0, 0, 1).values[0]
        if a and mate.testmode:
            if isinstance(args[0], bool):
                flat_value.type = 4
                flat_value.boolean = args[0]
            elif isinstance(args[0], int):
                flat_value.type = 1
                flat_value.integer = args[0]
            elif isinstance(args[0], float):
                flat_value.type = 2
                flat_value.real = args[0]
            elif (isinstance(args[0], (list, tuple)) and len(args[0]) == 2 and
                  isinstance(args[0][0], (int, float)) and
                  isinstance(args[0][1], (int, float))):
                flat_value.type = 6
                flat_value.pairX = args[0][0]
                flat_value.pairY = args[0][1]
        p_args = _ctypes.pointer(mate.flat_values(255, 0, 1))
        if a:
            if not isinstance(a, str):
                a = ''
            a = a.encode()
            p_args[0].values[0].type = mate.ValueType.vt_STRING
            p_args[0].values[0].string[0][0].length = len(a)
            p_args[0].values[0].string[0][0].text = a
        func_params = [flat_value, p, obj, p_args]
        out, mate.rc = mate.remote_access(func_params, mate.rc)
        if a:
            if out.type == 1:
                a = out.integer
            elif out.type == 2:
                a = out.real
            elif out.type == 4:
                a = bool(out.boolean)
            elif out.type == 5:
                a = out.enumeration
            elif out.type == 6:
                a = out.pairX, out.pairY
            else:
                a = None
    elif p == 'set_observed':
        if mate.testmode:
            _test_event_object = mate.scope + '::' + obj
        event_objects[obj] = [a, args, kwargs]
        func_params = [None, 'setObserved', obj, int(hasattr(a, '__call__'))]
        _, mate.rc = mate.remote_access(func_params, mate.rc)
    else:
        mate.rc = 0
    _check_rc()
    return a


def _no_event():
    global event_out, esc
    func_params = [(_test_event_object, 0, _p_values), 'getEvent']
    event_out, mate.rc = mate.remote_access(func_params, mate.rc)
    no_event = mate.rc == mate.rcs['RMT_NOEVENT']
    if mate.rc == mate.rcs['RMT_SUCCESS'] or mate.testmode:
        v = event_objects[event_out[0][len(mate.scope) + 2:]]
        v[0](*v[1], **v[2])
    # if kbhit():
    #     esc = ord(getch()) == 27
    return no_event# and not esc


def _check_rc():
    if mate.online and not mate.testmode:
        mate.exit_handler(mate.rc)


def _exit_handler():
    pass


def wait_for_event():
    log.AppendText('Waiting for event...\n')
    while _no_event():
        pass
        # sleep(0.01)


def get_clock_name(channel_name):
    global clock_name
    clock_name = mate.deployment_parameter(mate.scope, channel_name, 'Trigger')


def allocate_sample_memory(samples, test=None):
    global _p_values
    _p_values = _ctypes.pointer(mate.flat_values(0, samples, 1))
    if mate.testmode:
        if not test:
            b = 0.001
            a = -0.001
            test = [(b - a) * random() + a for i in range(samples)]
        _p_values[0].values[0].realArray[0][0].values = (_ctypes.c_double *
                                                         len(test))(*test)


def sample_data(data_size):
    return event_out[2][0].values[0].realArray[0][0].values[:data_size]


log = _Text('Starting log on ' + _time.strftime('%A, %d %B %Y %H:%M:%S',
                                                _time.localtime()) + '.\n')
mate = _MATE(log, _exit_handler, False)
event_objects = {}
_test_event_object = ''
_p_values = _ctypes.pointer(mate.flat_values(0, 0, 1))
event_out = ('', 0, _p_values)
channel_name = ''
clock_name = ''
channel = _Channel()
clock = _Clock(1.0)
experiment = _Experiment()
gap_voltage_control = _GapVoltageControl()
piezo_control = _PiezoControl()
pll = _PLLControl()
regulator = _Regulator()
view = _View()
xy_scanner = _XYScanner()
spectroscopy = _Spectroscopy()
crtcservice = _CRTCService()
tot_packets = 0
esc = False
