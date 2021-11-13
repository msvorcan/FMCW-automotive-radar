# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 13:19:37 2020

@author: student6
"""

from FMCWradar import *

r1 = FmcwRadar()
print('ime | frekvencija | propusni opseg | strmina | fs | trajanje frejma |'
      + ' broj odbiraka | broj antena')

print('Radar 1: ' + str(r1))

r2 = FmcwRadar(1250, 30, 1.5, 10000, 2, 5000, 5)

print('Radar 2: ' + str(r2))

awr1642 = FmcwRadar(77, 4, 42 * pow(10, 12), 6250 * pow(10, 3), 0.006, 64, 4)

print('Ocekivana medjufrekvencija awr1642 radara za rastojanje od 5m: ' + str("%.2f" %(awr1642.medjufrekvencija(5) / 1000)) + 'kHz.')
print('Maksimalno rastojanje je: ' + str("%.2f" %awr1642.maksRastojanje()) + ' m.')
print('Rezolucija radara je: ' + str("%.2f" %(awr1642.rezolucija() * 100)) + ' cm.')
print('Rezolucija brzine je: ' + str("%.2f" %awr1642.rezolucijaBrzine()) + ' m/s.')
print('Maksimalna merljiva brzina je: ' + str("%.2f" %awr1642.vMaks()) + ' m/s.')
print('Rezolucija ugla dolaska awr1642 radara je: ' + str("%.2f" %awr1642.rezolucijaUglaDolaska()) + ' rad.')
print('Doplerova: ' + str("%.2f" %awr1642.doplerovaFrekv(6)) + ' Hz.')