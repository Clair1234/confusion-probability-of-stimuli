# HEADER
import json
import argparse
import numpy as np
from src.distances.compute_dimensional import compute_dimensional_distances
from src.distances.combine_dimensions import compute_global_distance
from src.confusion.compute_confusion import distance_to_confusion
from src.confusion.normalize import normalize
from src.evaluation.plots import plot_matrix


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stimuli", required=True)
    parser.add_argument("--jnd", required=True)
    parser.add_argument("--out", required=True) # change to folder
    parser.add_argument("--weights", required=True)

    args = parser.parse_args()

    with open(args.stimuli) as f:
        stimuli = json.load(f)

    with open(args.jnd) as f:
        jnd = json.load(f)
        
    with open(args.weights) as f:
        weights = json.load(f)


    # Compute dimensional distances
    results, categories = compute_dimensional_distances(stimuli, jnd)

    # Save dimensional distances
    output_file = args.out + "\\dimensional_distances.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    
    # Compute global distance
    if categories != ['']:
        global_distance = {}
        for categorie in categories :
            
            global_distance_sub = compute_global_distance(results[categorie], weights)
    
            output_file = args.out + "\\global_distances_" + categorie + ".json"

            with open(output_file, "w") as f:
                json.dump(global_distance_sub, f, indent=2)  
                
            global_distance[categorie] = global_distance_sub  
 
    else :
        global_distance = compute_global_distance(results, weights)
    
        output_file = args.out + "\\global_distances.json"
        with open(output_file, "w") as f:
            json.dump(global_distance, f, indent=2)
            
    
    
    
    # Convert to probabilities of confusion
    alpha = 1
    beta = np.log(3)
    
    if categories != ['']:
        confusion_probabilities = {}
        for categorie in categories :
            
            confusion_probabilities_sub = distance_to_confusion(global_distance[categorie], alpha=alpha, beta=beta)
    
            output_file = args.out + "\\confusion_probabilities_" + categorie + ".json"

            with open(output_file, "w") as f:
                json.dump(confusion_probabilities_sub, f, indent=2)  
                
            confusion_probabilities[categorie] = confusion_probabilities_sub  
 
    else :
        confusion_probabilities = distance_to_confusion(global_distance, alpha=alpha, beta=beta)
    
        output_file = args.out + "\\confusion_probabilities.json"
        with open(output_file, "w") as f:
            json.dump(confusion_probabilities, f, indent=2)
    
    
    
    
    # Normalize the probabilities of confusion
    if categories != ['']:
        confusion_probabilities_normalized = {}
        for categorie in categories :
            
            confusion_probabilities_normalized_sub = normalize(confusion_probabilities[categorie])
    
            output_file = args.out + "\\confusion_probabilities_normalized_" + categorie + ".json"

            with open(output_file, "w") as f:
                json.dump(confusion_probabilities_normalized_sub, f, indent=2)  
                
            confusion_probabilities_normalized[categorie] = confusion_probabilities_normalized_sub  
 
    else :
        confusion_probabilities_normalized = normalize(confusion_probabilities)
    
        output_file = args.out + "\\confusion_probabilities_normalized.json"
        with open(output_file, "w") as f:
            json.dump(confusion_probabilities_normalized, f, indent=2)
                  
            
    # Plot results
    if categories != ['']:
        for categorie in categories :
            
            confusion_plot = plot_matrix(confusion_probabilities_normalized[categorie])
    
            output_file = args.out + "\\confusion_plot_" + categorie + ".png"  
            confusion_plot.savefig(output_file, dpi=confusion_plot.dpi)
 
    else :
        confusion_plot = plot_matrix(confusion_probabilities_normalized)
        output_file = args.out + "\\confusion_plot.png"
        confusion_plot.savefig(output_file, dpi=confusion_plot.dpi)    
    
        
if __name__ == "__main__" :
    main()