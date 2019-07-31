import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nOmicron-Oliver-Gordon",
    version="1.0.0",
    author="Oliver Gordon",
    author_email="oliver.gordon@nottingham.ac.uk",
    description="Python Controls for Scienta Omicron Matrix",
    long_description="nOmicron package/API for automatically control of Matrix through Python",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: Microsoft :: Windows",
    ],
)