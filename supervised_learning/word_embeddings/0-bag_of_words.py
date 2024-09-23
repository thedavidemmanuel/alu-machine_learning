#!/usr/bin/env python3
"""
0-bag_of_words.py

This module provides a function to create a bag of words embedding matrix.
"""

import numpy as np
import string


def bag_of_words(sentences, vocab=None):
    """
    Creates a bag of words embedding matrix.

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
        # Handle possessive 's (e.g., "children's" -> "children")
        sentence = sentence.replace("'s", "")
        # Remove punctuation and convert to lowercase
        translator = str.maketrans('', '', string.punctuation)
        clean_sentence = sentence.translate(translator).lower()
        tokens = clean_sentence.split()
        tokenized_sentences.append(tokens)

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

    # Initialize embeddings matrix
    embeddings = np.zeros((len(sentences), len(features)), dtype=int)

    # Populate embeddings matrix
    for i, tokens in enumerate(tokenized_sentences):
        for word in tokens:
            if word in word_to_idx:
                embeddings[i][word_to_idx[word]] += 1

    return embeddings, features
