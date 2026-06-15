# Input format documentation

## Input file formats

This document describes the required JSON formats for using the method pipeline

The pipeline requires **three input files**:
1. Stimuli description (stimuli.json)
2. JND thresholds (jnd.json)
3. Dimension weights (weights.json)

## Stimuli file 

### Purpose
Defines the set of stimuli and their physical properties

### Structure

The file is a nested JSON object with the following hierarchy 

```
Test category (optional) -> Signal -> Modality -> Dimension -> {Value, Unit}
```

The names "Signal", "Value", and "Unit" are mandatory, the code uses these names to parse the file. 

### Example

```
{
  "Signal1": {
    "Vibrotactile": {
      "Frequency": {
        "Value": 30,
        "Unit": "Hz"
      },
      "TotalDuration": {
        "Value": 1,
        "Unit": "s"
      }
    }
  }
}
```

### Rules

#### Signals
Each simulus must be named using:
```
SignalX (e.g. Signal1, Signal2,...)
```

#### Modalities
Signals must contain one or more modalities:
- "Vibrotactile"
- "Audio"
- (extensible)

#### Dimensions
Each modality contains dimensions, e.g.:
- Frequency
- Duration
- NumberOfPulses

Dimensions can be nested, for example: 
```
"Signal1" : {
    "Audio" : {
        "Intensity" : {
            "Left" : {
                "AVG" : {
                    "Value" : 76.24,
                    "Unit" : "db(A)"
                    },
                "STD" : {
                    "Value" : 0.42,
                    "Unit" : "db(A)"
                    }
            }
        }
    }
}
```

#### Values 
Each dimension must include: 
```
{
  "Value": <number>,
  "Unit": <string>
}
```

#### Units
Examples:
- "Hz"
- "ms"
- "s"
- "None" (for unitless quantities) 

#### Constraints
- All signals must have consistent structure
- Units must be identical across signals for a given dimension
- Values must be numerical


## JND file 

### Purpose
Defines the **Just Noticeable Difference (JND)** threshold ofr each dimension.

These values are used to **normalize perceptual distances**.

### Structure
```
Modality -> Dimension -> {Value, Unit}
```

### Example
```
{
  "Vibrotactile": {
    "Frequency": {
      "Value": 18,
      "Unit": "%"
    },
    "Duration": {
      "Value": 28.75,
      "Unit": "%"
    },
    "NumberOfIPI": {
      "Value": 1,
      "Unit": "None"
    }
  }
}
```

### Interpretation

#### Absolute JND
```
"Value": 10,
"Unit": "Hz"
```

Distance is computed as:
```
|x1 - x2| / JND
```

#### Relative JND (%)
```
"Value": 18,
"Unit": "%"
```
Distance is computed as:
```
(|x1 - x2| / max(x1, x2)) / (JND/100)
```

#### Matching rule
- Dimension names in JND must match or partially match those in the stimuli file for a given modality
- Matching is based on string inclusion

Example:
```
Stimuli : "Frequency"
matches with
JND: "Frequency"
```
```
Stimuli: "Intensity.Left.AVG"
matches with
JND: "Intensity"
```

## Weights file

### Purpose
Defines how each dimension contributes to the **global perceptual distance**.

### Strucuture
Flat dictionary, seperated by ".":
```
"Modality.Dimension" : weight
```

### Example
```
{
  "Vibrotactile.Frequency": 1,
  "Vibrotactile.IPIDuration": 1,
  "Vibrotactile.NumberOfIPI": 1,
  "Vibrotactile.NumberOfPulses": 1,
  "Vibrotactile.PulseDuration": 1,
  "Vibrotactile.TotalDuration": 1
}
```

### Interpretation
Global distance is computed as:
```
D(s1, s2) = sqrt( \sum (w_i * d_i)^2 )
```
where:
- d_i = distance in JND units
- w_i = weight for dimension i

### Constraints
- All dimension used in distance computation must have a weight
- Missing weights -> error

#### Recommendation:
- Use consistent naming accross all files
- Avoid plural / singular mismatches, the code will not work

Example:
```
NumberOfPulse vs NumberOfPulses
```

## Checking the format

Run ``test_schema.py`` with ``stimuli.json`` or ``weights.json`` or ``jnd.json``, if in doubt.
```
python test_schema.py --stimuli stimuli.json
python test_schema.py --weights weights.json
python test_schema.py --jnd jnd.json
```