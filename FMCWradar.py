# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 10:29:40 2020

@author: student6
"""

import scipy.constants

class FmcwRadar:
    
    
    def  __init__(self, frekvencija = 77, opseg = 4, S = 2, fs = 8000, \
                  trajanjeFrejma = 1, N = 1000, NAntena = 3):
        """Parametri zajedno sa jedinicama: f[GHz], B[GHz], S[Hz/s], fs[Hz], Tf[s], N, Na."""
        self.__frekvencija = frekvencija * pow(10, 9)
        self.__opseg = opseg * pow(10, 9)
        self.__S = S
        self.__fs = fs
        self.__trajanjeFrejma = trajanjeFrejma
        self.__N = N
        self.__NAntena = NAntena
        
        self.__TALASNA_DUZINA =  scipy.constants.c / self.__frekvencija
        
    def __str__(self):
        return str(self.__frekvencija) + ' ' + str(self.__opseg) + ' '  \
            + str(self.__S) + ' ' + str(self.__fs) + ' ' + str(self.__trajanjeFrejma) \
                + ' ' + str(self.__N) + ' ' + str(self.__NAntena) + '\n'
    
    def medjufrekvencija(self, rastojanje) -> float:
        return self.__S * 2 * rastojanje / scipy.constants.c
    
    def maksRastojanje(self) -> float:
        return self.__fs * scipy.constants.c / 2 / self.__S
    
    def rezolucija(self) -> float:
        return  scipy.constants.c / 2 / self.__opseg
    
    def rezolucijaBrzine(self) -> float:
        return  self.__TALASNA_DUZINA / 2 / self.__trajanjeFrejma
    
    def doplerovaFrekv(self, v) -> float:
        return 2 * v  / self.__TALASNA_DUZINA #* self.__trajanjeFrejma / self.__N
    
    def vMaks(self) -> float:
        return self.__TALASNA_DUZINA * self.__N / 4 / (self.__trajanjeFrejma + 100 * 10 ** (-6))
    
    def SNR(self, sigma, Pt, Gtx, Grx, d, TA, F) -> float:
        return sigma * Pt * Gtx * Grx * pow(self.__TALASNA_DUZINA, 2) *  \
                self.__trajanjeFrejma / pow((4 * scipy.pi), 3) / pow(d, 4) / \
                scipy.constants.Boltzmann / TA / F
    
    def rezolucijaUglaDolaska(self) -> float:
        return 2 / self.__NAntena
    
    