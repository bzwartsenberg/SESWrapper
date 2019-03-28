#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 08:45:42 2019

@author: berend
"""

import numpy as np


class SESMeasure:
    
    
    def __init__(self, params, verbose = False):
        """
        Take directories
        Load dll,
        set folders
        save state of DetectorGraph.ini, set detectorgraph.ini
        initialize
        
        
        
        finalize seswrapper
        Finally: free dll,
        
        """
        pass
    
    def __enter__(self, test): ##for syntax like "with ses = SES():"
        pass
    
    
    
    
    def __exit__(self, test):
        pass
    
    
    
    
    def MeasureAnalyzerRegion(self, region, data = None, updatefreq = 'slice', path = ''):
        """region is a dictionary of parameters
        data is a np array that gets written to
        
        updatefreq is the update frequency with which data gets updated
        
        Estart, Eend
        Estep, etc
        path is used to save"""
        data = np.zeros()
        
        return data
    
    
    
    def MeasureWithMotors(self, region, motors):
        """
        region: see above
        motors: dictionary of axis name and array of values: 'P' : np.array([0, 0.5,1.0])
        """
    
    
    
    
    
    
    
    
