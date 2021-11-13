# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack

N = 0
a1 = 1
a2 = 2
f1 = 1000
f2 = 1250
fs = 8000


def mySpectrum(a, fs, N):
    """
    

    Parameters
    ----------
    a : Signal
    fs : ucestanost odabiranja
    N : broj tacaka u kojima se racuna FFT

    Returns
    -------
    ampDb - decibelski amplitudski spektar
    phase - fazni spektar
    fscale - x - osa za crtanje spektra

    """
    yf = scipy.fft(a, N)
    fscale = np.linspace(0.0, fs, N)
    ampdB = 20 * np.log10(yf[:N] / max(np.abs(yf[:N])))
    phase = np.unwrap(np.angle(yf[:N], deg=True))
    return(ampdB, phase, fscale)
    




if __name__ == '__main__':

    for N in (128, 512, 16384):
    
        T = 1.0 / fs    
        x = np.linspace(0.0, N*T, N)
        y = a1 * np.sin(f1 * 2.0 * np.pi * x) + a2 * np.sin(f2 * 2.0 * np.pi * x)
    
        ampdB, phasedB, fscale = mySpectrum(y, fs, N)
        plt.figure(1)
        ax1 =  plt.subplot(211)
        ax1.set_title('N=' + str(N))
        ax1.set_xlabel('f[Hz]')
        ax1.set_ylabel('ampl[dB]')
        ax1.plot(fscale, ampdB)
        ax1.grid()
    
        ax2 = plt.subplot(212)
        ax2.set_title('N=' + str(N))
        ax2.set_xlabel('f[Hz]')
        ax2.set_ylabel('phase[deg]')
        ax2.plot(fscale, phasedB)
        ax2.grid()
    
  
        plt.show()