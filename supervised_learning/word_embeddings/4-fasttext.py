#!/usr/bin/env python3
"""
4-fasttext.py

This module provides a function to create and train a gensim FastText model.
"""

from gensim.models import FastText


def fasttext_model(sentences, size=100, min_count=5, negative=5,
                  window=5, cbow=True, iterations=5, seed=0, workers=1):
    """
    Creates and trains a gensim FastText model.

    Args:
        sentences (list of list of str): List of tokenized sentences to be trained on.
        size (int, optional): Dimensionality of the embedding layer. Defaults to 100.
        min_count (int, optional): Minimum number of occurrences of a word for use in training. Defaults to 5.
        negative (int, optional): Size of negative sampling. Defaults to 5.
        window (int, optional): Maximum distance between the current and predicted word within a sentence. Defaults to 5.
        cbow (bool, optional): If True, use CBOW; else, Skip-gram. Defaults to True.
        iterations (int, optional): Number of iterations to train over. Defaults to 5.
        seed (int, optional): Seed for the random number generator. Defaults to 0.
        workers (int, optional): Number of worker threads to train the model. Defaults to 1.

    Returns:
        FastText: The trained FastText model.
    """
    # Determine training algorithm
    sg = 0 if cbow else 1

    # Initialize and train FastText model
    model = FastText(sentences=sentences,
                     size=size,
                     window=window,
                     min_count=min_count,
                     workers=workers,
                     sg=sg,
                     negative=negative,
                     seed=seed,
                     iter=iterations)

    return model
