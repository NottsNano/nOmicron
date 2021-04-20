# Oliver Gordon, 2019

from nOmicron.mate import objects as mo

# from selenium import webdriver
# import chromedriver_autoinstaller
#
#
# chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
#                                       # and if it doesn't exist, download it automatically,
#                                       # then add chromedriver to path
#
# driver = webdriver.Chrome()
# driver.get("http://www.python.org")

def set_gap_voltage(voltage):
    mo.gap_voltage_control.Voltage(voltage)


def approach(v_gap, cautiousness):
    modes = {"Super Cautious": {"Loop_Gain_I": 3, "I_Setpoint": 50e-12},
             "Cautious": {"Loop_Gain_I": 3, "I_Setpoint": 50e-12},
             "Normal": {"Loop_Gain_I": 3, "I_Setpoint": 50e-12},
             "YOLO": {"Loop_Gain_I": 3, "I_Setpoint": 50e-12}}

    mo.regulator.Preamp_Range_1(0)
    mo.regulator.Loop_Gain_1_I(modes[cautiousness["Loop_Gain_I"]])
    mo.regulator.Setpoint_1(modes[cautiousness["I_Setpoint"]])
    mo.gap_voltage_control.Voltage(v_gap)

    print("Ready to beginning approach...")
    while not mo.regulator.Setpoint_Detected():
        pass
    print("Approach finished.")
