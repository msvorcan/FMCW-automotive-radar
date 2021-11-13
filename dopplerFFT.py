# -*- coding: utf-8 -*-
"""
Created on Thu Sep 10 14:23:30 2020

@author: student6
"""

import scipy.fftpack
import numpy as np
import matplotlib.pyplot as plt

from readDCA1000_xWR12xx import readDCA1000


f = 77 * pow(10, 9)
fs = 10 * pow(10, 6)
S = 30 * pow(10, 12)
Tc =  40 * pow(10, -6)
idleTime = 50 * pow(10, -6)
LAMBDA = scipy.constants.c / f

numADCSamples = 256
numChirps = 128

def dopplerFFT(data, ant = 0):
    """
    

    Parameters
    ----------
    data : signal iz binarne datoteke 
    ant : Broj antene ciji podaci se obradjuju.
        The default is 0.

    Returns
    -------
    amp : 2-D matrica (range-doppler mapa)

    """
    amp = np.zeros((numChirps, numADCSamples), dtype = complex)
    amp2 = np.zeros((numChirps, numADCSamples), dtype = complex)
    
    for i in range(0, numChirps):
        amp1 = scipy.fft.fft(data[ant,
                             numADCSamples * i:numADCSamples * (i + 1)] * np.hamming(numADCSamples),
                             numADCSamples)
        amp2[i, :] = amp1
        
    for i in range(0, numADCSamples):
        amp1 = scipy.fft.fft(amp2[:, i] * np.hamming(numChirps), numChirps)
        amp[:, i] = np.fft.fftshift(amp1)
        
    amp = np.transpose(amp)

    return amp

def plot(data):
    """
    F-ja racuna doppler-FFT i crta na grafiku range-doppler mapu.

    Parameters
    ----------
    data : signal iz binarne datoteke

    Returns
    -------
    None.

    """
    
    amp0 = dopplerFFT(data, 0)
    amp1 = dopplerFFT(data, 1)
    amp2 = dopplerFFT(data, 2)
    amp3 = dopplerFFT(data, 3)
    
    amp = amp0 + amp1 + amp2 + amp3
        
    y = np.arange(0, numADCSamples, 1) / numADCSamples *  fs * scipy.constants.c / 2 / S
    x = np.arange(-numChirps // 2, numChirps // 2, 1) * LAMBDA / 64 / 4 / (Tc + idleTime)
    
       
    X, Y = np.meshgrid(x, y)
    plt.pcolormesh(X, Y,
                   20 * np.log10(abs(amp[:numADCSamples, :numChirps])),
                   alpha = 1,)
                   #cmap = 'turbo')
    
    plt.grid()
    plt.colorbar()
    plt.xlabel('v[m/s]')
    plt.ylabel('d[m]')
    plt.show()
    
    
    
if __name__ == '__main__':
    data = readDCA1000('22.9.2020 parking/5/adc_data.bin')
    plot(data)