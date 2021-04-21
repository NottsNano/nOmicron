from setuptools import setup, find_packages

setup(
    name='nOmicron',
    version='1.6.1',
    url='https://github.com/OGordon100/nOmicron',
    license='GPL v3.0',
    author='Oliver Gordon',
    author_email='oliver.gordon@nottingham.ac.uk',
    description="Python Control for Scienta Omicron Matrix",
    long_description="nOmicron package/API to automatically control Matrix through Python",
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'tqdm', 'matplotlib', 'natsort', 'pefile', 'psutil', 'selenium', 'chromedriver_autoinstaller', 'bs4', 'lxml'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows"]
)
