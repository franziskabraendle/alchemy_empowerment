import random
import warnings

import numpy as np
import scipy.special
from sklearn import preprocessing
from scipy import stats

def softmax(x, temperature=1):
    """Applies softmax on a given list considering a temperature value. Softmax is applied row-wise if list is 2D.

    Args:
        x (ndarray(dtype=float, ndim=2) or dict_values): Array with values. Can be 1D or 2D.
        temperature (float, optional): Temperature that is applied to softmax.
                    A temperature > 1 produces a softer probability distribution and < 1 a probability distribution twords argmax.
                    Defaults to 1.

    Returns:
        ndarray(dtype=float, ndim=2): Probabilities row-wise.
    """
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")

        if not isinstance(x, np.ndarray):
            x = list(x)
            x = np.array(x)

        if x.ndim == 2:
            x = preprocessing.scale(x, axis=1)
            x_temperature = x/temperature
            probabilities = scipy.special.softmax(x_temperature, axis=1)
        else:
            x = preprocessing.scale(x)
            x_temperature = x/temperature
            probabilities = scipy.special.softmax(x_temperature)

        return probabilities

def split_numbers(n_elements, split):
    """Splits elements into groups of (nearly) equal size.

    Args:
        n_elements (int): Number of elements that have to be split.
        n_splits (int): Number of splits.

    Returns:
        (ndarray(dtype=int, ndim=2)): Array that contains multiple sub-arrays of (nearly) equal size filled with element indices.
    """
    x = np.arange(n_elements)
    random.shuffle(x)

    return np.array_split(x, split)

def jsonKeys2int(x):
    """Casts str keys to int.

    Args:
        x (dict): Dictionary with str keys.

    Returns:
        dict: Dictionary with int keys.
    """
    if isinstance(x, dict):
        return {int(k):v for k,v in x.items()}

    return x

def translate_empowerment_calculation(empowerment_calculation):
    """Maps empowerment calculation bool values to str.

    Args:
        empowerment_calculation (tuple): Tuple made of three entries.
                    - dynamic (bool): Whether calculation of empowerment is done dynamically or static.
                    - local (bool): Whether calculation of empowerment is done locally or globally.
                    - outgoing_combinations (bool): Whether calculation of empowerment is done on outgoing combinations
                                or length of set of resulting elements.

    Returns:
        tuple: Tuple made up of mapped empowerment calculation.
    """
    translation = tuple()
    if empowerment_calculation[0] is True:
        translation += ('dynamic',)
    else:
        translation += ('static',)
    if empowerment_calculation[1] is True:
        translation += ('local',)
    else:
        translation += ('global',)
    if empowerment_calculation[2] is True:
        translation += ('outgoing combinations',)
    else:
        translation += ('children',)

    return translation

def translate_model(model_type):
    """Maps model shortcut to full name.

    Args:
        model_type (str): Model shortcut.

    Returns:
        str: Model full name.
    """
    if model_type == 'base':
        model = 'random'
    elif model_type == 'cbu':
        model = 'uncertainty'
    elif model_type == 'cbv':
        model = 'CBV'
    elif model_type == 'sim':
        model = 'similarity'
    elif model_type == 'bin':
        model = 'success (approx.)'
    elif model_type == 'truebin':
        model = 'oracle'
    elif model_type == 'emp':
        model = 'empowerment (approx.)'
    elif model_type == 'trueemp':
        model = 'empowerment'
    else:
        raise ValueError('Undefined model version: "{}". Use "base", "cbv",\
                "cbu", "sim", "bin", "emp", "truebin" or "trueemp" instead.'.format(model_type))

    return model

def translate_subset_type(subset_type):
    """Maps subset shortcut to full name.

    Args:
        subset_type (str): Subset shortcut.

    Returns:
        str: Subset full name.
    """
    if subset_type == 'max':
        model = 'best'
    elif subset_type == 'random':
        model = 'random'
    elif subset_type == 'min':
        model = 'worst'
    else:
        raise ValueError('Undefined model version: "{}". Use "max", "min" or\
                "random" instead.'.format(subset_type))

    return model

def adjust_lightness(color, amount=0.5):
    """Function to lighten or darken given color by multiplying (1-luminosity) by the given amount.
                Taken from https://stackoverflow.com/questions/37765197/darken-or-lighten-a-color-in-matplotlib

    Args:
        color (str): Color can be matplotlib color string, hex string, or RGB tuple.
        amount (float, optional): If smaller than 1, color will be darker. If higher than 1, color will be lighter.
                Defaults to 0.5.

    Returns:
        tuple: Color RGB tuple.
    """
    import colorsys

    import matplotlib.colors as mc
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

def pearsonr_ci(x,y,alpha=0.05):
    'taken from github.com/zhiyzuo/pearsonr_ci.py'
    ''' calculate Pearson correlation along with the confidence interval using scipy and numpy
    Parameters
    ----------
    x, y : iterable object such as a list or np.array
      Input for correlation calculation
    alpha : float
      Significance level. 0.05 by default
    Returns
    -------
    r : float
      Pearson's correlation coefficient
    pval : float
      The corresponding p value
    lo, hi : float
      The lower and upper bound of confidence intervals
    '''

    r, p = stats.pearsonr(x,y)
    r_z = np.arctanh(r)
    se = 1/np.sqrt(x.size-3)
    z = stats.norm.ppf(1-alpha/2)
    lo_z, hi_z = r_z-z*se, r_z+z*se
    lo, hi = np.tanh((lo_z, hi_z))
    return r, p, lo, hi
