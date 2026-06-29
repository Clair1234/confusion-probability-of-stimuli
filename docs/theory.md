# Theory (WIP)

## Problem Statement

Predicting perceptual confusion between stimuli is a central problem in psychophysics.

Given:
- a set of stimuli described by physical parameters
- human sensitivity thresholds (JND)

We aim to estimate:
\[
P(\text{response } s_j \mid \text{stimulus } s_i)
\]


## Perceptual Space

We assume stimuli lie in a perceptual space where each physical dimension is rescaled according to perceptual sensitivity (JND).

Distances are therefore expressed in units of discriminability.


## JND Normalization

According to Weber-Fechner law, perceptual sensitivity depends on relative variation:

\[
\Delta I / I = constant
\]

Thus, distances are normalized to reflect perceptual equivalence.


## Multidimensional Integration

Perceptual dimensions are assumed to combine according to:

- Separable dimensions
- Euclidean integration

This assumption is common in perceptual modeling.


## Distance–Confusion Relationship

Confusion probability is modeled as a monotonic decay of distance.

We use a logistic function as a psychometric model:

- captures threshold behavior
- consistent with signal detection theory (for example in the definition of the perceptron)


## Discrimination Threshold

Below 1 JND, stimuli are assumed indistinguishable:

\[
P = 0.5
\]

This reflects chance-level performance.


## Relation to Existing Work

This approach relates to:

- Signal Detection Theory
- Multidimensional Scaling (MDS)


## Limitations

- Independence of dimensions may not always hold
- Logistic mapping is an approximation
- JND values may vary across individuals and contexts


## Extensions: Not planned yet

Future work may include:

- learned psychometric functions
- non-Euclidean metrics
- Bayesian inference of confusion
