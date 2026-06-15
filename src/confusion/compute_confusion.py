# HEADER
import math
import numpy as np


def _logistic(x, alpha=1.0, beta=None):
    """
    Logistic psychometric function.

    Parameters
    ----------
    x : float
        Distance value (in JND units ideally)
    alpha : float
        Threshold parameter (location, default = 1 JND)
    beta : float or None
        Slope parameter. If None, set to log(3) so that P=0.5 at x=alpha.

    Returns
    -------
    float
        Probability (confusion)
    """
    
    if beta is None:
        beta = np.log(3)

    # symmetric rule: below threshold -> chance level
    if x < alpha:
        return 0.5

    return 1 / (1 + math.exp(beta * (x - alpha)))


def distance_to_confusion(distance_matrix, method="logistic", **kwargs):
    """
    Convert a distance matrix into a confusion probability matrix.

    Parameters
    ----------
    distance_matrix : dict
        Nested dict {stim1: {stim2: distance}}
    method : str
        Psychometric function to use ("logistic", "weibull", "gaussian", etc.)
    **kwargs :
        Parameters for the psychometric function

    Returns
    -------
    dict
        Confusion probability matrix {stim1: {stim2: prob}}
    """

    # Select mapping function
    if method == "logistic":
        func = lambda x: _logistic(x, **kwargs)

    elif method == "linear":
        # simple baseline (for debugging)
        func = lambda x: min(1.0, max(0.0, 1 - x))

    elif method == "exponential":
        func = lambda x: math.exp(-x)

    else:
        raise ValueError(f"Unknown method '{method}'")

    # Apply transformation
    confusion_matrix = {}

    for s1 in distance_matrix:
        confusion_matrix[s1] = {}
        for s2 in distance_matrix[s1]:
            d = distance_matrix[s1][s2]
            
            confusion_matrix[s1][s2] = func(d)

    return confusion_matrix
