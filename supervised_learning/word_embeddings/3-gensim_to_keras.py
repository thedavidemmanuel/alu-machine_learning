#!/usr/bin/env python3
"""
3-gensim_to_keras.py

This module provides a function to convert a gensim Word2Vec model to a Keras Embedding layer.
"""

from gensim.models import Word2Vec
from keras.layers import Embedding
import numpy as np


def gensim_to_keras(model):
    """
    Converts a gensim Word2Vec model to a Keras Embedding layer.

    Args:
        model (Word2Vec): A trained gensim Word2Vec model.

    Returns:
        keras.layers.Embedding: A Keras Embedding layer with weights from the Word2Vec model.
    """
    # Get the number of words and the embedding dimension
    vocab_size = len(model.wv.vocab)
    embedding_dim = model.vector_size

    # Create a word to index mapping
    word_to_idx = {word: idx for idx, word in enumerate(model.wv.index2word)}

    # Initialize the embedding matrix
    embedding_matrix = np.zeros((vocab_size, embedding_dim))

    # Populate the embedding matrix
    for word, idx in word_to_idx.items():
        embedding_matrix[idx] = model.wv[word]

    # Create Keras Embedding layer
    embedding_layer = Embedding(input_dim=vocab_size,
                                output_dim=embedding_dim,
                                weights=[embedding_matrix],
                                trainable=True)

    return embedding_layer
