'''
code for predictor.
'''
import importlib.resources

# package imports
from TADA_T2.backend.features import create_features, scale_features_predict
from TADA_T2.backend.model import TadaModel

def get_model_path():
    ''' 
    Quick function to get back the path to the model.
    '''
    model_weights_path = importlib.resources.files('TADA_T2.data') / 'tada.14-0.02.hdf5'
    return str(model_weights_path)

def predict_tada(sequences, return_both_values=False):
    '''
    Parameters
    ----------
    sequences : list
        List of sequences to predict TADA scores for.

    return_both_values : bool
        Whether to return both values. The model returns two values, one for each category
        (is a TAD or is not a TAD). If True, both values are returned. If False, only the first
        value is returned. Default is False.
        The first value matches the 'TAD' scores that are used in the TADA paper.

    Returns
    -------
    list
        List of TADA scores for each input sequence.
    '''
    if not isinstance(sequences, list):
        raise Exception('Sequences must be input as a list!')

    # Defines the sequence window size and steps (stride length). Change values if needed.
    SEQUENCE_WINDOW = 5
    STEPS = 1
    LENGTH = 40

    # get scaled features
    features_scaled = scale_features_predict(create_features(sequences, SEQUENCE_WINDOW, STEPS))
    # Load the model
    model = TadaModel().create_model()
    # Load weights
    model.load_weights(str(get_model_path()))
    # run predictions
    predictions = model.predict(features_scaled, verbose=0)
    # return predictions. 
    if return_both_values:
        return predictions
    return [i[0] for i in predictions]
