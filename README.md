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
```

```

#### 2. Compute total distance
```

```

#### 3. Compute confusion matrix
```

```

#### 4. Evaluate results
```

```

#### Integrated first 3 steps
See integrated pipeline with: 
```
python generate_confusion_matrix.py --stimuli examples\sand_evaluating_2020\stimuli.json --jnd examples\jnd.json --weights examples\sand_evaluating_2020\weights.jnd
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

