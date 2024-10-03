"""Provide the primary functions."""

import protfasta
from TADA_T2.backend.predictor import predict_tada

def predict(sequences, return_dict=False):
    """
    Predicts TAD scores for a sequence or a list sequences.

    Parameters
    ----------
    sequences : str or list
        string of single sequence or list of sequences to predict TADA scores for.

    return_dict : bool
        Whether to return a dictionary with the sequence as the key and the 
        prediction score as the value.

    Returns
    -------
    list
        List of TADA scores for each input sequence.
    """
    if isinstance(sequences, str):
        sequences=[sequences]

    predictions = predict_tada(sequences)

    if return_dict:
        predictions=dict(zip(sequences, predictions))
    return predictions


def predict_from_fasta(path_to_fasta):
    """
    Predicts TAD scores for sequences in a .fasta file

    Parameters
    ----------
    path_to_fasta : str
        path to a .fasta file as a string

    Returns
    -------
    dict
        Dict with name of the sequence from the fasta file as the key
        and then a list as the values where the first element is the sequence
        and the second element is the TADA score. 
    """
    sequences=protfasta.read_fasta(path_to_fasta, invalid_sequence_action='convert')
    seq_names=list(sequences.keys())
    sequences=list(sequences.values())
    predictions=predict_tada(sequences)
    seqs_predictions=list(zip(sequences,predictions))
    return dict(zip(seq_names,seqs_predictions))

