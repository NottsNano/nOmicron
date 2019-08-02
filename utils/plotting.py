# Oliver Gordon, 2019
import matplotlib.pyplot as plt
from matplotlib import colors
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

    def plot(data, dir):
        plt.figure()
        plt.imshow(data, cmap=nanomap)

        plt.axis('off')
        plt.colorbar()
        if pixel_scale is not None:
            plt.gca().add_artist(ScaleBar(pixel_scale, units="nm"))
        if title is not None:
            plt.title(f"{title} {dir}")

    if len(xydata) == 2:
        plot(xydata[0], dir="Up")
        plot(xydata[1], dir="Down")
    else:
        plot(xydata, dir="Up")

    plt.show()


def plot_linear_signal(x, y, channel=None, title=None):
    """Plots a linear signal or set of spectroscopy curves, such as I(t) or I(V)"""

    fig = plt.figure()
    if isinstance(y, list):
        plt.close(fig)
        fig, axes = plt.subplots(nrows=len(y), ncols=1, sharex=True, sharey=True)
        for repeat in range(len(y)):
            if isinstance(y[0], list):
                axes[repeat].plot(x, y[repeat][0], 'green')
                axes[repeat].plot(x, y[repeat][1], 'gold')
                fig.legend(['Forward', 'Back'])
            else:
                axes[repeat].plot(x, y[repeat], 'green')
    else:
        plt.plot(x, y, 'green')

    if title is not None:
        plt.title(title)

    if channel is not None:
        plt.xlabel(channel[2])
        plt.ylabel(channel[0])
