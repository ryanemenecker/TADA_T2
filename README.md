TADA_T2
==============================

# About TADA_T2

TADA_T2 is a Tensorflow2 compatible version of the TADA transcriptional activation domain (TAD) predictor. TADA_T2 was developed with additional user-facing functionality to make TADA more accessible to the scientific community. With TADA_T2, you can input protein sequences or .fasta files and get back TAD scores, which are a measure of the ability of a protein sequence to activate transcription. See the [original publication](https://www.nature.com/articles/s41586-024-07707-3) for more details.
  
Credit to Lisa Van den Broeck for creating the original implementation of TADA. The original implementation can be found [here](https://github.com/LisaVdB/TADA).

## What does my TAD score mean?
TAD scores range between 0 and 1 where 0 means that the model **predicts** the protein sequence will *not* be a transcriptional activator and 1 means that the model **predicts** the protein sequence *will* be a transcriptional activator. Note that **the values are only predictions and should be treated as such**. Nothing can substitute for experimental validation; however, the TADA scores can be used as a guide to help generate new hypotheses or plan new experiments. 

## How were the transcriptional activation domains originally identified?
To simplify things a bit, the original activation domains were identified using a high-throughput assay in *Saccharomyces cerevisiae* that assessed the ability of tens of thousands of different 40 amino acid fragments to drive transcription of a reporter. For more information on the actual assay, please see the [publication](https://www.nature.com/articles/s41586-024-07707-3).

## How does TADA_T2 work..?
TADA_T2 takes in 40 amino acid long sequences and calculates a bunch of features from that sequence such as charge, hydrophobicity, etc. [see the create_features() function](https://github.com/ryanemenecker/TADA_T2/blob/main/TADA_T2/backend/features.py). These features are then fed into a ML model that uses a network originally trained tens of thousands of 40 amino acid fragments that were the experimentally tested for their capacity to drive transcriptional activation. This is ultimately used to predict whether the input sequence is or is not likely to be a transcriptional activation domain.

## What if my sequence is not 40 amino acids?

TADA_T2 can make predictions of other length sequences (sort of).

### Sequences longer than 40 amino acids:
For sequences longer than 40 amino acids, TADA_T2 uses a 'sliding window' approach. Basically, TADA can 'scan over' your sequence to identify potential transcriptional activation domains. Note that **this is equivalent to breaking up your sequence into 'chunks' of 40 amino acids and making individual predictions on each chunk**. Thus, it is important to remember that predictions will only take in information from windows of 40 amino acids.

### Sequences shorter than 40 amino acids:
For sequences shorter than 40 amino acids, TADA_T2 will pad the sequence with 'X' amino acids to make the sequence 40 amino acids long. You can choose to pad the sequence evenly or on the N- or C-terminus. Further, you can pad the sequence with just G and S or a random selection of amino acids. **This is NOT ideal** and we recommend that you do not use TADA_T2 to predict TAD scores for sequences shorter than 40 amino acids. However, this functionality is available for users if you set ``safe_mode=False``. Because the predictor was not made for this, the predictions may not be accurate. Thus, by default we restrict the availablity of this feature. 

## How can I cite TADA or TADA_T2?
Please cite the original publication at https://www.nature.com/articles/s41586-024-07707-3. If you use TADA_T2, please mention in your methods that you used TADA_T2 to generate your predictions and link to this repository so your readers know exactly how you got your results and so that they can use TADA_T2 if they would like to.

### Citation:
Morffy, N., Van den Broeck, L., Miller, C. et al. Identification of plant transcriptional activation domains. Nature 632, 166–173 (2024). https://doi.org/10.1038/s41586-024-07707-3


# Installation

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

## Important note about predictions:
TADA was originally made to make predictions of 40 amino acid sequences. Thus, if your sequence is over 40 amino acids, TADA_T2 will break it up into 40 amino acid 'chunks' and return a list of predictions where the first element in the list is the sequence for a given chunk and the second element is the TADA score for that chunk. If your sequence is less than 40 amino acids, TADA_T2 will by default raise an exception. You can disable this by setting ``safe_mode=False`` in the predict function. However, we do not recommend this as the predictions may not be accurate. 


## predict
  
The ``predict`` function lets you predicts TAD scores for a sequence or a list of sequences.
  
```python
predict(sequences)
```

**Parameters**:
* ``sequences`` (str or list): A string of a single sequence or a list of sequences to predict TADA scores for.
* ``overlap_length`` int: The amount of overlap to have between sequences when breaking up sequences longer than 40 amino acids. Default is 39.
* ``safe_mode`` (bool): If True, the function will raise an exception if the sequence is less than 40 amino acids. If False, the function will pad the sequence with 'X' amino acids to make the sequence 40 amino acids long. Default is True.
* ``pad`` (str): What amino acids to pad your sequence with if it is less than 40 amino acids. Options are 'random' or 'GS'. The 'random' option will pad your sequence with randomly chosen amino acids and the 'GS' option will pad your sequence with randomly selected G or S. Default is 'GS'.
* ``approach`` (str): How to pad the sequence if it is less than 40 amino acids. Options are 'even', 'N', or 'C'. The 'even' option will pad the sequence evenly on both sides, the 'N' option will pad the sequence on the N-terminus, and the 'C' option will pad the sequence on the C-terminus. Default is 'even'.
* ``verbose`` (bool): If True, the function will print out a warning when sequences are not all 40 amino acids. Default is True.


  
**Returns**:

The ``predict`` function returns a dictionary where the key is the sequence and the value is a list of lists where the first element in each sublist is the sequence used for the prediction and the second element is the score the specific sequence used for that prediction. The reason for this formatting is to keep it consistent with predictions of sequences that are not 40 amino acids in length.

### Examples

#### Predicting TAD scores for a single sequence:
```python
single_sequence = "EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD"
tada_score = predict(single_sequence)
print(tada_score)
{'EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD': [['EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD', 0.64596486]]}
```

#### Predicting TAD scores for multiple sequences:
```python
sequence_list = ["QFNENSNIMQQQPLQGSFNPLLEYDFANHGGQWLSDYIDL", "EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD"]
tada_scores = predict(sequence_list)
print(tada_scores)
{'QFNENSNIMQQQPLQGSFNPLLEYDFANHGGQWLSDYIDL': [['QFNENSNIMQQQPLQGSFNPLLEYDFANHGGQWLSDYIDL', 0.6370786]], 'EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD': [['EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD', 0.6459648]]}
```

#### Predicting TAD scores for sequences longer than 40 amino acids:

```python
sequence = "EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTDEFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD"
predictions = predict(sequence)
Warning: Not all sequences are 40 amino acids long.
Sequences shorter than 40 amino acids will be padded with a random selection of G and S evenly on the N and C terminus.
Sequences longer than 40 amino acids will be windowed to make sequences 40 amino acids in length with 39 overlapping amino acids.
print(predictions)
{'EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTDEFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD': [['EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD', 0.64596474], ['FSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTDE', 0.6526803], ['SPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTDEF', 0.6716454], ['PENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTDEFS', 0.68872523], ['ENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTDEFSP', 0.6902989], ['NSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTDEFSPE', 0.6911438], ['SSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTDEFSPEN', 0.6911325], ['SSSSWSSQESFLWEESFLHQSFDQSFLLSSPTDEFSPENS', 0.6796427], ['SSSWSSQESFLWEESFLHQSFDQSFLLSSPTDEFSPENSS', 0.6682477], ['SSWSSQESFLWEESFLHQSFDQSFLLSSPTDEFSPENSSS', 0.67283314], ['SWSSQESFLWEESFLHQSFDQSFLLSSPTDEFSPENSSSS', 0.6614274], ['WSSQESFLWEESFLHQSFDQSFLLSSPTDEFSPENSSSSS', 0.64761055], ['SSQESFLWEESFLHQSFDQSFLLSSPTDEFSPENSSSSSW', 0.65187407], ['SQESFLWEESFLHQSFDQSFLLSSPTDEFSPENSSSSSWS', 0.6707002], ['QESFLWEESFLHQSFDQSFLLSSPTDEFSPENSSSSSWSS', 0.6585511], ['ESFLWEESFLHQSFDQSFLLSSPTDEFSPENSSSSSWSSQ', 0.64087546], ['SFLWEESFLHQSFDQSFLLSSPTDEFSPENSSSSSWSSQE', 0.6390648], ['FLWEESFLHQSFDQSFLLSSPTDEFSPENSSSSSWSSQES', 0.5987145], ['LWEESFLHQSFDQSFLLSSPTDEFSPENSSSSSWSSQESF', 0.58188677], ['WEESFLHQSFDQSFLLSSPTDEFSPENSSSSSWSSQESFL', 0.6071577], ['EESFLHQSFDQSFLLSSPTDEFSPENSSSSSWSSQESFLW', 0.6604433], ['ESFLHQSFDQSFLLSSPTDEFSPENSSSSSWSSQESFLWE', 0.6806072], ['SFLHQSFDQSFLLSSPTDEFSPENSSSSSWSSQESFLWEE', 0.69611514], ['FLHQSFDQSFLLSSPTDEFSPENSSSSSWSSQESFLWEES', 0.6919587], ['LHQSFDQSFLLSSPTDEFSPENSSSSSWSSQESFLWEESF', 0.6967068], ['HQSFDQSFLLSSPTDEFSPENSSSSSWSSQESFLWEESFL', 0.6949902], ['QSFDQSFLLSSPTDEFSPENSSSSSWSSQESFLWEESFLH', 0.6817843], ['SFDQSFLLSSPTDEFSPENSSSSSWSSQESFLWEESFLHQ', 0.6620016], ['FDQSFLLSSPTDEFSPENSSSSSWSSQESFLWEESFLHQS', 0.64122045], ['DQSFLLSSPTDEFSPENSSSSSWSSQESFLWEESFLHQSF', 0.62519723], ['QSFLLSSPTDEFSPENSSSSSWSSQESFLWEESFLHQSFD', 0.6331634], ['SFLLSSPTDEFSPENSSSSSWSSQESFLWEESFLHQSFDQ', 0.64535403], ['FLLSSPTDEFSPENSSSSSWSSQESFLWEESFLHQSFDQS', 0.6383764], ['LLSSPTDEFSPENSSSSSWSSQESFLWEESFLHQSFDQSF', 0.6442358], ['LSSPTDEFSPENSSSSSWSSQESFLWEESFLHQSFDQSFL', 0.6482361], ['SSPTDEFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLL', 0.6431058], ['SPTDEFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLS', 0.638392], ['PTDEFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSS', 0.64072704], ['TDEFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSP', 0.6440916], ['DEFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPT', 0.648353], ['EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD', 0.6459648]]}
```
  
**Note**: You can turn off the warning message by setting ``verbose=False``.
  
**Note**: You can change the amount of overlap between the windows by setting the ``overlap_length`` parameter. The default is 39, which means that each sequence windows will overlap by 39 amino acids. This means that the windows will be 40 amino acids in length with 39 amino acids overlapping between each window. If you set the overlap length to 0, the windows will not overlap. If you set the overlap length to 20, the windows will overlap by 20 amino acids. Decreasing window value may result in you missing predictions for some subsequences if your sequence is not evenly divisible into 40 amino acid windows with that overlap amount. 

**Example with overlap_length**:
```python
sequence = "EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTDEFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD"
predictions = predict(sequence, overlap_length=20, verbose=False)
print(predictions)
{'EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTDEFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD': [['EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD', 0.6459648], ['EESFLHQSFDQSFLLSSPTDEFSPENSSSSSWSSQESFLW', 0.66044325], ['EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD', 0.6459648]]}
```

#### Predicting TAD scores for sequences shorter than 40 amino acids:

```python
sequence = "EFSPENSSSSSWSSQESFLW"
prediction = predict(sequence, safe_mode=False, verbose=False)
print(prediction)
{'EFSPENSSSSSWSSQESFLW': [['GSSGSGSSSGEFSPENSSSSSWSSQESFLWGSGSSSGSSG', 0.42451635]]}
```
  
**Note**: The sequence in the list is not the same as the input sequence. This is because the input sequence had to be padded to be 40 amino acids. In this case, the default padding was used. This evenly adds random G and S to each side of the sequence until it is 40 amino acids long. You can also change how the padding works. See below:

* ``pad`` (str): What amino acids to pad your sequence with if it is less than 40 amino acids. **Options are 'random' or 'GS'**. The 'random' option will pad your sequence with randomly chosen amino acids and the 'GS' option will pad your sequence with randomly selected G or S. Default is 'GS'.
* ``approach`` (str): How to pad the sequence if it is less than 40 amino acids. **Options are 'even', 'N', or 'C'**. The 'even' option will pad the sequence evenly on both sides, the 'N' option will pad the sequence on the N-terminus, and the 'C' option will pad the sequence on the C-terminus. Default is 'even'.


**Example with altered padding**:
```python
sequence = "EFSPENSSSSSWSSQ"
predictions = predict(sequence, safe_mode=False, pad='random', approach='N', verbose=False)
print(predictions)
{'EFSPENSSSSSWSSQ': [['KYPTSTWQCRRAKTLNPPREEVIFAEFSPENSSSSSWSSQ', 0.23243405]]}
```

## predict_from_fasta
  
The ``predict_from_fasta`` function lets you get TAD scores for sequences in a .fasta file.
  

```python
predict_from_fasta(path_to_fasta)
```
  
**Parameters**:
* ``path_to_fasta`` (str): The path to your .fasta file.
* ``overlap_length`` int: The amount of overlap to have between sequences when breaking up sequences longer than 40 amino acids. Default is 39.
* ``safe_mode`` (bool): If True, the function will raise an exception if the sequence is less than 40 amino acids. If False, the function will pad the sequence with 'X' amino acids to make the sequence 40 amino acids long. Default is True.
* ``pad`` (str): What amino acids to pad your sequence with if it is less than 40 amino acids. Options are 'random' or 'GS'. The 'random' option will pad your sequence with randomly chosen amino acids and the 'GS' option will pad your sequence with randomly selected G or S. Default is 'GS'.
* ``approach`` (str): How to pad the sequence if it is less than 40 amino acids. Options are 'even', 'N', or 'C'. The 'even' option will pad the sequence evenly on both sides, the 'N' option will pad the sequence on the N-terminus, and the 'C' option will pad the sequence on the C-terminus. Default is 'even'.
* ``verbose`` (bool): If True, the function will print out a warning when sequences are not all 40 amino acids. Default is True.

  
**Returns**:

The ``predict_from_fasta`` function returns a dictionary where the key is the name of the sequence as defined by the FASTA header and the value is a list of lists where the first element is the original sequence as in the .fasta file and the second element is a list of lists where each sublist contains the exact sequence used for the prediction and the value is the TADA score.


### Examples

Predicting TAD scores for sequences in a .fasta file:
```python
fasta_file = "example.fasta"
fasta_predictions = predict_from_fasta(fasta_file)
print(fasta_predictions)
{'0': ['QFNENSNIMQQQPLQGSFNPSSQESFLWEESFLLFDFSDT', [['QFNENSNIMQQQPLQGSFNPSSQESFLWEESFLLFDFSDT', 0.6412013]]], '1': ['EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTDEF', [['EFSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTD', 0.6459648], ['FSPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTDE', 0.6526802], ['SPENSSSSSWSSQESFLWEESFLHQSFDQSFLLSSPTDEF', 0.6716454]]]}
```

In the above example, the sequence associated with the .fasta header >1 is longer than 40 amino acids. Thus, we have multiple subsequences of length 40 amino acids that were used for each prediction.
  
**NOTE**: If there are any sequences under 40 amino acids in your fasta file, you must set ``safe_mode=False`` or it will not run any predictions.

**NOTE**: as with the ``predict`` function, you can also modify the ``pad`` and ``approach`` parameters for dealing with sequences under 40 amino acids. 

**Note**: as with the ``predict`` function, you can also modify the ``overlap_length`` for dealing with sequences greater than 40 amino acids. 

**Example showing altered pad, approach, overlap length**
```python
fasta_file = "example.fasta"
fasta_predictions = predict_from_fasta(fasta_file, safe_mode=False, pad='random', approach='N', overlap_length=20)
```

# Version history
## v0.1.0 (October 4, 2024)
* Initial release of TADA_T2


# other TADA_T2 info...

## TADA_T2 dependencies
Dependencies are:
* alphaPredict
* Tensorflow
* localcider
* numpy
* protfasta


### Copyright

Copyright (c) 2024, Ryan Emenecker Holehouse Lab WUSM


#### Acknowledgements
 
Project based on the 
[Computational Molecular Science Python Cookiecutter](https://github.com/molssi/cookiecutter-cms) version 1.10.
