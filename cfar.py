# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 10:40:56 2020

@author: student6
"""

import numpy as np
import matplotlib.pyplot as plt
from FFT import mySpectrum
from readDCA1000_xWR12xx import readDCA1000
import scipy.constants

S = 100 * 10 ** 12

def detect_peaks(x, num_train, num_guard, rate_fa):
    """
    

    Parameters
    ----------
    x : signal
    num_train : broj trening celija
    num_guard : broj zastitnih celija
    rate_fa : ucestanost laznih detekcija

    Returns
    -------
    peak_idx : niz detektovanih meta

    """

    num_cells = x.size
    num_train_half = round(num_train / 2)
    num_guard_half = round(num_guard / 2)
    num_side = num_train_half + num_guard_half
 
    alpha = 0.09 * num_train * (rate_fa ** (-1 / num_train) - 1) # threshold factor
    
    peak_idx = []
    for i in range(num_side, num_cells - num_side):
        
        if i != i-num_side + np.argmax(x[i-num_side : i+num_side+1]): 
            continue
        
        sum1 = np.sum(x[i-num_side : i+num_side+1])
        sum2 = np.sum(x[i-num_guard_half : i+num_guard_half+1]) 
        p_noise = (sum1 - sum2) / num_train 
        threshold = alpha * p_noise
        
        if x[i] > threshold and x[i] > -20: 
            peak_idx.append(i)
    
    peak_idx = np.array(peak_idx, dtype=int)
    
    return peak_idx

if __name__ == '__main__':

    data = readDCA1000('22.9/2/adc_data.bin')
    y = np.zeros((256, ), dtype = complex)
    
    for i in range(0, 4):
        for j in range(0, 128):
            y += data[i, j * 256 : (j + 1) * 256]
    
    #y = data[0, :256]
    
    
    amp, phaseDb, x = mySpectrum(y, 10 * pow(10, 6) * scipy.constants.c / 2 / S, 512)
    
    # Detect peaks
    peak_idx = detect_peaks(amp, num_train=20, num_guard=8, rate_fa=1e-3)
    print("peak_idx =", peak_idx)
    
    plt.grid()
    
    plt.plot(x, amp)
    plt.plot(x[peak_idx], amp[peak_idx], 'rD')
    
    plt.xlabel('d[m]')
    plt.ylabel('amp[dB]')
    
    plt.figure()
    
    plt.plot(x[peak_idx], np.ones(np.shape(amp[peak_idx])), 'ro')
    plt.grid()
    
    plt.show()
    
    plt.xlabel('d[m]')