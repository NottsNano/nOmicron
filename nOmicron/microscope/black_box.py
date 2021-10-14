import subprocess
from urllib import request

from nOmicron.utils.errors import MatrixUnsupportedOperationError

BLACK_BOX_IP = "10.0.42.2"

if "Received = 1" not in subprocess.check_output(f"ping {BLACK_BOX_IP} -n 1", shell=True).decode("utf-8"):
    raise MatrixUnsupportedOperationError("Remote black box control is unavailable in this hardware configuration. \n"
                                          f"Check that {BLACK_BOX_IP} can be loaded")


def _press_button(button_name):
    request.urlopen(f"{BLACK_BOX_IP}?{button_name}={button_name}")


def x_plus():
    _press_button("F1p")


def x_minus():
    _press_button("F1m")


def y_plus():
    _press_button("F2p")


def y_minus():
    _press_button("F2m")


def z_plus():
    _press_button("F3p")


def z_minus():
    _press_button("F3m")


def up():
    _press_button("UP")


def down():
    _press_button("DOWN")


def fx():
    _press_button("FX")


def backward():
    _press_button("BWD")


def forward():
    _press_button("FWD")


def auto_approach():
    _press_button("AUTO")
