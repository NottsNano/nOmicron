# Oliver Gordon, 2019
import matplotlib.pyplot as plt
from matplotlib import colors

_nanomap_dict = {'red': ((0.0, 0.0, 0.0),
                   (0.5, 1.0, 1.0),
                   (1.0, 1.0, 1.0)),
           'green': ((0.0, 0.0, 0.0),
                     (1.0, 1.0, 1.0)),
           'blue': ((0.0, 0.0, 0.0),
                    (0.5, 0.0, 0.0),
                    (1.0, 1.0, 1.0))}  # As defined by SPIW
nanomap = colors.LinearSegmentedColormap('Nanomap', _nanomap_dict)

def plot_xy(xydata):
    plt.figure()
    plt.imshow(xydata, cmap=nanomap)
    plt.axis('off')
    plt.colorbar()
    plt.show()
