# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 15:45:20 2020

@author: Vojislava Jankovic
Animacija za kretanje autic u biblioteci(range-dopler mape po frejmovima)
"""
import matplotlib.pyplot as plt
import numpy as np
import scipy.constants

from readDCA1000_xWR12xx import readDCA1000
import matplotlib.animation as animation

#PODACI
f = 77 * pow(10, 9)         
fs = 10 * pow(10, 6)        
S = 100 * pow(10, 12)       
Tc = 0.00004             
idleTime = 0.0001        
isReal = 0               
numADCSamples = 256       
numADCBits = 16          
numLanes = 4             
numRX = 0                
numChirps = 128           
numFrames = 32           
fps = 8
                 
matrice = []            

LAMBDA = scipy.constants.c / f

#Konfiguracija radara i ucitavanje podataka 

vmax = LAMBDA * numChirps / 2 / 4 / (Tc + idleTime)                     
dmax = numADCSamples /  fs / scipy.constants.c * 2 * S    

def doppler(data):
    amp = np.zeros((128, 256), dtype = complex)
    amp2 = np.zeros((128, 256), dtype = complex)
    
    for ind in range(0, numFrames):
    
        for i in range(0, 128):
            amp1 = scipy.fft(data[0, ind * 256 * i : ind * 256 * (i + 1)], 256)
            amp2[i, :] = amp1
            
        for i in range(0, 256):
            amp1 = scipy.fft(amp2[:, i], 128)
            amp[:, i] = np.fft.fftshift(amp1)  
            
        matrice.append(amp)         

data = readDCA1000('23.9.2020/4/adc_data.bin') 

#Obrada podataka
doppler(data)

    
 
#Crtanje dopler mapa
y = np.arange(0, numADCSamples, 1) * dmax / numADCSamples    
x = np.arange(-numChirps // 2, numChirps // 2, 1) * vmax / (numChirps / 2) 
X,Y = np.meshgrid(x, y)
fig = plt.figure()

def init(xa, ya, za):
    plt.ylabel('Distance[m]')
    plt.xlabel('Velocity[m/s]') 
    plt.contourf(xa, ya ,20 * np.log10(abs(np.transpose(za[0]))),
                     20, cmap='jet',levels=np.linspace(30, 130, 100)
                 )
    plt.colorbar()
def update(ifrm, xa, ya, za):
    plt.contourf(xa, ya ,20 * np.log10(abs(np.transpose(za[ifrm]))),
                     20, cmap='jet',levels=np.linspace(30, 130, 100)
                )

ani = animation.FuncAnimation(fig, update, numFrames,init_func=init(X, Y, matrice), 
                                  fargs=(X, Y, matrice), interval=100 / fps
                              )
ani.save('animation.gif', writer='pillow',fps=fps)