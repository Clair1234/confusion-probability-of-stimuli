# Methodology

## Purpose
Explains how to use the method, what the pipeline does step-by-step, and how to reproduce results

## Overview

The method estimates perceptual confusion between stimuli based on
their physical descriptions and psychophysical parameters.

The pipeline consists of three main stages:

1. Compute distances per dimension (JND-normalized)
2. Combine distances across dimensions
3. Convert distances into confusion probabilities

## Input Data

The method requires three inputs:

- A stimulus description file (`stimuli.json`)
- A JND definition file (`jnd.json`)
- A weights file (`weights.json`)

See [input_format.md](input_format.md) for full specification.


## Step 1: Dimensional Distance Computation

For each dimension \( d \), pairwise distances between stimuli are computed.

Given two stimuli \( s_i, s_j \), the distance is:

- Absolute JND:
  
  \( d_{ij} = \frac{|x_i - x_j|}{JND} \)

- Relative JND:

  \( d_{ij} = \frac{|x_i - x_j|}{\max(x_i, x_j)} \cdot \frac{1}{JND} \)

Distances are expressed in units of JND.

## Step 2: Distance Integration

Distances across dimensions are combined using a weighted Euclidean metric:

\[
D_{ij} = \sqrt{ \sum_{k} (w_k \cdot d_{ij}^{(k)})^2 }
\]

where:
- \( d_{ij}^{(k)} \) is the distance along dimension \( k \)
- \( w_k \) is the weight assigned to that dimension


## Step 3: Distance to Confusion Mapping

Distances are transformed into confusion probabilities using a psychometric function.

Default model: logistic function

\[
P_{ij} = \frac{1}{1 + \exp(\beta (D_{ij} - \alpha))}
\]

With:
- \( \alpha \): discrimination threshold (default = 1 JND)
- \( \beta \): slope parameter (default = log(3))

For distances below threshold:
\[
P_{ij} = 0.5
\]

## Step 4: Normalization

The confusion matrix is row-normalized:

\[
P_{ij}^{norm} = \frac{P_{ij}}{\sum_j P_{ij}}
\]

## Usage

See ``generate_confusion_matrix.py``.


## Reproducibility

All computations are deterministic given:
- identical input files
- identical psychometric parameters

Results are stored as JSON files for full reproducibility.