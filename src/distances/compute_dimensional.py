# HEADER
import math
import re
import Levenshtein


def compute_dimensional_distances(stimuli, jnd):
    """
    Compute pairwise distances per dimension using JND normalization.

    Parameters
    ----------
    stimuli : dict
        Parsed stimulus description
    jnd : dict
        JND configuration

    Returns
    -------
    dict
        {dimension_name: distance_matrix}
    list
        [categories]
    """
    
    # TBD

    paths = list(extract_structure_paths(stimuli))
    categories = sorted(find_signal_groups(paths))

    results = {}

    for cat in categories:
        n = len(cat.split(".")) + 1

        dimensions = list(set([
            ".".join(p.split(".")[n:-1])
            for p in paths
            if (p.endswith(".Value") or p.endswith(".Unit")) and p.startswith(cat)
        ]))

        signals = sorted(list(set([
            ".".join(p.split(".")[n-1:n])
            for p in paths
            if (p.endswith(".Value") or p.endswith(".Unit")) and p.startswith(cat)
        ])))

        cat_key = ".".join(cat.split(".")[1:])
        
        container = stimuli if cat_key == "" else stimuli[cat_key]
        
        if cat_key != "":
            results[cat_key] = {}

        for dimension in dimensions:
            dim_keys = dimension.split(".")

            values = {}
            units = []

            for signal in signals:
                val = get_nested(container, [signal] + dim_keys + ["Value"])
                unit = get_nested(container, [signal] + dim_keys + ["Unit"])

                values[signal] = float(val)
                units.append(unit)

            if len(set(units)) != 1:
                raise ValueError(f"Unit mismatch in dimension {dimension}")
           
            jnd_value, jnd_unit, _ = get_jnd_for_dimension(jnd, dim_keys)

            matrix = {}

            for s1 in signals:
                matrix[s1] = {}
                for s2 in signals:
                    matrix[s1][s2] = compute_distance(
                        values[s1], values[s2], jnd_value, jnd_unit
                    )

            if cat_key != "":
                results[cat_key][dimension] = matrix
            else :
                results[dimension] = matrix

    # Optional: add Levenshtein
    namesList = list(path for path in paths if (path.endswith('.Name') and path.startswith(cat)))
    if namesList :
        results["name_distance"] = compute_name_distances(stimuli, categories)


    # Drop the dot
    categories = [categorie[1:] if categorie.startswith('.') else categorie for categorie in categories]
    return results, categories

    
    

def compute_distance(val1, val2, jnd_value, jnd_unit):
    """
    Compute distance between two values using JND normalization.

    Parameters
    ----------
    val1, val2 : float
        Physical parameter values
    jnd_value : float
        JND threshold value
    jnd_unit : string
        JND threshold unit

    Returns
    -------
    float
        distance
    """
    delta = abs(val1 - val2)

    if delta == 0:
        distance = 0
    
    else :

        if jnd_unit != "%":
            distance = delta / jnd_value
        else:
            jnd_value = jnd_value / 100
            distance = (delta / max(val1, val2)) / jnd_value
            
    return distance
    
    
def extract_structure_paths(data, prefix=""):
    """Flatten JSON structure into dot paths with leading dot."""
    if isinstance(data, dict):
        for key, value in data.items():
            path = f"{prefix}.{key}"  # always builds with leading "."
            yield path
            yield from extract_structure_paths(value, path)
                

def find_signal_groups(paths):
    """Find categories containing SignalX."""
    cats = [p for p in paths if re.search(r"Signal\d+$", p)]
    return list(set([".".join(cat.split(".")[:-1]) for cat in cats]))
    
    

def get_nested(data, keys):
    for k in keys:
        data = data[k]
    return data


def compute_name_distances(stimuli, categories):
    """Compute Levenshtein distance between stimulus names."""
    output = {}

    for cat in categories:
        signals = stimuli if cat == "" else stimuli[cat]

        names = {k: v["Name"] for k, v in signals.items() if "Name" in v}

        matrix = {}
        for s1 in names:
            matrix[s1] = {}
            for s2 in names:
                matrix[s1][s2] = Levenshtein.distance(names[s1], names[s2])

        output[cat or "global"] = matrix

    return output


def get_jnd_for_dimension(jnd, dimension_keys):
    # Check dimension to ID modality and dimension (frequency, itensity...)
    
    modality = dimension_keys[0] # granted that Li and Sand are fixed
    
    jnd_dimensions = jnd[modality]
    
    for dim in dimension_keys:
        for jnd_key in jnd_dimensions.keys():
            if jnd_key in dim:
                jnd_name = modality + "." + jnd_key
                return jnd_dimensions[jnd_key]["Value"], jnd_dimensions[jnd_key]["Unit"], jnd_name
    
    print(f"WARNING: Dimension is {dimension_keys} \nbut the JND file as the following keys:\n{jnd.keys()} ")
    raise ValueError(f"No JND found for {dimension_keys}")



