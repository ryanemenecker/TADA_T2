'''
Code for the ML Model. Modified to be compaitble with Tensorflow2 along
with a few other optimizations. 
Credit to Lisa (see https://github.com/LisaVdB/TADA)
for original implementation of the model.
'''
import importlib.resources

from tensorflow import nn, matmul, reduce_sum, constant
from tensorflow.keras import layers, regularizers, metrics, models, optimizers
from tensorflow.keras.models import Sequential

class Attention(layers.Layer):
    '''
    Custom Attention class. Updated to be a bit more 
    efficient and compatible with Tensorflow2. 
    '''
    def __init__(self, return_sequences=True, **kwargs):
        super(Attention, self).__init__(**kwargs)
        self.return_sequences = return_sequences

    def build(self, input_shape):
        # Weight matrix for attention
        self.W = self.add_weight(
            name="att_weight", shape=(input_shape[-1], 1), 
            initializer="glorot_uniform", trainable=True
        )
        # Bias term
        self.b = self.add_weight(
            name="att_bias", shape=(input_shape[1], 1), 
            initializer="zeros", trainable=True
        )
        super(Attention, self).build(input_shape)

    def call(self, inputs):
        # Compute the attention scores
        e = nn.tanh(matmul(inputs, self.W) + self.b)
        # Softmax over the attention scores along the time axis
        a = nn.softmax(e, axis=1)
        # Apply attention weights to the input
        output = inputs * a
        
        if self.return_sequences:
            return output
        # If not returning sequences, sum the weighted input along the time axis
        return reduce_sum(output, axis=1)

    def get_config(self):
        config = super().get_config()
        config.update({"return_sequences": self.return_sequences})
        return config


class TadaModel:
    def __init__(self, 
                 shape=(36,42), 
                 kernel_size=2, 
                 filters=100, 
                 activation_function='gelu', 
                 learning_rate=1e-3, 
                 dropout=0.3, 
                 bilstm_output_size=100):
        """
        Initialize the CustomModel and build the architecture.
        """
        self.shape = shape
        self.kernel_size = kernel_size
        self.filters = filters
        self.activation_function = activation_function
        self.learning_rate = learning_rate
        self.dropout = dropout
        self.bilstm_output_size = bilstm_output_size
        self.model = self.create_model()

    def create_model(self):
        """
        Define the NN architecture.
        """
        model = Sequential()
        
        # Add an explicit Input layer
        model.add(layers.Input(shape=self.shape))

        model.add(layers.Conv1D(filters=self.filters, 
                                 kernel_size=self.kernel_size,
                                 padding='valid',
                                 activation=self.activation_function,
                                 strides=1,
                                 kernel_regularizer=regularizers.l1_l2(l1=1e-5, l2=1e-4)))
        
        model.add(layers.Dropout(self.dropout)) 
        model.add(layers.Conv1D(filters=self.filters,
                                 kernel_size=self.kernel_size,
                                 padding='valid',
                                 activation=self.activation_function,
                                 strides=1))
        model.add(layers.Dropout(self.dropout))
        
        model.add(Attention())  # Custom attention layer
        
        model.add(layers.Bidirectional(layers.LSTM(self.bilstm_output_size, return_sequences=True)))  # Bidirectional LSTM
        model.add(layers.Bidirectional(layers.LSTM(self.bilstm_output_size))) 
        model.add(layers.Dense(2, activation="softmax"))  # Output layer
        
        return model

