# nOmicron


### About

Python API for interacting with Scienta Omicron Matrix (via the MATE scripting language).

A fork of Stephan Zevenhuizen's [MATE-for-Dummies](https://pypi.org/project/MATE-for-Dummies/), 
nOmicron allows for simple, easily extensible control of Matrix and running of common routines, and 
without the need to ever touch Matrix or compile MATE scripts! 

All data channels are readable _**during experimentation**_, negating the need to finish experimenting and
converting from the proprietary .mtrx file formats.

The package has been verified to work with Matrix 4.3.5 and Python 3.6.3 and the STM 
Spectroscopy experiment window.

---

### Installation

Recommended method is to install from PyPi with ``pip install nOmicron``

---

### Citing

If you use nOmicron in your research, it would be appreciated if you could cite via the DOI in the badge

---

### Setting & Getting Parameters

After opening Matrix and initialising a connection to your SPM, initialise the code with

```
from nOmicron.microscope import IO
IO.connect
```

Experiment parameters are settable in their related packages. For example, you can 
change the scan position and angle, with
```
from nOmicron.microscope import xy_scanner
xy_scanner.set_scan_position(angle=10, xy_pos=[5e-9, 0])
```

It is also possible (but not preferable) to get and set parameters in the mate4dummies style, with
```
from nOmicron.mate import objects as mo

mo.mate.xy_scanner.Angle()    # Get the angle
mo.mate.xy_scanner.Angle(10)  # Set the angle
mo.mate.xy_scanner.Area([5e-9, 0])  
```

Although any sent parameter is first verified to be within the tolerable parameters of the object, 
you can also manually check the allowed values with
```
from nOmicron.utils import read_min_max
min_max = read_min_max("xy_scanner", "Angle")
```

---

### Getting Live Data

Data can only be acquired in pre-defined chunks, due to technical limitations of MATE.
It is also not (yet) possible to acquire more than one data source at a time.

Pickable channels are those available in the ``Channel List`` window of Matrix. e.g
```
Z
I
Aux1
I(V)
I(Z)
Aux1(Z)
Z(t)
I(t)
```

Image channels can be captured and viewed on a line-by-line basis with 
```
from nOmicron.microscope.xy_scanner import get_xy_scan
from nOmicron.utils.plotting import plot_xy

xydata = get_xy_scan("Z", x_direction="forward", y_direction="up")
plot_xy(xydata, view_count, pixel_scale=mo.xy_scanner.Width() * 1e9 / mo.xy_scanner.Points())
```

Spectroscopy is performable with the ``microscope.continuous_spectroscopy.get_point_spectra`` function
```
from nOmicron.microscope.continuous_spectroscopy import get_point_spectra
V, I = get_point_spectra("I(V)", start_end=(0, 4), target_position=[0, 1],
                          repeats=2, sample_points=50, sample_time=10e-3, 
                          forward_back=True)
``` 

Time series data can be captured with the ``microscope.continuous_spectroscopy.get_continuous_signal`` function
```
from nOmicron.microscope.continuous_spectroscopy import get_continuous_signal
t, I = get_continuous_signal("I(t)", sample_time=2, sample_points=50)
```
For ease of use, common routines are abstracted from the underlying MATE code

---
### Adding core MATE functions

Anything doable with MATE is doable in nOmicron. Individual elements can be determined from the
Matrix window by selecting the ↖❓ button and clicking on a changeable element, or with the the MATE documentation in
``Tools -> Manage Scripts -> Help -> Script Documentation``.

For example, the ``Points`` parameter of the ``XY Scanner`` window has:

``Experiment Element``: `XYScanner`
``Parameter Name``: ``Points``
``Type``: ``boolean``

We now go to mate.objects.py and look for the ``Class`` ``_XYScanner`` and make
a ``function`` called ``Points``, following the template from the other functions.

If we want to make a whole new ``Experiment Element``, we can make this with a similar Class
beginning with ``_``, and then initialising it with ``name()`` at the bottom of the file.

If you do this, please submit a pull request :)