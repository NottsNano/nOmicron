#   Code up to mate4dummies 0.4.2 (at time of branch) is Copyright © 2015 - 2018 Stephan Zevenhuizen
#   MATE, (20-08-2018).

import ctypes as _ctypes
import inspect
import inspect as _inspect
import sys
import time as _time
from msvcrt import getch, kbhit
from random import random

from nOmicron.utils import utils
from nOmicron.utils.utils import is_parameter_allowable
from .mate import MATE as _MATE


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
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a


class _Clock(object):
    """Generates a continuous clock signal at a variable frequency, for use as a trigger source for data acquisition.
     Data cannot be streamed live, only sent in selected buffer chunks."""
    def __init__(self, period):
        self.period = period

    def Enable(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Period(self, a=None):
        if mate.testmode and a:
            self.period = a
        test = self.period
        p = 'double'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Samples(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a


class _Experiment(object):
    """Core features of the experiment. Can read/change the state of the experiment."""
    def Bricklet_Ready(self, test=''):
        p = 'string'
        a = _process(p, [self, _inspect.stack()[0][3]], None, test)
        return a

    def Bricklet_Written(self, test=''):
        p = 'string'
        a = _process(p, [self, _inspect.stack()[0][3]], None, test)
        return a

    def Name(self, test=''):
        p = 'string'
        a = _process(p, [self, _inspect.stack()[0][3]], None, test)
        return a

    def Result_File_Name(self, test=''):
        p = 'string'
        a = _process(p, [self, _inspect.stack()[0][3]], None, test)
        return a

    def Result_File_Path(self, test=''):
        p = 'string'
        a = _process(p, [self, _inspect.stack()[0][3]], None, test)
        return a

    def State(self, test='test mode'):
        p = 'string'
        a = _process(p, [self, _inspect.stack()[0][3]], None, test)
        return a

    def pause(self):
        p = 'function'
        out = _process(p, [self, _inspect.stack()[0][3]], None)

    def resume(self):
        p = 'function'
        out = _process(p, [self, _inspect.stack()[0][3]], None)

    def start(self):
        p = 'function'
        out = _process(p, [self, _inspect.stack()[0][3]], None)

    def stop(self):
        p = 'function'
        out = _process(p, [self, _inspect.stack()[0][3]], None)

    def restart(self):
        p = 'function'
        out = _process(p, [self, _inspect.stack()[0][3]], None)

    def upload(self):
        p = 'function'
        out = _process(p, [self, _inspect.stack()[0][3]], None)

    def unload(self):
        p = 'function'
        out = _process(p, [self, _inspect.stack()[0][3]], None)


class _GapVoltageControl(object):
    """Control the gap voltage between the STM probe and the sample."""
    def Preamp_Range(self, a=None, test=0):
        p = 'enum'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Voltage(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a


class _PiezoControl(object):
    """Controls tip approach."""
    def Approach(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Move_Auto(self, a=None, test=True):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Move_Backward(self, a=None, test=True):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Move_Forward(self, a=None, test=True):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Move_Tip_X_Minus(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Move_Tip_X_Plus(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Move_Tip_Y_Minus(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Move_Tip_Y_Plus(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Retract(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def isLocked(self, s, test=0):
        p = 'function'
        out = _process(p, [self, _inspect.stack()[0][3]], s, test)
        return out


class _Regulator(object):
    """Controls the Z position of the probe."""
    def Enable_Z_Offset_Slew_Rate(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Feedback_Loop_Enabled(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Loop_Gain_1_I(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Loop_Gain_2_I(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Preamp_Range_1(self, a=None, test=0):
        p = 'enum'
        # is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Preamp_Range_2(self, a=None, test=0):
        p = 'enum'
        # is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Setpoint_1(self, a=None, test=0.0):
        p = 'double'
        # is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Setpoint_2(self, a=None, test=0.0):
        p = 'double'
        # is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Z_Offset(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Z_Offset_Slew_Rate(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Z_Out(self, test=0.0):
        p = 'double'
        a = _process(p, [self, _inspect.stack()[0][3]], None, test)
        return a


class _View(object):
    """Allows for the delivery of data. Open the channel with IO.py, set Deliver_Data to True and return data
    with Data() and a callback if desired."""
    def Cycle_Count(self, test=0):
        p = 'unsigned_integer'
        a = _process(p, [self, _inspect.stack()[0][3]], None, test)
        return a

    def Data(self, f=None, *args, **kwargs):
        p = 'set_observed'
        out = _process(p, [self, _inspect.stack()[0][3]], f, *args, **kwargs)

    def Data_Size(self, test=None):
        if mate.testmode and not test:
            test = _p_values[0].values[0].realArray[0][0].length
        p = 'unsigned_integer'
        a = _process(p, [self, _inspect.stack()[0][3]], None, test)
        return a

    def Deliver_Data(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Run_Count(self, test=0):
        p = 'unsigned_integer'
        a = _process(p, [self, _inspect.stack()[0][3]], None, test)
        return a

    def Cycle_Count(self, test=0):
        p = 'unsigned_integer'
        a = _process(p, [self, _inspect.stack()[0][3]], None, test)
        return a

    def Packet_Count(self, test=0):
        p = 'unsigned_integer'
        a = _process(p, [self, _inspect.stack()[0][3]], None, test)
        return a


class _XYScanner(object):
    """Controls the image generation of the scan"""
    def Angle(self, a=None, test=0):
        p = 'integer'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Area(self, a=None, test=[0.0, 0.0]):
        p = 'pair'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Enable_Drift_Compensation(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Execute_Port_Colour(self, a=None, test=0):
        """Here be dragons."""
        p = 'string'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Lines(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Offset(self, a=None, test=[0.0, 0.0]):
        p = 'pair'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Plane_X_Slope(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Plane_Y_Slope(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Points(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Raster_Time(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Return_To_Stored_Position(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Store_Current_Position(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Target_Position(self, a=None, test=[0.0, 0.0]):
        p = 'pair'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Trigger_Execute_At_Target_Position(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def XY_Position_Report(self, test=[0.0, 0.0]):
        p = 'pair'
        a = _process(p, [self, _inspect.stack()[0][3]], None, test)
        return a

    def X_Drift(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def X_Retrace(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def X_Retrace_Done(self, f=None, *args, **kwargs):
        p = 'set_observed'
        out = _process(p, [self, _inspect.stack()[0][3]], f, *args, **kwargs)

    def X_Retrace_Trigger(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def X_Trace_Done(self, f=None, *args, **kwargs):
        p = 'set_observed'
        out = _process(p, [self, _inspect.stack()[0][3]], f, *args, **kwargs)

    def X_Trace_Trigger(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Y_Drift(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Y_Retrace(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Y_Retrace_Done(self, f=None, *args, **kwargs):
        p = 'set_observed'
        out = _process(p, [self, _inspect.stack()[0][3]], f, *args, **kwargs)

    def Y_Retrace_Trigger(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Y_Trace_Done(self, f=None, *args, **kwargs):
        p = 'set_observed'
        out = _process(p, [self, _inspect.stack()[0][3]], f, *args, **kwargs)

    def Y_Trace_Trigger(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def move(self):
        p = 'function'
        out = _process(p, [self, _inspect.stack()[0][3]], None)

    def resume(self):
        p = 'function'
        out = _process(p, [self, _inspect.stack()[0][3]], None)

    def execute(self):
        p = 'function'
        out = _process(p, [self, _inspect.stack()[0][3]], None)


class _Spectroscopy:
    """Controls spectroscopy. Device 1&2 are the first two channels in the Matrix window."""
    def Enable_Feedback_Loop(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Disable_Feedback_Loop(self, a=None, test=False):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Spectroscopy_Mode(self, a=None, test=0):
        p = 'enum'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def execute(self):
        p = 'function'
        out = _process(p, [self, _inspect.stack()[0][3]], None)

    def Device_1_Repetitions(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Device_1_Start(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Device_1_End(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Device_1_Points(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Raster_Time_1(self, a=None, test=0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Device_1_Offset_Delay(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Enable_Device_1_Ramp_Reversal(self, a=None, test=True):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Device_2_Repetitions(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Device_2_Start(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Device_2_End(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Device_2_Points(self, a=None, test=0):
        p = 'unsigned_integer'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Raster_Time_2(self, a=None, test=0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Device_2_Offset_Delay(self, a=None, test=0.0):
        p = 'double'
        is_parameter_allowable(a, self.__class__.__name__, _inspect.stack()[0][3], test)
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a

    def Enable_Device_2_Ramp_Reversal(self, a=None, test=True):
        p = 'boolean'
        a = _process(p, [self, _inspect.stack()[0][3]], a, test)
        return a


def read_min_max(module, parameter, test=0):
    """Reads the minimum and maximum allowed values for settable parameters."""
    p = 'function'
    module = utils._friendly_name_to_mate(module)
    members = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    inspected = [item[1] for item in members if item[0] == module][0]

    def get_value(min_max):
        if module == "_Clock":
            out = _process(p, [inspected(1.0), min_max], parameter, test)
        else:
            out = _process(p, [inspected(), min_max], parameter, test)
        if type(out) is tuple:
            out = out[0]
        return out

    outs = [get_value("min"), get_value("max")]
    return outs


def _process(p, caller, a, *args, **kwargs):
    global event_objects, _test_event_object
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
    if kbhit():
        esc = ord(getch()) == 27
    return no_event and not esc

def _check_rc():
    if mate.online and not mate.testmode:
        mate.exit_handler(mate.rc)


def _exit_handler():
    pass


def wait_for_event():
    print("Waiting...")
    log.AppendText('Waiting for event...\n')
    while _no_event():
        _time.sleep(0.05)


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
regulator = _Regulator()
view = _View()
xy_scanner = _XYScanner()
spectroscopy = _Spectroscopy()
esc = False
