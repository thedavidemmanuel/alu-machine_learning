#!/usr/bin/env python3
'''
    Script that defines a function def bi_rnn(bi_cell, X, h_0, h_t):
    that performs forward propagation for a bidirectional RNN:
'''

import numpy as np

def bi_rnn(bi_cell, X, h_0, h_T):
    '''
        Function that performs forward propagation for a bidirectional RNN

        parameters:
            bi_cell: an instance of BidirectionalCell
            X: data
            h_0: initial hidden state
            h_T: terminal hidden state

        return:
            H: all hidden states
            Y: all outputs
    '''

    t, m, i = X.shape
    _, h = h_0.shape  # h_0 shape is (m, h)
    H = np.zeros((t, m, 2*h))
    Y = np.zeros((t, m, bi_cell.by.shape[1]))  # Assuming bi_cell.by gives output dimension

    h_forward = h_0
    h_backward = h_T

    for step in range(t):
        h_forward, _ = bi_cell.forward(h_forward, X[step])
        h_backward, _ = bi_cell.backward(h_backward, X[t-1-step])
        
        H[step] = np.concatenate((h_forward, h_backward), axis=1)
        Y[step] = bi_cell.output(H[step])

    return H, Y