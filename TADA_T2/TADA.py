"""Provide the primary functions."""

import protfasta
import os

from TADA_T2.backend.predictor import predict_tada as _predict_tada
from TADA_T2.backend.utils import make_sequences_constant_length, map_sequences_to_prediction, verbose_warning_message


def predict(sequences, overlap_length=39, pad='GS', approach='even', verbose=True, safe_mode=True):
    """
    Predicts TAD scores for a sequence or a list sequences.

    Parameters
    ----------
    sequences : str or list
        string of single sequence or list of sequences to predict TADA scores for.

    overlap_length : int
        The length of the overlap between sequences.
        Default is 39
    
    pad : str
        The approach to pad your sequence. 
        Options are 'random' or 'GS'.
        GS will pad both sides of your sequence with GS.
        Random will pad both sides of your sequence with random amino acids.
        Default is 'GS'.
    
    approach : str
        The approach to pad your sequence. 
        Options are 'even' or 'N' or 'C'.
        Even will pad the sequence evenly on both sides.
        'N' will pad the sequence only at the N-terminus.
        'C' will pad the sequence only at the C-terminus.
        Default is 'even'.

    verbose : bool
        whether to warn user when sequence lengths are not 40 amino acids.

    safe_mode : bool
        whether to run the function in safe mode. Safe mode will raise an exception
        if any sequences are under 40 amino acids. Default is True.

    Returns
    -------
    dict
        A dict with the sequence as the key and the scores as the values.
    """
    if isinstance(sequences, str):
        sequences=[sequences]

    # get sequence lengths
    seq_lengths=[len(seq) for seq in sequences]
    if safe_mode:
        # check if all sequences are over 40 amino acids long   
        if not all([length>=40 for length in seq_lengths]):
            raise ValueError('Not all sequences are 40 amino acids long. TADA was not made for sequences under 40 amino acids. You can still make these predictions by setting safe_mode=False, but use this feature with extreme caution!.')        
    if any([length!=40 for length in seq_lengths]):
        if verbose:
            message = verbose_warning_message(overlap_length=overlap_length, pad=pad, approach=approach)
            print(str(message))
    seq_dict=make_sequences_constant_length(sequences, 
                                            overlap_length=overlap_length, 
                                            pad=pad, approach=approach)
    padded_or_trimmed_seqs, map_to_predictions=map_sequences_to_prediction(seq_dict)
    predictions=_predict_tada(padded_or_trimmed_seqs)
    # holds final sequences
    final_dict={}
    # map the indices in the predictions to the original sequences
    for seq, indices in map_to_predictions.items():
        final_dict[seq]=[[padded_or_trimmed_seqs[index],predictions[index]] for index in indices]
    return final_dict


def predict_from_fasta(path_to_fasta, overlap_length=39, pad='GS', 
                        approach='even', verbose=True, safe_mode=True):
    """
    Predicts TAD scores for sequences in a .fasta file

    Parameters
    ----------
    path_to_fasta : str
        path to a .fasta file as a string

    overlap_length : int
        The length of the overlap between sequences.
        Default is 39
    
    pad : str
        The approach to pad your sequence. 
        Options are 'random' or 'GS'.
        GS will pad both sides of your sequence with GS.
        Random will pad both sides of your sequence with random amino acids.
        Default is 'GS'.
    
    approach : str
        The approach to pad your sequence. 
        Options are 'even' or 'N' or 'C'.
        Even will pad the sequence evenly on both sides.
        'N' will pad the sequence only at the N-terminus.
        'C' will pad the sequence only at the C-terminus.
        Default is 'even'.

    safe_mode : bool
        Whether to run the function in safe mode. Safe mode will raise an exception
        if any sequences are under 40 amino acids. Default is True.

    verbose : bool
        whether to warn user when sequence lengths are not 40 amino acids.

    Returns
    -------
    dict
        Dict with name of the sequence from the fasta file as the key
        and then a list as the values where the first element is the sequence
        and the second element is the TADA score. 
    """
    # make sure that path is valid
    if not os.path.exists(path_to_fasta):
        raise ValueError('Path does not exist.')        

    # read in sequences
    sequences=protfasta.read_fasta(path_to_fasta, invalid_sequence_action='convert')
    seq_names=list(sequences.keys())
    sequences=list(sequences.values())

    if safe_mode:
        # check if all sequences are over 40 amino acids long
        seq_lengths=[len(seq) for seq in sequences]
        if not all([length>=40 for length in seq_lengths]):
            raise ValueError('Not all sequences are 40 amino acids long. TADA was not made for sequences under 40 amino acids. You can still make these predictions by setting safe_mode=False, but use this feature with extreme caution!.')
    
    # run predictions
    predictions=predict(sequences, overlap_length=overlap_length, 
                        pad=pad, approach=approach, verbose=verbose,
                        safe_mode=safe_mode)

    # map sequence names to predictions
    final_dict={}
    for i, s in enumerate(seq_names):
        final_dict[s]=[sequences[i], predictions[sequences[i]]]
    return final_dict
