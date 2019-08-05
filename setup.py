from setuptools import setup, find_packages

setup(
    name='nOmicron',
    version='1.0.0',
    url='https://github.com/OGordon100/nOmicron',
    license='GPL v3.0',
    author='Oliver Gordon',
    author_email='oliver.gordon@nottingham.ac.uk',
    description="Python Controls for Scienta Omicron Matrix",
    long_description="nOmicron package/API for automatically control of Matrix through Python",
    packages=find_packages(),
    install_requires=['numpy', 'tqdm', 'matplotlib'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows"]
)
