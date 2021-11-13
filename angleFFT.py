# -*- coding: utf-8 -*-
"""
Created on Fri Sep 18 10:15:17 2020

@author: student6
"""

import math
import scipy.constants
import numpy as np
import matplotlib.pyplot as plt

from readDCA1000_xWR12xx import readDCA1000
from dopplerFFT import dopplerFFT

f = 77 * pow(10, 9)
fs = 10 * pow(10, 6)
S = 30 * pow(10, 12)
Tc =  40 * pow(10, -6)
idleTime = 50 * pow(10, -6)
LAMBDA = scipy.constants.c / f

numADCSamples = 256
numChirps = 128

D = LAMBDA / 2
RANGE = 180
DTHETA = 5

def tauFunc(theta):
    """"Vreme kasnjenja signala izmedju dve antene za dati ugao."""
    return D * math.sin(theta * math.pi / 180) / LAMBDA

def angleFFT(data):
    """F-ja racuna i vraca RDA matricu. """
    amp0 = dopplerFFT(data, 0)
    amp1 = dopplerFFT(data, 1)
    amp2 = dopplerFFT(data, 2)
    amp3 = dopplerFFT(data, 3)  
    
    vectorsMatrix = np.zeros((4, RANGE // DTHETA + 1), dtype = complex)        
    #matrica vektora za 4 antene po svim uglovima 
    
    iterator = 0
    
    RDA = np.zeros((numChirps, numADCSamples, RANGE // DTHETA + 1), dtype = complex)
    #3-D matrica u kojoj se smestaju rezultati nakon bimforminga
    
    for theta in range(-RANGE // 2, RANGE // 2 + 1, DTHETA):
        tau = tauFunc(theta)
        
        for i in range(0, 4): vectorsMatrix[i, iterator] = np.exp(-1j * 2 * math.pi * tau * i)
        
        amp = amp0 * vectorsMatrix[0, iterator]     \
                + 1.5 * amp1 * vectorsMatrix[1, iterator] \
                + 1.5 * amp2 * vectorsMatrix[2, iterator] \
                + amp3 * vectorsMatrix[3, iterator] 
                      
        RDA[:, :, iterator] = np.transpose(amp)     
    
        iterator += 1
    
    return RDA

def plot(RDA):
    """

    F-ja crta grafike za svaki ugao

    Returns
    -------
    None.

    """
    iterator = 0
    
    x = np.arange(-numChirps // 2, numChirps // 2, 1) * LAMBDA / 64 / 4 / (Tc + idleTime)
    y = np.arange(0, numADCSamples, 1) / numADCSamples *  fs * scipy.constants.c / 2 / S
    X, Y = np.meshgrid(x, y)
    
    
    for theta in range(-RANGE // 2, RANGE // 2 + 1, DTHETA):
        ax = plt.subplot(4, 10, iterator + 1)
        plt.title('theta = ' + str(theta))
        X, Y = np.meshgrid(x, y)
        plt.pcolormesh(X, Y,
                   20 * np.log10(abs(np.transpose(RDA[:numChirps, :numADCSamples, iterator]))),
                   alpha = 1,
                   #cmap = 'Accent',
                   vmin=-30, vmax=120
                   )
        
        plt.grid()
        plt.colorbar()
        plt.xlabel('v[m/s]')
        plt.ylabel('d[m]')
        
        iterator += 1

def polarni(RDA, brzina):
    """
    

    Parameters
    ----------
    RDA : Matrica nakon bimforminga
    brzina : Odbirak koji odgovara odredjenoj dopler frekvenciji, 
        odnosno brzini.

    Returns
    -------
    None.

    """
    plt.figure()
    ax = plt.subplot(111, polar = True)
    t = np.linspace(-RANGE // 2, RANGE // 2, RANGE // DTHETA + 1) * math.pi / 180
    r = np.linspace(0, 14, numADCSamples)
    ax.set_thetamin(RANGE // 2)
    ax.set_thetamax(-RANGE // 2)
    ax.set_theta_zero_location("N")
    plt.axes(polar = True)
    ax.contourf(t, r , 20 * np.log10(RDA[brzina, :, :]))
    ax.plot() 
    plt.grid()
    plt.show()
    plt.colorbar()     



if __name__ == '__main__':
    data = readDCA1000('22.9.2020 parking/5/adc_data.bin')
    rez = angleFFT(data)
    plot(rez)
    polarni(rez, 64)
    