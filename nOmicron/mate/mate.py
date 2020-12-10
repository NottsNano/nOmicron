#   Code up to mate4dummies 0.4.2 (at time of branch) is Copyright © 2015 - 2018 Stephan Zevenhuizen
#   MATE, (20-08-2018).
#   Additional changes by Oliver Gordon, 2019
import ctypes
import os
import re
import sys
import time
import xml.etree.ElementTree as ET

import pefile
import psutil
from natsort import natsort


class MATE(object):
    class ValueType:
        vt_INTEGER = 1
        vt_DOUBLE = 2
        vt_STRING = 3
        vt_BOOLEAN = 4
        vt_ENUM = 5
        vt_PAIR = 6
        vt_ARRAY_OF_DOUBLE = 7

    class String(ctypes.Structure):
        _fields_ = [('length', ctypes.c_int),
                    ('text', ctypes.c_char * 256)]

    def flat_values(self, string_length, array_length, length):
        pack = 4 * (1 + int(self.machine == 34404))

        class RealArray(ctypes.Structure):
            _pack_ = pack
            _fields_ = [('length', ctypes.c_int),
                        ('values', ctypes.c_double * array_length)]

        class FlatValue(ctypes.Structure):
            _pack_ = pack
            _fields_ = [('type', ctypes.c_int),
                        ('boolean', ctypes.c_int),
                        ('integer', ctypes.c_int),
                        ('enumeration', ctypes.c_int),
                        ('real', ctypes.c_double),
                        ('string', ctypes.POINTER(ctypes.POINTER(self.String))),
                        ('pairX', ctypes.c_double),
                        ('pairY', ctypes.c_double),
                        ('realArray',
                         ctypes.POINTER(ctypes.POINTER(RealArray)))]

        class FlatValues(ctypes.Structure):
            _fields_ = [('length', ctypes.c_int),
                        ('values', FlatValue * length)]

        flat_values = FlatValues(length)
        for i in range(length):
            o = flat_values.values[i]
            o.string = ctypes.pointer(ctypes.
                                      pointer(self.String(string_length)))
            o.realArray = ctypes.pointer(ctypes.
                                         pointer(RealArray(array_length)))
            flat_values.values[i] = o
        return flat_values

    def __init__(self, log, exit_handler2, testmode):
        self.log = log
        self.exit_handler2 = exit_handler2
        self.testmode = testmode
        self.rcs = dict(RMT_DEBUG=0x00000000,
                        RMT_SUCCESS=0x00000001,
                        RMT_UNEXPECTEDRESPONSE=0x00000002,
                        RMT_LIBNOTLOADABLE=0x00000004,
                        RMT_INTERNALFAILURE=0x00000006,
                        RMT_NOSERVER=(0x00000010 | 0x00000002),
                        RMT_NOEVENT=(0x00000020 | 0x00000003),
                        RMT_INCOMPATIBLEPROTOCOL=(0x00000010 | 0x00000004),
                        RMT_DISCONNECTED=(0x00000010 | 0x00000006),
                        RMT_UNSUPPORTEDREQ=(0x00000020 | 0x00000005),
                        RMT_UNKNOWNOBJECT=(0x00000020 | 0x00000002),
                        RMT_UNKNOWNPROPERTY=(0x00000020 | 0x00000004),
                        RMT_INVALIDTYPE=(0x00000020 | 0x00000006),
                        RMT_REJECTED=(0x00000020 | 0x00000008))
        self.experiments_directory = ''
        self.online = False
        self.is_ran_down = True
        self.rc = self.rcs['RMT_SUCCESS']
        pe = pefile.PE(sys.executable, fast_load=True)
        self.machine = pe.FILE_HEADER.Machine
        pe.close()

    def rc_key(self, rc):
        rc_key = list(self.rcs.keys())[list(self.rcs.values()).index(rc)]
        return rc_key

    def exit_handler(self, rc):
        if rc != self.rcs['RMT_SUCCESS'] and rc != self.rcs['RMT_NOEVENT']:
            self.exit_handler2()
            self.disconnect()
            self.log.AppendText('Active MATRIX experiment/project closed or '
                                'MATRIX software terminated.\n')

    def remote_access(self, p, rc):
        if rc == self.rcs['RMT_SUCCESS'] or rc == self.rcs['RMT_NOEVENT']:
            if len(p) > 2:
                p[2] = p[2].encode()
            if p[1] == 'getString':
                s = self.String(255)
                p_s = ctypes.pointer(s)
                rc = self.lib_mate.getStringPropertyByDesc(p[2], -1,
                                                           ctypes.byref(p_s))
                out = s.text[:].decode()
            elif p[1] == 'getBoolean':
                b = ctypes.c_char()
                rc = self.lib_mate.getBooleanProperty(p[2], -1,
                                                      ctypes.byref(b))
                out = bool(ord(b.value))
            elif p[1] == 'getInteger':
                if len(p) == 4:
                    i = p[3]
                else:
                    i = ctypes.c_int()
                rc = self.lib_mate.getIntegerProperty(p[2], -1,
                                                      ctypes.byref(i))
                out = i.value
            elif p[1] == 'getEnum':
                e = ctypes.c_int()
                rc = self.lib_mate.getEnumProperty(p[2], -1,
                                                   ctypes.byref(e))
                out = e.value
            elif p[1] == 'getDouble':
                d = ctypes.c_double()
                rc = self.lib_mate.getDoubleProperty(p[2], -1,
                                                     ctypes.byref(d))
                out = d.value
            elif p[1] == 'getDoubleArray':
                count = ctypes.c_int(len(p[0]))
                p_values = ctypes.pointer(list(map(ctypes.c_double, p[0])))
                rc = self.lib_mate.getDoubleArrayProperty(p[2], -1,
                                                          ctypes.byref(count),
                                                          ctypes.byref(p_values)
                                                          )
                out = p_values[0][:count]
            elif p[1] == 'getPair':
                d1 = ctypes.c_double()
                d2 = ctypes.c_double()
                rc = self.lib_mate.getPairProperty(p[2], -1,
                                                   ctypes.byref(d1),
                                                   ctypes.byref(d2))
                out = d1.value, d2.value
            elif p[1] == 'getEvent':
                prop = self.String(255)
                p_prop = ctypes.pointer(prop)
                value_count = ctypes.c_int()
                p_values = p[0][2]
                rc = self.lib_mate.getEntityEventByDesc(ctypes.byref(p_prop),
                                                        ctypes.
                                                        byref(value_count),
                                                        ctypes.
                                                        byref(p_values), 0)
                out = prop.text[:].decode(), value_count.value, p_values
            elif p[1] == 'trigger':
                rc = self.lib_mate.triggerProperty(p[2], -1)
                out = None
            elif p[1] == 'setString':
                rc = self.lib_mate.setStringProperty(p[2], -1,
                                                     p[3].encode())
                out = None
            elif p[1] == 'setBoolean':
                rc = self.lib_mate.setBooleanProperty(p[2], -1, p[3])
                out = None
            elif p[1] == 'setInteger':
                rc = self.lib_mate.setIntegerProperty(p[2], -1, p[3])
                out = None
            elif p[1] == 'setEnum':
                rc = self.lib_mate.setEnumProperty(p[2], -1, p[3])
                out = None
            elif p[1] == 'setDouble':
                d = ctypes.c_double(p[3])
                rc = self.lib_mate.setDoubleProperty(p[2], -1, d)
                out = None
            elif p[1] == 'setDoubleArray':
                count = len(p[3])
                p_value = ctypes.pointer(list(map(ctypes.c_double, p[3])))
                rc = self.lib_mate.setDoubleArrayProperty(p[2], -1,
                                                          count, p_value)
                out = None
            elif p[1] == 'setPair':
                d1 = ctypes.c_double(p[3])
                d2 = ctypes.c_double(p[4])
                rc = self.lib_mate.setPairProperty(p[2], -1, d1, d2)
                out = None
            elif p[1] == 'setObserved':
                rc = self.lib_mate.setObservedEntity(p[2], p[3])
                out = None
            elif p[1] == 'function':
                flat_value = p[0]
                p_args = p[3]
                rc = self.lib_mate.callFunctionByDesc(p[2],
                                                      ctypes.byref(flat_value),
                                                      ctypes.byref(p_args))
                out = flat_value
            else:
                rc = 0
                out = p[0]
            if (rc != self.rcs['RMT_SUCCESS'] and
                    rc != self.rcs['RMT_NOEVENT'] and
                    rc != self.rcs['RMT_UNKNOWNOBJECT']):
                out = p[0]
                self.log.AppendText('MATRIX error, response: ' +
                                    self.rc_key(rc) + '.\n')
        else:
            out = p[0]
        return out, rc

    def deployment_parameter(self, scope, eei_name, dp_name):
        path = self.experiments_directory
        try:
            tree = ET.parse(os.path.join(path, scope + '.exps'))
            root = tree.getroot()
            tag = 'ExperimentElementInstance'
            p = re.compile(r'^{.*?}(.*)')
            elements = [i for i in root if p.match(i.tag).group(1) == tag]
            eei = [i for i in elements if i.get('name') == eei_name]
            if len(eei) == 1:
                dp = [i for i in eei[0] if i.get('name') == dp_name]
                if len(dp) == 1:
                    value = dp[0].get('value').split('::')[0]
                else:
                    value = ''
            else:
                value = ''
        except:
            value = ''
        return value

    def experiment(self):
        path = self.experiments_directory
        try:
            experiments = [s[:-5] for s in os.listdir(path)
                           if s.endswith('.expd')]
        except:
            experiments = []
        l = len(experiments)
        e = enumerate(experiments)
        rc = 1
        state = 'closed'
        flag = (l != 0)
        while flag:
            i = next(e)
            prop = i[1] + '::' + i[1] + '.State'
            func_params = ['', 'getString', prop]
            state, rc = self.remote_access(func_params, 1)
            flag = (((rc == self.rcs['RMT_SUCCESS']) or
                     (rc == self.rcs['RMT_UNKNOWNOBJECT'])) and i[0] < l - 1 and
                    ((state == 'closed') or (state == '')))
        if ((rc == self.rcs['RMT_SUCCESS']) and (state != 'closed')) or \
                self.testmode:
            self.scope = i[1]
            self.lib_mate.setScopeName(i[1].encode())
            name = 'testmode'
            rfn = time.strftime('%Y%m%d-%H%M%S', time.localtime()) + \
                  '_' + name
            rfp = os.path.join(os.environ['USERPROFILE'], 'SPM-data')
            if not os.path.exists(rfp):
                try:
                    os.mkdir(rfp)
                except:
                    pass
            self.exp_params = {'Name': name, 'Result_File_Name': rfn,
                               'Result_File_Path': rfp}
            for parameter in list(self.exp_params.keys()):
                if not self.testmode:
                    prop = self.scope + '.' + parameter
                    func_params = ['', 'getString', prop]
                    value, rc = self.remote_access(func_params, rc)
                    self.exp_params[parameter] = value
                self.log.AppendText('Experiment parameter ' + parameter + ': ' +
                                    self.exp_params[parameter] + '.\n')
            self.online = (rc == self.rcs['RMT_SUCCESS']) or self.testmode
        else:
            self.scope = ''
            self.log.AppendText('No open experiments found.\n')
            self.online = False

    def connect(self):
        bin_sub_path = 'Bin\\Matrix.exe'
        library_sub_path = 'SDK\\RemoteAccess\\RemoteAccess_API.dll'
        name = os.path.basename(bin_sub_path)
        ok = False
        ps = psutil.process_iter()
        p = next(ps)
        go = True
        while go and not ok:
            try:
                p_path = p.exe()
                p_name = p.name()
            except:
                p_path = ''
                p_name = ''
            if p_name == name:
                installation_directory = p_path[:-(len(bin_sub_path) + 1)]
                library_path = os.path.join(installation_directory,
                                            library_sub_path)
                ok = os.path.exists(library_path)
            try:
                p = next(ps)
            except StopIteration:
                go = False
        ps.close()
        co = ''
        if ok:
            try:
                pe = pefile.PE(p_path)
                if pe.FILE_HEADER.Machine != self.machine:
                    self.log.AppendText('Bit architecture mismatch.\n')
                    pe.close()
                    pe = None
            except:
                pe = None
            if hasattr(pe, 'FileInfo') and pe.FileInfo:
                if isinstance(pe.FileInfo[0], list):
                    file_info = pe.FileInfo[0]
                else:
                    file_info = pe.FileInfo
                entries = [i for i in file_info if hasattr(i, 'StringTable')]
                if entries:
                    st_entries = [i for i in entries[0].StringTable]
                    if st_entries:
                        co = st_entries[0].entries[b'CompanyName'].decode()
                pe.close()
        if co:
            user_config_dir = os.environ['APPDATA']
            all_default_paths = natsort.natsorted(os.listdir(f"{user_config_dir}\\{co}\\MATRIX"))
            exp_sub_path = f'MATRIX\\{all_default_paths[-1]}\\Experiments'
            self.experiments_directory = os.path.join(user_config_dir, co,
                                                      exp_sub_path)
            self.lib_mate = ctypes.cdll.LoadLibrary(library_path)
            self.lib_mate.setHost(b'localhost')
            self.disconnect()
            if self.is_ran_down or self.testmode:
                rc = self.lib_mate.init(installation_directory.encode())
                self.log.AppendText('Connecting to the MATRIX, response: ' +
                                    self.rc_key(rc) + '.\n')
                if (rc == self.rcs['RMT_SUCCESS']) or self.testmode:
                    self.is_ran_down = False
                    self.experiment()
                    if not self.online:
                        self.disconnect()
                    else:
                        self.rc = self.rcs['RMT_SUCCESS']
                else:
                    self.rc = rc
        else:
            self.log.AppendText('Connecting to the MATRIX, response: '
                                '---.\n')

    def disconnect(self):
        if not self.is_ran_down:
            rc = self.lib_mate.rundown()
            self.log.AppendText('Disconnecting from the MATRIX, response: ' +
                                self.rc_key(rc) + '.\n')
            self.is_ran_down = (rc == self.rcs['RMT_SUCCESS'])
            self.online = False
            self.rc = rc
