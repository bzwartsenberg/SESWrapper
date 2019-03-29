#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 14:00:29 2019

@author: berend
"""

### test API:

from ses_measure import SESMeasure


import numpy as np


if __name__ == '__main__':
    
    
    dllpath = 'C:/seswrapper_2.7.4_Win64/SESWrapper.dll'
    ses_dir = 'C:/SES_1.4.0-r30_Win64'
    ses_instrument = ses_dir + '/dll/SESInstrument.dll'
    inst_path =  ses_dir + '/data/9ES219L_Instrument.dat'
    
    sm = SESMeasure(dllpath, ses_dir, ses_instrument = ses_instrument, 
                    inst_path = inst_path , verbose = True, 
                    element_set = 'High Pass (UPS)')
    
    
    region = {'centerEnergy': 17.0,
              'dwellTime': 10,
              'energyStep': 0.05,
              'fixed': False,
              'highEnergy': 20.0,
              'lowEnergy': 15.0,
              'lens_mode' : 'Transmission',
              'pass_energy' : 10.,
              'sweeps' : 2}
    
    data, slice_scale, channel_scale = sm.MeasureAnalyzerRegion(region, data = None, 
                            updatefreq = 'slice',  path = None)
    
    
#    sm.Finalize()
    
    
    
    
    
    