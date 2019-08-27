from nOmicron.mate import objects as mo

mo.pll.PLL_Enable(True)


def enable_pll():
    mo.pll.PLL_Enable(True)


def disable_pll():
    mo.pll.PLL_Enable(False)


def is_pll_locked():
    """Check if the PLL is locked"""
    return mo.pll.PLL_Locked()


def set_attenutation_level(attenuation):
    """
    Set the attenuation level

    Parameters
    ----------
    attenuation : int
        The level of attenuation from 0-4 (corresponds to 0, 0.1, 0.01, 0.001).
    """
    if mo.pll.Non_Contact_Mode() == 0:
        mo.pll.Excitation_Attenuation_Constant_Amplitude(attenuation)
    elif mo.pll.Non_Contact_Mode() == 1:
        mo.pll.Excitation_Attenuation_Constant_Excitation(attenuation)
    elif mo.pll.Non_Contact_Mode() == 2:
        mo.pll.Excitation_Attenuation_Self_Excitation(attenuation)


def set_loop_gain(I, P, method='new'):
    """Sets the loop gain"""

    if method == 'new':
        mo.pll.PLL_Loop_Gain_I(I)
        mo.pll.PLL_Loop_Gain_P(P)
    else:
        if mo.pll.Non_Contact_Mode() == 0:
            mo.pll.Amplitude_Loop_Gain_I_Constant_Amplitude(I)
            mo.pll.Amplitude_Loop_Gain_P_Constant_Amplitude(P)
        elif mo.pll.Non_Contact_Mode() == 1:
            raise BlockingIOError("Cannot set loop gain for constant excitation PLL mode")
        elif mo.pll.Non_Contact_Mode() == 2:
            mo.pll.Amplitude_Loop_Gain_I_Self_Excitation(I)
            mo.pll.Amplitude_Loop_Gain_P_Self_Excitation(P)
