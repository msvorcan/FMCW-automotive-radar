# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 11:31:22 2020

@author: student6
"""

import numpy as np
import os

numADCSamples = 256
numADCBits = 16
numRX = 4
numLanes = 2
isReal = 0

filename = "adc.bin"

with open(filename, "rb") as f:
    adcData = f.read(16)
    
    print(os.path.getsize(filename))
    
    if numADCBits != 16:
        max1 = pow(2, (numADCBits - 1)) - 1
        adcData[adcData > max1] = adcData[adcData > max1] - pow(2, numADCBits) #???
    f.close()
    
    fileSize = os.path.getsize(filename)
    
    if isReal:
        numChirps = fileSize / numADCSamples / numRX
        LVDS = np.zeros(1, fileSize)
        LVDS = np.reshape(adcData, (numADCBits * numRX, numChirps))
        LVDS = np.transpose(LVDS)
    else:
        numChirps = fileSize / 2 / numADCSamples / numRX
        LVDS = np.zeros(1, fileSize / 2)
        counter = 1
        i = 1
        while i < fileSize - 1:
            LVDS[1, counter] = adcData[i] + adcData[i + 2] * np.sqrt(-1)
            LVDS[1, counter + 1] = adcData[i + 1] + adcData[i + 3] * np.sqrt(-1)
            counter += 2
            i += 4
        LVDS = np.reshape(LVDS, (numADCSamples * numRX, numChirps))
        LVDS = np.transpose(LVDS)
        
    adcData = np.zeros(numRX, numChirps * numADCSamples)
    for i in range(1, numRX):
        for j in range(1, numChirps):
            adcData[i, (j - 1) * numADCSamples ]
            
        
        
        