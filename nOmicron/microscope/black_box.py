from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
import subprocess

from nOmicron.utils.errors import MatrixUnsupportedOperationError

if "Received = 1" not in subprocess.check_output("ping 10.0.42.2 -n 1", shell=True).decode("utf-8"):
    raise MatrixUnsupportedOperationError("Remote black box control is unavailable in this hardware configuration. \n"
                                          "Check that http://10.0.42.2 can be loaded")
chromedriver_autoinstaller.install()

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)
driver.get("http://10.0.42.2/")


def x_plus():
    driver.find_element_by_name("F1p").click()


def x_minus():
    driver.find_element_by_name("F1m").click()


def y_plus():
    driver.find_element_by_name("F2p").click()


def y_minus():
    driver.find_element_by_name("F2m").click()


def z_plus():
    driver.find_element_by_name("F3p").click()


def z_minus():
    driver.find_element_by_name("F3m").click()


def up():
    driver.find_element_by_name("UP").click()


def down():
    driver.find_element_by_name("DOWN").click()


def fx():
    driver.find_element_by_name("FX").click()


def backward():
    driver.find_element_by_name("BWD").click()


def forward():
    driver.find_element_by_name("FWD").click()


def auto_approach():
    driver.find_element_by_name("AUTO").click()


def auto_approach():
    driver.find_element_by_name("AUTO").click()
