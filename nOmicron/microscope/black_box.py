import subprocess
from time import sleep

import backoff
import requests
from bs4 import BeautifulSoup

from nOmicron.utils.errors import MatrixUnsupportedOperationError

BLACK_BOX_IP = "10.0.42.2"

if "Received = 1" not in subprocess.check_output(f"ping {BLACK_BOX_IP} -n 1", shell=True).decode("utf-8"):
    raise MatrixUnsupportedOperationError("Remote black box control is unavailable in this hardware configuration. \n"
                                          f"Check that {BLACK_BOX_IP} can be loaded")


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
def _wait_for_approach():
    while True:
        output = requests.get(f"http://{BLACK_BOX_IP}")
        soup = BeautifulSoup(output.text, 'html.parser')
        display_text = soup.find("textarea")

        if "ANY KEY STOPS" not in display_text.contents[0]:
            break
        else:
            sleep(0.5)


@backoff.on_exception(backoff.expo,
                      requests.exceptions.RequestException)
def _press_button(button_name):
    requests.get(f"http://{BLACK_BOX_IP}?{button_name}={button_name}")


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
    _wait_for_approach()
