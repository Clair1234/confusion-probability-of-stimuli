# HEADER
import numpy as np
from scipy.spatial import procrustes
from scipy import stats
from scipy.stats import pearsonr, spearmanr
from scipy.special import rel_entr
import math
from itertools import permutations


def descriptive_statistics(prediction, reference) :
    # Flatten
    flat_prediction = []
    flat_reference = []
    for key1 in prediction.keys():
        for key2 in prediction[key1].keys():
            flat_prediction.append(prediction[key1][key2])
            flat_reference.append(reference[key1][key2])
    
    # Average
    mean_reference = np.mean(reference)
    mean_prediction = np.mean(prediction)
    print("\nAverage probability:")
    print(f"    Reference: {mean_reference:.3f}")
    print(f"    Prediction: {mean_prediction:.3f}")
    
    # STE
    ste_reference = stats.sem(flat_reference)
    ste_prediction = stats.sem(flat_prediction)
    print("\nStandard error:")
    print(f"    Reference: {ste_reference:.3f}")
    print(f"    Prediction: {ste_prediction:.3f}")
    
    # Median
    median_reference = np.median(flat_reference)
    median_prediction = np.median(flat_prediction)
    print("\nMeadian value:")
    print(f"    Reference: {median_reference:.3f}")
    print(f"    Prediction: {median_prediction:.3f}")
    
    # STD
    std_reference =  np.std(flat_reference)
    std_prediction = np.std(flat_prediction)
    print("\nStandard deviation:")
    print(f"    Reference: {std_reference:.3f}")
    print(f"    Prediction: {std_prediction:.3f}")
    
    # Var
    var_reference =  np.var(flat_reference)
    var_prediction = np.var(flat_prediction)
    print("\nVariance:")
    print(f"    Reference: {var_reference:.3f}")
    print(f"    Prediction: {var_prediction:.3f}")
    
    # Range
    min_reference = min(flat_reference)
    max_reference = max(flat_reference)
    range_reference = max_reference - min_reference
    min_prediction = min(flat_prediction)
    max_prediction = max(flat_prediction)
    range_prediction = max_prediction - min_prediction
    print("Range:")
    print(f"    Reference: {range_reference:.3f}: [{min_reference}, {max_reference}]")
    print(f"    Prediction: {range_prediction:.3f}: [{min_prediction}, {max_prediction}]")
    
    # Number of values
    n_reference = len(flat_reference)
    n_prediction = len(flat_prediction)
    print("\nNumber of samples:")
    print(f"    Reference: {n_reference:.3f}")
    print(f"    Prediction: {n_prediction:.3f}")
    
    return 0
    
    
def bootstrap_correlation(reference, prediction, n_bootstrap=1000, exclude_diag=True):
    """
    Confidence interval on correlation
    """
    
    # Conversion into numpy array
    M_pred = prediction.values
    M_emp = reference.values
    
    assert M_pred.shape == M_emp.shape, "Matrices must have same size"
    N = M_pred.shape[0]
    
    # Exclude diagonal
    if exclude_diag:
        mask = ~np.eye(N, dtype=bool)
        pred_vals = M_pred[mask]
        emp_vals = M_emp[mask]
    else:
        pred_vals = M_pred.flatten()
        emp_vals = M_emp.flatten()
        
    n_values = len(pred_vals)
    
    # Correlation
    r, p_value = pearsonr(pred_vals, emp_vals)
    #rho, _ = spearmanr(pred_vals, emp_vals)
    
    rho, rho_p, rho_perm = spearman_permutation_pvalue(
        pred_vals, emp_vals, n_perm=9999
    )

    
    # Bootstrap
    r_bootstrap = []
    rho_bootstrap = []
    
    np.random.seed(42)
    for _ in range(n_bootstrap):
        indices = np.random.choice(n_values, size=n_values, replace=True)
        
        pred_sample = pred_vals[indices]
        emp_sample = emp_vals[indices]
        
        # Correlation
        r_boot, _ = pearsonr(pred_sample, emp_sample)
        rho_boot, _ = spearmanr(pred_sample, emp_sample)
        
        r_bootstrap.append(r_boot)
        rho_bootstrap.append(rho_boot)
        
        
    r_ci_low = np.percentile(r_bootstrap, 2.5)
    r_ci_high = np.percentile(r_bootstrap, 97.5)
    
    rho_ci_low = np.percentile(rho_bootstrap, 2.5)
    rho_ci_high = np.percentile(rho_bootstrap, 97.5)
    
    # Standard deviation
    r_se = np.std(r_bootstrap)
    rho_se = np.std(rho_bootstrap)
    
    return {
        'pearson_r': r,
        'pearson_p': p_value,
        'pearson_ci_95': (r_ci_low, r_ci_high),
        'pearson_se': r_se,
        'spearman_rho': rho,
        'spearman_p': rho_p,
        'spearman_ci_95': (rho_ci_low, rho_ci_high),
        'spearman_se': rho_se,
        'n_values': n_values,
        'bootstrap_distributions': {
            'pearson': r_bootstrap,
            'spearman': rho_bootstrap
        } 
    }


def hellinger_distance(p, q):
    p = np.array(p, dtype=float)
    q = np.array(q, dtype=float)
    
    p = p / p.sum()
    q = q / q.sum()
    
    assert np.isclose(p.sum(), 1.0), f"p does not sum to 1: {p.sum()}"
    assert np.isclose(q.sum(), 1.0), f"q does not sum to 1: {q.sum()}"
    
    return np.sqrt(np.sum((np.sqrt(p) - np.sqrt(q))**2)) / np.sqrt(2)


def bootstrap_hellinger(prediction, reference, bins=999, n_perm=5000, seed=42):
    rng = np.random.default_rng(seed)
    
    # Flatten
    x = []
    y = []
    for key1 in prediction.keys():
        for key2 in prediction[key1].keys():
            x.append(prediction[key1][key2])
            y.append(reference[key1][key2])

    hx, _ = np.histogram(x, bins=bins)
    hy, _ = np.histogram(y, bins=bins)
    observed = hellinger_distance(hx, hy)

    pooled = np.concatenate([x, y])
    nx = len(x)

    null = np.empty(n_perm)
    for i in range(n_perm):
        perm = rng.permutation(pooled)
        hx_p, _ = np.histogram(perm[:nx], bins=bins)
        hy_p, _ = np.histogram(perm[nx:], bins=bins)
        null[i] = hellinger_distance(hx_p, hy_p)

    p_val = (np.sum(null >= observed) + 1) / (n_perm + 1)
    return observed, p_val


def kl_divergence(p, q, eps=1e-12):
    p = np.array(p, dtype=float) + eps
    q = np.array(q, dtype=float) + eps
    norm_p = p / p.sum()
    norm_q = q / q.sum()
    return np.sum(rel_entr(p, q))
    
    
def js_divergence(prediction, reference):
    # Flatten
    x = []
    y = []
    for key1 in prediction.keys():
        for key2 in prediction[key1].keys():
            x.append(prediction[key1][key2])
            y.append(reference[key1][key2])
            
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    m = 0.5 * (x + y)
    return 0.5 * kl_divergence(x, m) + 0.5 * kl_divergence(y, m)


def mantel_structure_test(m1, m2, eps=1e-12, n_perm_random=9999, seed=42, exact_threshold=10000):

    rng = np.random.default_rng(seed)
    signals = sorted(set(m1.keys()) & set(m2.keys()))
    n = len(signals)

    # insure correct unwrap - ok
    a1 = dict_to_array(m1, signals)
    a2 = dict_to_array(m2, signals)
    
    # check for 0 values -> change to eps - ok
    # ref: Martín-Fernández, J. A., Barceló-Vidal, C., & Pawlowsky-Glahn, V. (2003). Dealing with zeros and missing values in compositional data sets using nonparametric imputation. Mathematical Geology, 35(3), 253-278.
    a1 = impute(a1, eps)
    a2 = impute(a2, eps)
    idx = np.triu_indices(n, k=1)
    
    d1 = hellinger_distance_matrix(a1)
    d2 = hellinger_distance_matrix(a2)

    # Observed statistic
    v1 = d1[idx]
    v2 = d2[idx]
    r_obs, _ = pearsonr(v1, v2)

    # Decide exact vs random
    n_fact = math.factorial(n)

    if n_fact <= exact_threshold:
        perm_iter = permutations(range(n))
        n_perm = n_fact
    else:
        perm_iter = (rng.permutation(n) for _ in range(n_perm_random))
        n_perm = n_perm_random

    perm_r = np.empty(n_perm)

    for b, perm_idx in enumerate(perm_iter):
        perm_idx = list(perm_idx)
        d2_perm = d2[np.ix_(perm_idx, perm_idx)]
        v2_perm = d2_perm[idx]
        perm_r[b], _ = pearsonr(v1, v2_perm)

    # Phipson & Smyth correction
    ## ref: Phipson, B., & Smyth, G. K. (2016). Permutation P-values should never be zero: calculating exact P-values when permutations are randomly drawn. arXiv preprint arXiv:1603.05766.
    p_val = (np.sum(np.abs(perm_r) >= np.abs(r_obs)) + 1) / (n_perm + 1)

    return r_obs, p_val


def impute(matrix, epsilon=1e-12):
    # TRIPLE CHECK
    # ref: Martín-Fernández, J. A., Barceló-Vidal, C., & Pawlowsky-Glahn, V. (2003). Dealing with zeros and missing values in compositional data sets using nonparametric imputation. Mathematical Geology, 35(3), 253-278.
    ## eq 3
    imputed = matrix.copy().astype(float)
    for i in range(imputed.shape[0]):
        row = imputed[i]
        zero_mask = row < epsilon
        if not zero_mask.any():
            continue
        n_zeros = zero_mask.sum()
        delta = epsilon
        # scale non-zero parts down to make room for the zero replacements
        row[~zero_mask] *= (1.0 - n_zeros * delta) / row[~zero_mask].sum()
        row[zero_mask] = delta
        imputed[i] = row
    return imputed


def procrustes_pvalue(reference, prediction, n_perm=9999, random_state=42):
    rng = np.random.default_rng(random_state)
    
    X = reference.values
    Y = prediction.values
    
    _, _, D_obs = procrustes(X, Y)
    
    D_perm = np.empty(n_perm)
    for i in range(n_perm):
        idx = rng.permutation(Y.shape[0])
        _, _, D_perm[i] = procrustes(X, Y[idx])
    
    p_value = (np.sum(D_perm <= D_obs) + 1) / (n_perm + 1)
    return D_obs, p_value, D_perm


def spearman_permutation_pvalue(x, y, n_perm=9999, seed=42):
    rng = np.random.default_rng(seed)

    rho_obs, _ = spearmanr(x, y)

    rho_perm = np.empty(n_perm)
    for i in range(n_perm):
        y_perm = rng.permutation(y)
        rho_perm[i], _ = spearmanr(x, y_perm)

    # test bilatéral
    p_val = (np.sum(np.abs(rho_perm) >= np.abs(rho_obs)) + 1) / (n_perm + 1)
    return rho_obs, p_val, rho_perm

def dict_to_array(M, labels):
    return np.array([[M[s1][s2] for s2 in labels] for s1 in labels])


def hellinger_distance_matrix(matrix: np.ndarray) -> np.ndarray:
    # ref: González-Castro, V., Alaiz-Rodríguez, R., & Alegre, E. (2013). Class distribution estimation based on the Hellinger distance. Information Sciences, 218, 146-164.
    
    row_sums = matrix.sum(axis=1)
    assert np.allclose(row_sums, 1), "Rows must sum to 1 (probability distributions)"

    sq = np.sqrt(matrix)           # square-root transform
    n = sq.shape[0]
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            diff = sq[i] - sq[j]
            dist = np.sqrt(np.dot(diff, diff)) / np.sqrt(2)
            D[i, j] = dist
            D[j, i] = dist
    return D
