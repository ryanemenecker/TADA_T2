TADA_T2
==============================

# About TADA_T2

TADA_T2 is a Tensorflow2 compatible version of the TADA transcriptional activation domain predictor. TADA_T2 was developed with additional user-facing functionality to make TADA more accessible to the scientific community. TADA allows users to input protein sequences or .fasta files and get back TAD scores, which are a measure of the ability of a protein to activate transcription. See https://www.nature.com/articles/s41586-024-07707-3 for the original publication. Note that **the values are only predictions and should be treated as such**. Nothing can substitute for experimental validation; however, the TADA scores can be used as a guide to help generate new hypotheses or plan new experiments. 
  
Credit to Lisa Van den Broeck for creating the original implementation of TADA. The original version of TADA can still be found at https://github.com/LisaVdB/TADA

## What does my TAD score mean?
TAD scores range between 0 and 1 where 0 means that the model **predicts** the protein sequence will *not* be a transcriptional activator and 1 means that the model **predicts** the protein sequence *will* be a transcriptional activator. TAD scores are a measure of the ability of a protein to activate transcription. 

## How were the transcriptional activation domains originally identified?
To simplify things a bit, the original avitvation domains were identified using a high-throughput assay in *Saccharomyces cerevisiae* that assessed the ability of tens of thousands of different 40 amino acid fragments to drive transcription of a reporter. For more information on the actual assay, please see: https://www.nature.com/articles/s41586-024-07707-3

## How does TADA_T2 work..?
TADA_T2 takes in 40 amino acid long sequences and calculates a bunch of features from that sequence such as charge, hydrophobicity, etc. (see the create_features() function in /TADA_T2/backend/features.py). These features are then fed into a ML model that uses a network originally trained tens of thousands of 40 amino acid fragments that were the experimentally tested for their capacity to drive transcriptional activation. This is ultimately used to predict whether the input sequence is or is not likely to be a transcriptional activation domain.

## What if my sequence is longer than 40 amino acids?
**Right now TADA_T2 can only run predictions on sequences that are 40 amino acids long. I am adding functionality to either pad sequences shorter than 40 amino acids or use a sliding window approach for sequences longer than 40 amino acids. However, I need to go to bed so that's for another day.**
In the future, TADA_T2 will be able to make predictions of other length sequences (sort of). TADA_T2 can make predictions on sequences longer than 40 amino acids by using a 'sliding window' approach. Basically, TADA can 'scan over' your sequence to identify potential transcriptional activation domains. Note that **this is equivalent to breaking up your sequence into 'chunks' of 40 amino acids and making individual predictions on each chunk**. Thus, it is important to remember that predictions will only take in information from windows of 40 amino acids.

## How can I cite TADA or TADA_T2?
Please cite the original publication at https://www.nature.com/articles/s41586-024-07707-3. If you use TADA_T2, please mention in your methods that you used TADA_T2 to generate your predictions so your readers know exactly how you got your results and so that they can use TADA_T2 if they would like to.

### Citation:
Morffy, N., Van den Broeck, L., Miller, C. et al. Identification of plant transcriptional activation domains. Nature 632, 166–173 (2024). https://doi.org/10.1038/s41586-024-07707-3


# Installation

**NOTE**: TADA_T2 is not yet on PyPi! Do not use this approach yet!

To install from PyPI, run:
```bash
    pip install TADA_T2
```

You can also install the current development version from
```bash
    pip install git+https://git@github.com/ryanemenecker/TADA_T2
```

To clone the GitHub repository and gain the ability to modify a local copy of the code, run
```bash
    git clone https://github.com/ryanemenecker/TADA_T2.git
    cd TADA_T2
    pip install -e .
```

# Usage

This documentation covers the functions for predicting TAD scores using the TADA model. The available functions are `predict` and `predict_from_fasta`.
 
First import the functions. 

```python
from TADA_T2.TADA import predict, predict_from_fasta
```
  
Now you should be ready to go!

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

# other TADA_T2 info...

## TADA_T2 dependencies
Dependencies are:
* alphaPredict
* Tensorflow
* localcider
* numpy
* protfasta
* getSequence


### Copyright

Copyright (c) 2024, Ryan Emenecker Holehouse Lab WUSM


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.10.
