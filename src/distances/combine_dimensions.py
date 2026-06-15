import math

def compute_global_distance(distance_matrices: dict, weights: dict) -> dict:
    """
    Combine per-dimension distances into a global distance matrix.

    Parameters
    ----------
    distance_matrices : dict
        {dimension: {stim1: {stim2: distance}}}
    weights : dict
        {dimension: weight}

    Returns
    -------
    dict
        Global distance matrix
    """


    if not distance_matrices:
        raise ValueError("Empty distance matrices")

    if not weights:
        raise ValueError("Empty weights")

    first_dim = next(iter(distance_matrices))
    signals = sorted(list(distance_matrices[first_dim].keys()))

    distance_matrix = {s1: {} for s1 in signals}

    for s1 in signals:
        for s2 in signals:
            value = 0.0

            for dim, matrix in distance_matrices.items():

                # Fix name_distance WITHOUT changing key
                if dim == "name_distance":
                    matrix = matrix["global"]

                # STRICT check (important)
                if dim not in weights:
                    raise ValueError(f"Missing weight for dimension: {dim}")
                    weights[dim] = 0
                    
                w = float(weights[dim])
                d = float(matrix[s1][s2])

                value += (w * d) ** 2
                
            distance_matrix[s1][s2] = math.sqrt(value)

    return distance_matrix
