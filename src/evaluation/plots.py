# HEADER 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def plot_matrix(matrix, transpose=True) :
    matrix_df = pd.DataFrame(matrix)
    
    # Transpose so that y is True
    if transpose == True :
        matrix_df = matrix_df.T
    
    # Ensure correct order
    matrix_df = matrix_df.reindex(sorted(matrix_df.index), axis=0)
    matrix_df = matrix_df.reindex(sorted(matrix_df.columns), axis=1)
    
    # Plot
    fig = plt.figure(figsize=(10, 8))
    sns.heatmap(matrix_df, annot=True, cmap="Blues", fmt=".2f", annot_kws={"size": 14})
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    #plt.show()
    
    return fig


def plot_linear_regression(prediction, reference) :
    
    M_prediction =  prediction.values
    M_reference = reference.values
    
    flat_prediction = []
    flat_reference = []
    
    diag_prediction = []
    diag_reference = []
    for key1 in prediction.keys():
        for key2 in prediction[key1].keys():
        
            flat_prediction.append(prediction[key1][key2])
            flat_reference.append(reference[key1][key2])
            
            if key1 == key2:
                diag_prediction.append(prediction[key1][key2])
                diag_reference.append(reference[key1][key2])
    
    df = pd.DataFrame({'data_method': flat_prediction, 'data_article': flat_reference})
    
    
    x = df["data_method"]
    y = df["data_article"]

    slope, intercept = np.polyfit(x, y, 1)
    #print(f"y = {slope:.3f}x + {intercept:.3f}")

    
    #PLOT
    g = sns.jointplot(data=df, x="data_method", y="data_article")
    ax = g.ax_joint

    ax.plot([0,1], [0,1], '--', color='green', label='Perfect prediction')
    ax.plot([0,1], [intercept,slope+intercept], '--', color='orange', label=f'Linear Regression : y = {slope:.3f}x + {intercept:.3f}')

    ax.legend(loc='upper left')
    
    plt.xlabel('P(confusion) - Method')
    plt.ylabel('P(confusion) - User Tests')
    
    return g
    

def plot_distribution(reference, prediction):

    # Flatten
    flat_prediction = []
    flat_reference = []
    for key1 in prediction.keys():
        for key2 in prediction[key1].keys():
            flat_prediction.append(prediction[key1][key2])
            flat_reference.append(reference[key1][key2])
    

    # Distribution of probabilities
    fig, ax = plt.subplots(figsize=(6, 6))
    fig.tight_layout()
    ax.tick_params(labelsize=15)
    # histogram plot the samples
    ax.hist(flat_prediction, bins=50, alpha=0.6, color='r', label="Proposed method")
    ax.hist(flat_reference, bins=50, alpha=0.3, color='b', label="Reference")
    ax.set_xlabel("Probbalitity", fontsize=15)
    ax.set_ylabel("Likelihood", fontsize=15)
    plt.legend(frameon=False, fontsize=15)
    
    return fig
