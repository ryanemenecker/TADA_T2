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

