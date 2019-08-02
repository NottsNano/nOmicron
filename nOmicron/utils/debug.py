# Oliver Gordon, 2019

import ctypes
import nOmicron.mate.objects as mo

from nOmicron.microscope import IO


def view_channel_properties(channel_name):
    # TODO: Rewrite!
    def read_prop(obj, prop):
        out = getattr(obj, prop)()
        print(prop + ':', out)

    channel_props = ['Enable']
    clock_props = ['Enable', 'Period', 'Samples']
    experiment_props = ['Bricklet_Written', 'Name', 'Result_File_Name',
                        'Result_File_Path', 'State']
    gap_voltage_control_props = ['Preamp_Range', 'Voltage']
    regulator_props = ['Enable_Z_Offset_Slew_Rate', 'Feedback_Loop_Enabled',
                       'Loop_Gain_1_I', 'Loop_Gain_2_I', 'Preamp_Range_1',
                       'Preamp_Range_2', 'Setpoint_1', 'Setpoint_2', 'Z_Offset',
                       'Z_Offset_Slew_Rate', 'Z_Out']
    view_props = ['Cycle_Count', 'Data_Size', 'Deliver_Data', 'Run_Count']
    xy_scanner_props = ['Angle', 'Area', 'Enable_Drift_Compensation', 'Lines',
                        'Offset', 'Plane_X_Slope', 'Plane_Y_Slope', 'Points',
                        'Raster_Time', 'Return_To_Stored_Position',
                        'Store_Current_Position', 'Target_Position',
                        'Trigger_Execute_At_Target_Position', 'XY_Position_Report',
                        'X_Drift', 'X_Retrace', 'X_Retrace_Trigger',
                        'X_Trace_Trigger', 'Y_Drift', 'Y_Retrace',
                        'Y_Retrace_Trigger', 'Y_Trace_Trigger']

    obj_names = ['channel', 'clock', 'experiment', 'gap_voltage_control',
                 'regulator', 'view', 'xy_scanner', 'spectroscopy']
    IO.connect()
    IO.enable_channel(channel_name)
    for obj_name in obj_names:
        obj = getattr(mo, obj_name)
        print()
        print('Object ' + obj_name + ':')
        print('--------------------------------------------------------------')
        for prop in eval(obj_name + '_props'):
            read_prop(obj, prop)

    mo.mate.disconnect()


def check_response_code(string_to_check, object_type):
    """Read the response code described by the Mate manual. e.g. View.I_V.Deliver_Data"""

    class String(ctypes.Structure):
        _fields_ = [('length', ctypes.c_int),
                    ('text', ctypes.c_char * 256)]

    bt = bytearray()
    bt.extend(string_to_check.encode())
    string_to_check = bytes(bt)

    lib_mate = mo.mate.lib_mate
    b = ctypes.c_char()
    i = ctypes.c_int()
    e = ctypes.c_int()
    d = ctypes.c_double()
    s = String(255)
    p_s = ctypes.pointer(s)
    d1 = ctypes.c_double()
    d2 = ctypes.c_double()

    response = dict()
    response_strings = {v: k for k, v in mo.mate.rcs.items()}

    if object_type == "bool":
        response["response_code"] = lib_mate.getBooleanProperty(string_to_check, -1, ctypes.byref(b))
        response["response_value"] = bool(ord(b.value))
    elif object_type == "int":
        response["response_code"] = lib_mate.getIntegerProperty(string_to_check, -1, ctypes.byref(b))
        response["response_value"] = i.value
    elif object_type == "str":
        response["response_code"] = lib_mate.getStringPropertyByDesc(string_to_check, -1, ctypes.byref(p_s))
        response["response_value"] = s.text[:].decode()
    elif object_type == "enum":
        response["response_code"] = lib_mate.getEnumProperty(string_to_check, -1, ctypes.byref(e))
        response["response_value"] = e.value
    elif object_type == "double":
        response["response_code"] = lib_mate.getDoubleProperty(string_to_check, -1, ctypes.byref(d))
        response["response_value"] = d.value
    elif object_type == "pair":
        response["response_code"] = lib_mate.getPairProperty(string_to_check, -1, ctypes.byref(d1), ctypes.byref(d2))
        response["response_value"] = (d1.value, d2.value)
    else:
        raise KeyError("Not a gettable type")

    response["response_string"] = response_strings[response["response_code"]]

    return response
