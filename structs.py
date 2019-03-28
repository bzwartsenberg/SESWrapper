#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:30:04 2019

@author: berend
"""

import ctypes

class AnalyzerRegion(ctypes.Structure):
    _fields_ = [('fixed_', ctypes.c_bool),
                ('highEnergy_', ctypes.c_double),
                ('lowEnergy_', ctypes.c_double),
                ('centerEnergy_', ctypes.c_double),
                ('energyStep_', ctypes.c_double),
                ('dwellTime_', ctypes.c_int)]
    
    def __init__(self, paramdict = {}):
        for k,v in paramdict.items():
            setattr(self, k + '_', v)
    
    def __iter__(self):
        
        d = {'fixed' : self.fixed_,
             'highEnergy' : self.highEnergy_,
             'lowEnergy' : self.lowEnergy_,
             'centerEnergy' : self.centerEnergy_,
             'energyStep' : self.energyStep_,
             'dwellTime' : self.dwellTime_}
        
        for k,v in d.items():
            yield (k,v)
            
    
class DetectorRegion(ctypes.Structure):
    _fields_ = [('firstXChannel_', ctypes.c_int),
                ('lastXChannel_', ctypes.c_int),
                ('firstYChannel_', ctypes.c_int),
                ('lastYChannel_', ctypes.c_int),
                ('slices_', ctypes.c_int),
                ('adcMode_', ctypes.c_char)]    ###this may actually be a bool? It's true or false
    
    def __init__(self, paramdict = {}):
        for k,v in paramdict.items():
            setattr(self, k + '_', v)    
    
    def __iter__(self):
        
        d = {'firstXChannel' : self.firstXChannel_,
             'lastXChannel' : self.lastXChannel_,
             'firstYChannel' : self.firstYChannel_,
             'lastYChannel' : self.lastYChannel_,
             'slices' : self.slices_,
             'adcMode' : self.adcMode_}
        for k,v in d.items():
            yield (k,v)

            
            
                
class DetectorInfo(ctypes.Structure):
    _fields_ = [('timerControlled_', ctypes.c_bool),
                ('xChannels_', ctypes.c_int),
                ('yChannels_', ctypes.c_int),
                ('maxSlices_', ctypes.c_int),
                ('maxChannels_', ctypes.c_int),
                ('frameRate_', ctypes.c_int),
                ('adcPresent_', ctypes.c_bool),
                ('discPresent_', ctypes.c_bool)]    ###this may actually be a bool? It's true or false
    
    def __iter__(self):
        
        d = {'timerControlled' : self.timerControlled_,
             'xChannels' : self.xChannels_,
             'yChannels' : self.yChannels_,
             'maxSlices' : self.maxSlices_,
             'maxChannels' : self.maxChannels_,
             'frameRate' : self.frameRate_,
             'adcPresent' : self.adcPresent_,
             'discPresent' : self.discPresent_}
        
        for k,v in d.items():
            yield (k,v)
                    
    
    
    