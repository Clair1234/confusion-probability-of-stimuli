#HEADER
import json
import argparse
import pandas as pd
import numpy as np
from scipy.spatial import procrustes
from src.confusion.normalize import normalize
from src.evaluation.plots import plot_matrix
from src.evaluation.plots import plot_linear_regression
from src.evaluation.plots import plot_distribution
from src.evaluation.metrics import descriptive_statistics
from src.evaluation.metrics import hellinger_distance
from src.evaluation.metrics import bootstrap_hellinger
from src.evaluation.metrics import bootstrap_correlation
from src.evaluation.metrics import js_divergence
from src.evaluation.metrics import mantel_structure_test
from src.evaluation.metrics import procrustes_pvalue


def main(): 
    parser = argparse.ArgumentParser()
    parser.add_argument("--ref", required=True)
    parser.add_argument("--prediction", required=True)
    parser.add_argument("--out", required=True) # change to folder
    
    args = parser.parse_args()
    
    with open(args.ref) as f:
        ref = json.load(f)

    with open(args.prediction) as f:
        prediction = json.load(f)
        
        
    # Normalize reference to ensure correct shape
    reference = normalize(ref)
   
    # Convert to dataframe
    prediction = pd.DataFrame(prediction)
    prediction = prediction.reindex(sorted(prediction.index), axis=0)
    prediction = prediction.reindex(sorted(prediction.columns), axis=1)
    
    reference = pd.DataFrame(reference)
    reference = reference.reindex(sorted(reference.index), axis=0)
    reference = reference.reindex(sorted(reference.columns), axis=1)
        
    
    # Plot reference's confusion matrix
    reference_confusion_plot = plot_matrix(reference)
    output_file = args.out + "\\confusion_plot.png"
    reference_confusion_plot.savefig(output_file, dpi=reference_confusion_plot.dpi) 
    
    
    # Evaluate similarities
    
    ## Descriptive analysis
    _ = descriptive_statistics(prediction=prediction, reference=reference)
    
    ## Linear Regression
    linear_regression = plot_linear_regression(reference=reference, prediction=prediction)
    output_file = args.out + "\\linear_regression.png"
    linear_regression.savefig(output_file)
    
    ## Plot distribution
    distribution_plot = plot_distribution(reference=reference, prediction=prediction)
    output_file = args.out + "\\distribution_plot.png"
    distribution_plot.savefig(output_file, dpi=distribution_plot.dpi)
    
    ## MAE, RMSE
    diff = prediction.values.astype(float) - reference.values.astype(float)
    mae = np.mean(np.abs(diff))
    rmse = np.sqrt(np.mean(diff**2))
    print("\nError calulated as (prediction - reference)")
    print(f"    MAE: {mae}")
    print(f"    RMSE: {rmse}")
    
    ## Spearman Correlation 
    print("\nBootstrap evaluation with diagonal")
    results = bootstrap_correlation(prediction=prediction, reference=reference, exclude_diag=False)
    print(f"Pearson r = {results['pearson_r']:.3f}")
    print(f"    95% CI = [{results['pearson_ci_95'][0]:.3f}, {results['pearson_ci_95'][1]:.3f}]")
    print(f"    SE = {results['pearson_se']:.3f}")
    print(f"    p = {results['pearson_p']:.10f}")
    print(f"Spearman rho = {results['spearman_rho']:.3f}")
    print(f"    95% CI = [{results['spearman_ci_95'][0]:.3f}, {results['spearman_ci_95'][1]:.3f}]")
    print(f"    SE = {results['spearman_se']:.3f}")
    print(f"    p = {results['spearman_p']:.10f}")
    
    print("\nBootstrap evaluation without diagonal")
    results = bootstrap_correlation(prediction=prediction, reference=reference)
    print(f"Pearson r = {results['pearson_r']:.3f}")
    print(f"    95% CI = [{results['pearson_ci_95'][0]:.3f}, {results['pearson_ci_95'][1]:.3f}]")
    print(f"    SE = {results['pearson_se']:.3f}")
    print(f"    p = {results['pearson_p']:.10f}")
    print(f"Spearman rho = {results['spearman_rho']:.3f}")
    print(f"    95% CI = [{results['spearman_ci_95'][0]:.3f}, {results['spearman_ci_95'][1]:.3f}]")
    print(f"    SE = {results['spearman_se']:.3f}")
    print(f"    p = {results['spearman_p']:.10f}")
    
    ## Hellinger distance
    hd_overall = hellinger_distance(prediction, reference)
    print(f"\nHellinger distance (overall): {hd_overall}")
    for signal in prediction.keys():
        hd = hellinger_distance(prediction.loc[signal], reference.loc[signal])
        print(f"    Hellinger distance [{signal}]: {hd}")
        
    hd_obs, hd_pval = bootstrap_hellinger(prediction, reference)
    print(f"Hellinger distance (bootstrap): {hd_overall}, with p-value: {hd_pval}")
    
    ## Jensen Shannon Divergence
    jsd = js_divergence(reference=reference, prediction=prediction)
    print(f"\nJensen-Shannon divergence: {jsd}, squared-root JSD: {np.sqrt(jsd)}")

    ## Mantel Test
    r1, p1 = mantel_structure_test(reference, prediction)
    r2, p2 = mantel_structure_test(prediction, reference)
    print(f"\nMantel r strucutre: {(r1 + r2)/2}, p={(p1 + p2)/2}")
    
    ## Procrustes
    mtx1, mtx2, disparity = procrustes(reference, prediction)
    D_obs, p_value, D_perm = procrustes_pvalue(reference=reference, prediction=prediction)    
    print(f"\nProcrustes test disparity: {disparity}, p_value: {p_value}\n")

    



if __name__ == "__main__" :
    main()