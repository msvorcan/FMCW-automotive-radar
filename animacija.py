# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:45:20 2020

@author: student6

"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.constants

from readDCA1000_xWR12xx import readDCA1000
from dopplerFFT import dopplerFFT
import matplotlib.animation as animation

#PODACI
f = 77 * pow(10, 9)         
fs = 10 * pow(10, 6)        
S = 15 * pow(10, 12)       
Tc = 0.00004             
idleTime = 0.00005        
isReal = 0               
numADCSamples = 256       
numADCBits = 16          
numLanes = 4             
numRX = 0                
numChirp = 128           
numFrames = 32           
fps = 8                  

LAMBDA = scipy.constants.c / f

matrice = []             

def data2(data, frame):
    return data[:, frame * numChirp * numADCSamples : (frame + 1) * numChirp * numADCSamples]


def animacija():
    """
    Funkcija crta range-doppler mape po svim frejmovima jedan za drugim.

    Returns
    -------
    None.

    """

    data = readDCA1000('24.9.2020/1/adc_data.bin', 256, 128, 32) 
    
    #Obrada podataka
    for ind in range(0, numFrames):
        matrice.append(dopplerFFT(data2(data, ind)))
     
    #Crtanje dopler mapi
    
    y = np.arange(0, numADCSamples, 1) / numADCSamples *  fs * scipy.constants.c / 2 / S    
    x = np.arange(-numChirp // 2, numChirp // 2, 1) * LAMBDA / 64 / 4 / (Tc + idleTime) 
    X, Y = np.meshgrid(x, y)
    fig = plt.figure()

    ani = animation.FuncAnimation(fig, update, numFrames,
                                      init_func=init(X, Y, matrice), 
                                      fargs=(X,Y,matrice), interval=100 / fps
                                 )
    ani.save('animation.gif', writer='pillow', fps=fps)
    
    
def init(xa, ya, za):
    """
    

    Parameters
    ----------
    xa, ya: Ose grafika
    za : F-ja koja se iscrtava

    Returns
    -------
    None.

    """
    plt.ylabel('d[m]')
    plt.xlabel('v[m/s]') 
    plt.contourf(xa, ya , 20 * np.log10(abs(za[0])),
                     20, cmap='jet', levels=np.linspace(30, 130, 100)
                )
    plt.colorbar()
    
def update(ifrm, xa, ya, za):
    """F-ja koja crta ponovo grafik"""
    plt.contourf(xa, ya ,20 * np.log10(abs(za[ifrm])),
                     20, cmap='jet',levels=np.linspace(30, 130, 100)
                )
    
if __name__ == '__main__':
    animacija()