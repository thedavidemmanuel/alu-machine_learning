#!/usr/bin/env python3
"""Variational Autoencoder"""

import tensorflow.keras as keras
import tensorflow.keras.backend as K


def autoencoder(input_dims, hidden_layers, latent_dims):
    """
    Creates a variational autoencoder
    Args:
        input_dims: integer containing the dimensions of the model input
        hidden_layers: list containing the number of nodes for each hidden
                      layer in the encoder, respectively
        latent_dims: integer containing the dimensions of the latent space
                    representation
    Returns: encoder, decoder, auto
    """
    # Encoder
    X_input = keras.Input(shape=(input_dims,))
    
    # Hidden layers for encoder
    Y_prev = X_input
    for units in hidden_layers:
        Y_prev = keras.layers.Dense(units=units, activation='relu')(Y_prev)
    
    # Latent space parameters
    z_mean = keras.layers.Dense(units=latent_dims, activation=None,
                              name='z_mean')(Y_prev)
    z_log_sigma = keras.layers.Dense(units=latent_dims, activation=None,
                                   name='z_log_sigma')(Y_prev)
    
    def sampling(args):
        """Reparameterization trick"""
        z_mean, z_log_sigma = args
        batch = K.shape(z_mean)[0]
        dim = K.int_shape(z_mean)[1]
        epsilon = K.random_normal(shape=(batch, dim))
        return z_mean + K.exp(z_log_sigma / 2) * epsilon
    
    # Reparameterization layer
    z = keras.layers.Lambda(sampling,
                          output_shape=(latent_dims,),
                          name='z')([z_mean, z_log_sigma])
    
    # Create encoder model
    encoder = keras.Model(X_input, [z, z_mean, z_log_sigma], name='encoder')
    
    # Decoder
    X_decode = keras.Input(shape=(latent_dims,))
    
    # Hidden layers for decoder (reverse order)
    Y_prev = X_decode
    for units in reversed(hidden_layers):
        Y_prev = keras.layers.Dense(units=units, activation='relu')(Y_prev)
    
    # Output layer
    output = keras.layers.Dense(units=input_dims,
                              activation='sigmoid')(Y_prev)
    
    # Create decoder model
    decoder = keras.Model(X_decode, output, name='decoder')
    
    # Full autoencoder
    outputs = decoder(encoder(X_input)[0])
    auto = keras.Model(X_input, outputs, name='autoencoder')
    
    # Custom VAE loss
    reconstruction_loss = keras.losses.binary_crossentropy(X_input, outputs)
    reconstruction_loss *= input_dims
    kl_loss = 1 + z_log_sigma - K.square(z_mean) - K.exp(z_log_sigma)
    kl_loss = K.sum(kl_loss, axis=-1)
    kl_loss *= -0.5
    vae_loss = K.mean(reconstruction_loss + kl_loss)
    auto.add_loss(vae_loss)
    
    # Compile model
    auto.compile(optimizer='adam')
    
    return encoder, decoder, auto
