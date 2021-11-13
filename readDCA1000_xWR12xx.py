# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 11:27:52 2020

@author: student6
"""

import numpy as np
import FFT
import matplotlib.pyplot as plt
import scipy.constants

numADCSamples = 256
numFrames = 32
numChirps = 128
numADCBits = 16
numRX = 4
numLanes = 4
isReal = 0

fs = 10**7

fileName = '15.9.2020/range fft/1 na 0.5m 1 na 1m 1 na 2m/adc_data.bin'

def readDCA1000(fileName, numADCSamples=256, numChirps=128, numFrames=8):
"""
    

    Parameters
    ----------
    fileName : binarna datoteka
    numADCSamples : Broj odbiraka po cirpu.
        The default is 256.
    numChirps : Broj cirpova po frejmu.
        The default is 128.
    numFrames : Broj frejmova
        The default is 8.

    Returns
    
    Matrica 4 x [numADCSamples * numChirps * numFrames]

    """

    with open(fileName, "rb") as f:
        adcData = np.fromfile(f, dtype = np.int16)
    
        if numADCBits != 16:
            max1 = 2 ** (numADCBits - 1) - 1
            adcData[adcData > max1] = adcData[adcData > max1] - numADCBits ** 2 #???
           
        f.close()
    
        if isReal:
            data = np.reshape(adcData, (numLanes, -1))
        else:
           adcData2 = np.zeros((8, numADCSamples * numChirps * numFrames))
           i = 0
           for j in range(0, numADCSamples * numChirps * numFrames):
               adcData2 [:, j] = adcData[i * 8 : (i + 1) * 8]
               i += 1
               
           data = adcData2[[0, 1, 2, 3], :] + 1j * adcData2[[4, 5, 6, 7], :]
           
        return data
    
    
    
    
            
if __name__ == '__main__':
    
    #mejn funkcija za proveru
    
    adcData = readDCA1000(fileName)
    
    N = 512
    T = 1.0 / fs    
    
    y = np.array(adcData[1, 0:256])
    
    ampdB, phasedB, fscale = FFT.mySpectrum(y, fs * scipy.constants.c / 2 / (100 * 10 ** 12), N)
    
    plt.figure(1)
    ax1 =  plt.subplot(111)
    ax1.set_title('N=' + str(N))
    ax1.set_xlabel('d[m]')
    ax1.set_ylabel('ampl[dB]')
    ax1.set_xlim(0, 15)
    ax1.plot(fscale, ampdB)
    ax1.legend(['meta na ~2m'])
    
    ax1.grid()
    
  
    plt.show()
    