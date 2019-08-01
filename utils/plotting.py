# Oliver Gordon, 2019
import matplotlib.pyplot as plt
from matplotlib import colors
from mate import objects as mo
from matplotlib_scalebar.scalebar import ScaleBar

_nanomap_dict = {'red': ((0.0, 0.0, 0.0),
                   (0.5, 1.0, 1.0),
                   (1.0, 1.0, 1.0)),
           'green': ((0.0, 0.0, 0.0),
                     (1.0, 1.0, 1.0)),
           'blue': ((0.0, 0.0, 0.0),
                    (0.5, 0.0, 0.0),
                    (1.0, 1.0, 1.0))}  # As defined by SPIW
nanomap = colors.LinearSegmentedColormap('Nanomap', _nanomap_dict)

def plot_xy(xydata, title=None, pixel_scale=None):
    """Takes the CURRENT values from Matrix for the scalebar."""
    plt.figure()
    plt.imshow(xydata, cmap=nanomap)

    plt.axis('off')
    plt.colorbar()
    if pixel_scale is not None:
        plt.gca().add_artist(ScaleBar(pixel_scale, units="nm"))
    plt.title(title)

    plt.show()
