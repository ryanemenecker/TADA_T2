'''
Code for the encoding features. Modified to be compaitble with Tensorflow2 along
with optimizations to make it faster.
'''
from copy import deepcopy
import importlib.resources

import numpy as np
import alphaPredict as alpha
from localcider.sequenceParameters import SequenceParameters


def get_scaler_path():
    ''' 
    Quick function to get back the path to the model.
    '''
    scaler_arr_path = importlib.resources.files('TADA_T2.data') / 'scaler_metric.npy'
    return str(scaler_arr_path)


def create_features(sequences, SEQUENCE_WINDOW = 5, STEPS = 1, LENGTH = 40, PROPERTIES = 42):
    '''
    Function to create features for the model. Updated to improve readability.

    Parameters
    ----------
    sequences : List. 
        List of sequences with max length of 40AA.
    SEQUENCE_WINDOW : Int, optional
        The window that the sequence is scanned over.
    STEPS : Int, optional
        The size of steps. 
    LENGTH : int, optional
        The length of the sequences. 
    PROPERTIES : Int, optional
        The number of properties
    
    Returns
    -------
    features : Processed input data for model
    '''

    aliphatics_set = set(['I', 'V', 'L', 'A'])
    aromatics_set = set(['W', 'F', 'Y'])
    branching_set = set(['V', 'I', 'T'])
    charged_set = set(['K', 'R', 'H', 'D', 'E'])
    negatives_set = set(['D', 'E'])
    phosphorylatables_set = set(['S', 'T', 'Y'])
    polars_set = set(['R', 'K', 'D', 'E', 'Q', 'N', 'Y'])
    hydrophobics_set = set(['W', 'F', 'L', 'V', 'I', 'C', 'M'])
    positives_set = set(['K', 'R', 'H'])
    sulfurcontaining_set = set(['M', 'C'])
    tinys_set = set(['G', 'A', 'S', 'P'])
    amino_acids = ['R', 'K', 'D', 'E', 'Q', 'N', 'H', 'S', 'T', 'Y', 'C', 'W', 'M', 'A', 'I', 'L', 'F', 'V', 'P', 'G']

    features = []        
    for sequence in sequences:
        SEQUENCE_LENGTH = len(sequence)
        SeqOb = SequenceParameters(sequence)
        kappa = np.full(int((SEQUENCE_LENGTH-SEQUENCE_WINDOW)/STEPS+1), SeqOb.get_kappa())
        omega = np.full(int((SEQUENCE_LENGTH-SEQUENCE_WINDOW)/STEPS+1), SeqOb.get_Omega())
        
        # make subseqs.
        sub_seq = [sequence[STEPS * j:STEPS * j + SEQUENCE_WINDOW] for j in range((SEQUENCE_LENGTH - SEQUENCE_WINDOW) // STEPS + 1)]
        one = np.array([sum(aa in aliphatics_set for aa in seq) for seq in sub_seq])
        two = np.array([sum(aa in aromatics_set for aa in seq) for seq in sub_seq])
        three = np.array([sum(aa in branching_set for aa in seq) for seq in sub_seq])
        four = np.array([sum(aa in charged_set for aa in seq) for seq in sub_seq])
        five = np.array([sum(aa in negatives_set for aa in seq) for seq in sub_seq])
        six = np.array([sum(aa in phosphorylatables_set for aa in seq) for seq in sub_seq])
        seven = np.array([sum(aa in polars_set for aa in seq) for seq in sub_seq])
        eight = np.array([sum(aa in hydrophobics_set for aa in seq) for seq in sub_seq])
        nine = np.array([sum(aa in positives_set for aa in seq) for seq in sub_seq])
        ten = np.array([sum(aa in sulfurcontaining_set for aa in seq) for seq in sub_seq])
        eleven = np.array([sum(aa in tinys_set for aa in seq) for seq in sub_seq])
        sstructure = np.array([sum(alpha.predict(seq)) / len(seq) for seq in sub_seq])
        count_20 = np.array([[s.count(aa) for s in sub_seq] for aa in amino_acids])
        
        # turn subseqs into SeqObs.
        sub_seq = [SequenceParameters(seq) for seq in sub_seq]
        hydropathy = np.array([seq.get_mean_hydropathy() for seq in sub_seq])
        hydropathy_ww = np.array([seq.get_WW_hydropathy() for seq in sub_seq])
        ncpr = np.array([seq.get_NCPR() for seq in sub_seq])
        promoting = np.array([seq.get_fraction_disorder_promoting() for seq in sub_seq])
        fcr = np.array([seq.get_FCR() for seq in sub_seq])
        charge = np.array([seq.get_mean_net_charge() for seq in sub_seq])
        negative = np.array([seq.get_fraction_negative() for seq in sub_seq])
        positive = np.array([seq.get_fraction_positive() for seq in sub_seq])

        # make array of features.
        x = np.array([kappa, omega, hydropathy, hydropathy_ww, ncpr, promoting, fcr, charge, negative, positive,
                     one, two, three, four, five, six, seven, eight, nine, ten, eleven, sstructure])
        # concatenate x and count_20
        x = np.concatenate([x, count_20])
        # do padding 
        padded_x = np.zeros((PROPERTIES, (LENGTH - SEQUENCE_WINDOW) // STEPS + 1))
        padded_x[:x.shape[0], :x.shape[1]] = x
        # append to features
        features.append(padded_x)

    features = np.array(features)
    return np.transpose(features, (0, 2, 1))


def scale_features_predict(features: np.ndarray, SEQUENCE_WINDOW=5, STEPS=1, LENGTH=40) -> np.ndarray:
    '''
    Function to scale the features for prediction. Updated to improve readability.

    Parameters
    ----------
    features : np.ndarray
        Takes the output of create_features() and scales the values per feature column.

    Returns
    -------
    scaled_array_copy : np.ndarray
        Scaled feature array ready for prediction.
    '''

    scaled_array_copy = deepcopy(features)
    n, m = features[0].shape
    scaler_metric = np.load(str(get_scaler_path()))


    # Precompute the length for reshaping
    num_steps = int((LENGTH - SEQUENCE_WINDOW) / STEPS + 1)
    
    for i in range(m):
        # Load StandardScaler and MinMaxScaler parameters for each feature
        mean_, var_, scale_, n_samples_seen_ = scaler_metric[i, :4]
        min_, data_min_, data_max_, scale2_, n_samples_seen2_, data_range_ = scaler_metric[i, 4:10]
        
        # Normalize using StandardScaler metrics
        results = (scaled_array_copy[:, :, i] - mean_) / scale_

        # Apply MinMaxScaler metrics
        results = (results - data_min_) / data_range_

        # Reshape back to original dimensions
        results = results.reshape((len(features), num_steps))
        scaled_array_copy[:, :, i] = results

    return scaled_array_copy


