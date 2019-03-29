#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 08:45:42 2019

@author: berend
"""

import numpy as np
from ses_functions import SESFunctions

class SESMeasure:
    
    
    def __init__(self, dllpath, ses_dir, ses_instrument = '', inst_path = '' , 
                 verbose = False, element_set = 'High Pass (UPS)'):
        """
        
        """
        
        self.ses = SESFunctions(dllpath, verbose = verbose)
            
        
        self.ses.SetProperty('lib_working_dir', ses_dir)
        self.ses.SetProperty('instrument_library', ses_instrument)
        
        ## Note: change ini file here
        self.ses.Initialize()
        
        self.ses.LoadInstrument(inst_path)
        
        self.ses.SetProperty('element_set', element_set)
        
        
            
    def __enter__(self, test): ##for syntax like "with ses = SES():"
        pass
    
    
    
    
    def __exit__(self, test):
        pass
    
    
    
    
    def MeasureAnalyzerRegion(self, region, data = None, updatefreq = 'slice', 
                              path = None):
        """region is a dictionary of parameters
        data is a np array that gets written to
        
        updatefreq is the update frequency with which data gets updated
        
        Estart, Eend
        Estep, etc
        path is used to save"""
        
        sweeps = region.pop('sweeps')
                
        self.ses.SetProperty('pass_energy', float(region.pop('pass_energy')))
        self.ses.SetProperty('lens_mode', region.pop('lens_mode'))

        self.ses.SetAnalyzerRegion(region)
        
        self.InitAcquisition(False, True)

        channels = self.ses.GetAcquiredData('acq_channels')
        slices = self.ses.GetAcquiredData('acq_slices')
        
        data_size = channels*slices
        
        data = np.zeros(data_size)
        

        for i in range(sweeps):
            self.ses.StartAcquisition()
            self.ses.WaitForRegionReady(-1)
            self.ContinueAcquisition()

        data = self.ses.GetAcquiredDataArray('acq_image', data_size, data = data)
        
        if path is not None:
            np.savetxt(path, data)
            
        return data
        
    
    
    
    def MeasureWithMotors(self, region, motors):
        """
        region: see above
        motors: dictionary of axis name and array of values: 'P' : np.array([0, 0.5,1.0])
        """
        pass
    
    
    
    
    
    
    
    
