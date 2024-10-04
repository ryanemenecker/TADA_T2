# various utilities
import random

def sliding_window(s: str, window_length: int, overlap: int) -> list:
    """
    Generates a list of substrings using a sliding window approach with specified overlap.

    Parameters:
    s (str): The input string.
    window_length (int): The length of the window (i.e., length of each substring).
    overlap (int): The number of characters that should overlap between consecutive substrings.

    Returns:
    list: A list of substrings of length `window_length` with specified overlap.
    """
    if window_length > len(s) or window_length <= 0:
        raise ValueError("Window length must be a positive integer and less than or equal to the length of the input string.")
    
    if overlap < 0 or overlap >= window_length:
        raise ValueError("Overlap must be a non-negative integer less than the window length.")
    
    step = window_length - overlap
    return [s[i:i + window_length] for i in range(0, len(s) - window_length + 1, step)]


def pad_sequence(input_sequence, pad='GS', 
                    objective_length=40,
                    approach='even'):
    '''
    Function to pad a sequence less than 40 amino acids. 

    Parameters
    ----------
    input_sequence : str
        The input sequence to pad.
    pad : str
        The approach to pad your sequence. 
        Options are 'random' or 'GS'.
        GS will pad both sides of your sequence with GS.
        Random will pad both sides of your sequence with random amino acids.
    objective_length : int
        The length of the sequence to pad to.
    approach : str
        The approach to pad your sequence. 
        Options are 'even' or 'N' or 'C'.
        Even will pad the sequence evenly on both sides.
        'N' will pad the sequence only at the N-terminus.
        'C' will pad the sequence only at the C-terminus.

    Returns
    -------
    str
        The padded sequence.
    '''
    if len(input_sequence) >= objective_length:
        return input_sequence
    if pad not in ['random', 'GS']:
        raise ValueError('Pad must be either random or GS.')
    if approach not in ['even', 'N', 'C']:
        raise ValueError('Approach must be either even, N, or C.')
    if objective_length < 0:
        raise ValueError('Objective length must be a positive integer.')
    num_to_pad = objective_length - len(input_sequence)
    amino_acids=['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T','V', 'W', 'Y']
    if pad=='random':
        padding=[random.choice(amino_acids) for _ in range(num_to_pad)]
    else:
        padding=[random.choice(['G', 'S']) for _ in range(num_to_pad)]
    if approach=='even':
        num_N = num_to_pad // 2
        num_C = num_to_pad - num_N
        return ''.join(padding[:num_N]) + input_sequence + ''.join(padding[num_N:])
    if approach=='N':
        return ''.join(padding)+input_sequence 
    if approach=='C':
        return input_sequence+''.join(padding)

def make_sequences_constant_length(sequence_list, objective_length=40, 
                                        overlap_length=39, pad='GS', approach='even'):
    '''
    Function to make all sequences a constant 40 amino acids using the
    pad_sequence() and sliding_window() functions as outlined above.

    Parameters
    ----------
    sequence_list : list
        The list of sequences to pad or to make windowed seqs of.
    objective_length : int
        The length of the sequence to pad to.
    overlap_length : int
        The length of the overlap between sequences.
    pad : str
        The approach to pad your sequence. 
        Options are 'random' or 'GS'.
        GS will pad both sides of your sequence with GS.
        Random will pad both sides of your sequence with random amino acids.
    approach : str
        The approach to pad your sequence. 
        Options are 'even' or 'N' or 'C'.
        Even will pad the sequence evenly on both sides.
        'N' will pad the sequence only at the N-terminus.
        'C' will pad the sequence only at the C-terminus.

    Returns
    -------
    dict:
        A dictionary with the sequence as the key and the padded or windowed sequences as the values.
    '''
    over_length = [seq for seq in sequence_list if len(seq)>objective_length]
    under_length = [seq for seq in sequence_list if len(seq)<objective_length]
    at_length = [seq for seq in sequence_list if len(seq)==objective_length]
    padded_seqs = [pad_sequence(seq, pad=pad, objective_length=objective_length, approach=approach) for seq in under_length]
    windowed_seqs = [sliding_window(seq, objective_length, overlap_length) for seq in over_length]
    over_length_dict = dict(zip(over_length, windowed_seqs))
    under_length_dict = dict(zip(under_length, padded_seqs))
    at_length_dict = dict(zip(at_length, [seq for seq in at_length]))
    return {**over_length_dict, **under_length_dict, **at_length_dict}


def map_sequences_to_prediction(sequence_dict):
    '''
    Function that takes in the sequence dict and then returns
    a list of all the values in the dict and a dict for 
    all keys in the dict with index numbers matched to the values
    in the list.

    Parameters
    ----------
    sequence_dict : dict
        A dictionary with the sequence as the key and the padded or windowed sequences as the values.

    Returns
    -------
    list, dict:
        a list of sequences and a dictionary with the sequence as the key index values for every sequence
        that match to that sequence.
    '''
    seq_list=[]
    dict_to_seq={}
    seq_index=0
    for s in sequence_dict:
        if isinstance(sequence_dict[s], list):
            seq_list.extend(sequence_dict[s])
            dict_to_seq[s]=list(range(seq_index, seq_index+len(sequence_dict[s])))
            seq_index+=len(sequence_dict[s])
        else:
            seq_list.append(sequence_dict[s])
            dict_to_seq[s]=[seq_index]
            seq_index+=1
    return seq_list, dict_to_seq


def verbose_warning_message(overlap_length, pad, approach):
    '''
    Function to make a warning message when running in verbose.
    
    Parameters
    ----------
    overlap_length : int
        The length of the overlap between sequences.
    pad : str
        The approach to pad your sequence. 
        Options are 'random' or 'GS'.
        GS will pad both sides of your sequence with GS.
        Random will pad both sides of your sequence with random amino acids.
    approach : str
        The approach to pad your sequence. 
        Options are 'even' or 'N' or 'C'.
        Even will pad the sequence evenly on both sides.
        'N' will pad the sequence only at the N-terminus.
        'C' will pad the sequence only at the C-terminus.
    '''
    if pad=='GS':
        pad_message='random selection of G and S'
    else:
        pad_message='random selection of all amino acids'
    if approach=='even':
        approach_message = 'evenly on the N and C terminus'
    elif approach=='N':
        approach_message = 'only at the N terminus'
    else:
        approach_message = 'only at the C terminus'
    warning_message=f'Warning: Not all sequences are 40 amino acids long.\nSequences shorter than 40 amino acids will be padded with a {pad_message} {approach_message}.\nSequences longer than 40 amino acids will be windowed to make sequences 40 amino acids in length with {overlap_length} overlapping amino acids.'
    return warning_message
