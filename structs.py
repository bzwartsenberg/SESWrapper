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
    
    
    
class DetectorRegion(ctypes.Structure):
    _fields_ = [('firstXChannel_', ctypes.c_int),
                ('lastXChannel_', ctypes.c_int),
                ('firstYChannel_', ctypes.c_int),
                ('lastYChannel_', ctypes.c_int),
                ('slices_', ctypes.c_int),
                ('adcMode_', ctypes.c_char)]    ###this may actually be a bool? It's true or false
    
    
    
    
    