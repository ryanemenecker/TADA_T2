TADA_T2
==============================
[//]: # (Badges)
[![GitHub Actions Build Status](https://github.com/REPLACE_WITH_OWNER_ACCOUNT/TADA_T2/workflows/CI/badge.svg)](https://github.com/REPLACE_WITH_OWNER_ACCOUNT/TADA_T2/actions?query=workflow%3ACI)
[![codecov](https://codecov.io/gh/REPLACE_WITH_OWNER_ACCOUNT/TADA_T2/branch/main/graph/badge.svg)](https://codecov.io/gh/REPLACE_WITH_OWNER_ACCOUNT/TADA_T2/branch/main)


A Tensorflow2 compatible version of the TADA transcriptional activation domain predictor.

# Usage

This documentation covers the functions for predicting TAD scores using the TADA model. The available functions are `predict` and `predict_from_fasta`.
  
**NOTE** At this time sequences must be 40 amino acids!!!

## predict
  
Predicts TAD scores for a sequence or a list of sequences.
  
```python
predict(sequences, return_dict=False)
```

**Parameters**:
    - ``sequences`` (str or list): A string of a single sequence or a list of sequences to predict TADA scores for.
    - ``return_dict`` (bool): Whether to return a dictionary with the sequence as the key and the prediction score as the value. Default is False.
**Returns**:
if return_dict is False:
    - list: A list of TADA scores for each input sequence.
if return_dict is True:
    - dict: A dictionary with the sequence as the key and the prediction score as the value.

### Examples
Predicting TAD scores for a single sequence:
```python
single_sequence = "EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD"
tada_score = predict(single_sequence)
print(tada_score)
[0.6459648]
```

Predicting TAD scores for multiple sequences:
```python
sequence_list = ["QFNENSNIMQQQPLQGSFNPLLEYDFANHGGQWLSDYIDL", "EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD"]
tada_scores = predict(sequence_list)
print(tada_scores)
[0.63707864, 0.6459648]
```

Returning predictions as a dictionary:
```python
sequence_list = ["QFNENSNIMQQQPLQGSFNPLLEYDFANHGGQWLSDYIDL", "EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD"]
predictions_dict = predict(sequence_list, return_dict=True)
print(predictions_dict)
{'QFNENSNIMQQQPLQGSFNPLLEYDFANHGGQWLSDYIDL': 0.6370786, 'EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD': 0.6459648}
```

## predict_from_fasta
  
Predicts TAD scores for sequences in a .fasta file.
  

```python
predict_from_fasta(path_to_fasta):
```
  
**Parameters**:  
  ``path_to_fasta`` (str): Path to a .fasta file as a string.

**Returns**:  
  A dictionary with the name of the sequence from the FASTA file as the key and a list as the value, where the first element is the sequence and the second element is the TADA score.

### Examples

Predicting TAD scores for sequences in a .fasta file:
```python
fasta_file = "example.fasta"
fasta_predictions = predict_from_fasta(fasta_file)
print(fasta_predictions)
{'0': ('QFNENSNIMQQQPLQGSFNPLLEYDFANHGGQWLSDYIDL', 0.63707864), '1': ('EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD', 0.6459648), '2': ('VLPPLSESFDLDSLMSTPMSSPRQNSIEAETNSSTFFDFG', 0.66275495), '3': ('SWLLPNSGKNSGNNNGFSIGDEFLNLVDYSSSDKQFTDQS', 0.5776086)}
```

## Installation

Make sure to have the necessary dependencies installed. You can install them via pip:

**Section to be updated soon**

Dependencies are:
* alphaPredict
* Tensorflow
* localcider
* numpy
* scikit-learn
* protfasta


### Copyright

Copyright (c) 2024, Ryan Emenecker Holehouse Lab WUSM


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.10.
