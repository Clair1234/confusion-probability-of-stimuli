# Confusion probability of stimuli


The method is a computational tool to estimate **perceptual distances** and **confusion probabilities** between stimuli based on:

- multidimensional physical descriptions
- Just Noticeable Difference (JND)
- psychophysical models

It is designed for **research in psychophysics, HCI, and multimodal perception**.

---

## Overview

The pipeline:

```
Physical properties of stimuli -> Per-dimension distances -> Integrated distance -> Confusion probabilities
```

### Steps:
1. Compute pairwise distances per dimension (JND-normalized)
2. Combine distances across dimensions (weighted integration)
3. Map distances to confusion probabilities (psychometric function)

### Installation - TBD
```

```

### Main functions
#### 1. Compute dimensional distances
Two dictionnaries have to be defined, here they are extracted from .json files (see [docs/input_format.md](docs/input_format.md) for input description):
- stimuli: explains the characteristics of stimuli.
- jnd: lists the discrimination thresholds (or ``Just Noticeable Difference``).

The function that is responsable for computing the dimensional distances takes two arguments and is:
```
compute_dimensional_distances(stimuli, jnd)
```
This function is available in [src/distances/compute_dimensional.py](src/distances/compute_dimensional.py).

There are two outputs:
- a dictionary that, for each dimension, gives you the pairwise distance between stimuli
- a list that gives you the categories, if any (for examplefor Sand et al there are none but for Chen et al. there are four categories (C1), (C2), (C3), (C4))

#### 2. Compute total distance
Two dictionaries have to be defined, here one comes from the ``compute_dimensional_distances`` function and the other is extracted from a .json file (see [docs/input_format.md](docs/input_format.md) for input description):
- results: describes dimension per dimension the pairwise distances between stimuli.
- weights: lists the weights attributed to each dimension in results.

The function that is responsable for computing the total distance takes two arguments and is:
```
compute_global_distance(results, weights)
```
There is one output : the total distance matrix between stimuli. 

This function is available in [src/distances/combine_dimensions.py](src/distances/combine_dimensions.py).

#### 3. Compute confusion matrix
One dictionaru has to be defined, here it comes from the ``compute_global_distance`` function :
- global_distance: describes the pairwise distances between stimuli.

It can take optional variables such as ``alpha`` and ``beta`` to change the parameters of the logistic function (see [docs/theory.md](docs/theory.md) for details).

The funciton that is responsible for the translation of distances into proability of confusion is: 
```
distance_to_confusion(global_distance)
```
There is one output : the **not normalised** confusion matrix.

This function is available in [src/confusion/compute_confusion.py](src/confusion/compute_confusion.py).

The ``normalize`` function (available in [src/confusion/normalize.py](src/confusion/normalize.py)) normlize the confusion matrix. 

#### 4. Evaluate results
If a confusion matrix otherwise obtained (such as through user tests) is available. The similarities between the confusion matrices can be evaluated with multiple functions from [src/evaluation/metrics.py](src/evaluation/metrics.py). Two dictionaries need to be defined, here they are stored in .json files (see [docs/input_format.md](docs/input_format.md) for input description):
- reference.json: gives the confusion matrix of reference
- prediction.json: gives the confusion matrix from the method

A pipeline of evaluation is available and requires a ``out_folder`` to store the output:
```
validate.py --ref reference.json --prediction prediciton.json --out out_folder
```

#### Integrated first 3 steps
See integrated pipeline with an exemple. The integrated first 3 steps requires a ``out_folder`` to store the output: 
```
python generate_confusion_matrix.py --stimuli examples\sand_evaluating_2020\stimuli.json --jnd examples\jnd.json --weights examples\sand_evaluating_2020\weights.jnd --out out_folder
```

### Input files 
The method requires **three input files**:
- ``stimuli.json``: Stimulus descriptions
- ``jnd.json``: Perceptual hresholds (JND: Just Noticeable Difference)
- ``weights.json``: Dimension weights

See [docs/input_format.md](docs/input_format.md) for full specification.


## Core idea

The method models perception as :

### 1. JND-normalized space
Distance are expressed in perceptual units: 
```
d = \frac{|x1 - x2|}{JND}
```

### 2. Multidimensional integration
```
D = sqrt( \sum_k (w_k d_k)^2 )
```

### 3. Psychophysical mapping
```
P = \frac{1}{1 + exp( \beta (D - \alpha) )}
```
where \alpha is a perceptual threshold (default: 1 JND)

and \beta a slope parameter (default: ln(3))

## Outputs
The method produces:
- Distance matrices
- Confusion probability matrices
- Normalized confusion matrices
- Optional evaluation metrics

## Documentation
- [docs/input_format.md](docs/input_format.md)
- [docs/methodology.md](docs/methodology.md)

## Use case
- Multimodal perception modeling
- Haptic and audio interface design for discriminative tasks
- Predicting confusion in stimulus sets prior to user tests

## Limitations
- Assumes independence between dimensions
- Used fixed JND thresholds
- Logistic mapping is an approximation

## Example
See [examples/](examples/) for 3 examples from literature.

The following articles were used:
- Chen, H. Y., Park, J., Tan, H. Z., & Dai, S. (2010, March). Redundant coding of simulated tactile key clicks with audio signals. In 2010 IEEE Haptics Symposium (pp. 29-34). IEEE.
- Sand, A., Rakkolainen, I., Surakka, V., Raisamo, R., & Brewster, S. (2020, September). Evaluating ultrasonic tactile feedback stimuli. In International Conference on Human Haptic Sensing and Touch Enabled Computer Applications (pp. 253-261). Cham: Springer International Publishing.
- Vo, D. B., Pauchet, S., Jolly, I., Simon, F., Brock, A. M., & Garcia, J. (2023, April). Tactilient: Turbulence resilient tactile icons for pilot feedback. In Proceedings of the 2023 CHI Conference on Human Factors in Computing Systems (pp. 1-13).


## Citation 
If you use this work, please cite
```
Coming soon
```

