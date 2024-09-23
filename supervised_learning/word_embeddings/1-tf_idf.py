#!/usr/bin/env python3
"""
1-tf_idf.py

This module provides a function to create a TF-IDF embedding matrix.
"""

import numpy as np
import string
from math import log


def tf_idf(sentences, vocab=None):
    """
    Creates a TF-IDF embedding matrix.

    Args:
        sentences (list of str): List of sentences to analyze.
        vocab (list of str, optional): List of vocabulary words to use for the analysis.
            If None, all words within sentences are used.

    Returns:
        tuple:
            embeddings (numpy.ndarray): Embedding matrix of shape (s, f),
                where s is the number of sentences and f is the number of features.
            features (list of str): List of features used for embeddings.
    """
    # Tokenize sentences
    tokenized_sentences = []
    for sentence in sentences:
        # Remove punctuation and lowercase
        translator = str.maketrans('', '', string.punctuation)
        clean_sentence = sentence.translate(translator).lower()
        tokens = clean_sentence.split()
        tokenized_sentences.append(tokens)

    num_sentences = len(sentences)

    # Build vocabulary if not provided
    if vocab is None:
        vocab_set = set()
        for tokens in tokenized_sentences:
            vocab_set.update(tokens)
        features = sorted(list(vocab_set))
    else:
        features = sorted(vocab)

    # Create word to index mapping
    word_to_idx = {word: idx for idx, word in enumerate(features)}
    f = len(features)

    # Initialize term frequency matrix
    tf = np.zeros((num_sentences, f), dtype=float)

    # Populate term frequency matrix
    for i, tokens in enumerate(tokenized_sentences):
        for word in tokens:
            if word in word_to_idx:
                tf[i][word_to_idx[word]] += 1

    # Compute document frequency
    df = np.zeros(f, dtype=int)
    for tokens in tokenized_sentences:
        unique_tokens = set(tokens)
        for word in unique_tokens:
            if word in word_to_idx:
                df[word_to_idx[word]] += 1

    # Compute inverse document frequency
    idf = np.array([log((num_sentences) / (df_i)) if df_i != 0 else 0.0 for df_i in df])

    # Compute TF-IDF
    tf_idf = tf * idf

    # Normalize TF-IDF vectors to unit vectors
    norm = np.linalg.norm(tf_idf, axis=1, keepdims=True)
    # To avoid division by zero
    norm[norm == 0] = 1.0
    tf_idf_normalized = tf_idf / norm

    return tf_idf_normalized, features
