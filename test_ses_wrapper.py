#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 14:00:29 2019

@author: berend
"""

### test API:

from ses_measure import SESMeasure
from motors import MotorController


import numpy as np
import h5py

if __name__ == '__main__':
    
    
    dllpath = 'D:/programs/seswrapper_2.7.4_Win64/SESWrapper.dll'
    ses_dir = 'D:/SES_1.8.0_Win64_Package/SES_1.8.0_Win64'
    ses_instrument = ses_dir + '/dll/SESInstrument.dll'
    inst_path =  ses_dir + '/data/9ES219L_Instrument.dat'

    mc = MotorController()

    
    sm = SESMeasure(dllpath, ses_dir, ses_instrument = ses_instrument, 
                    inst_path = inst_path , verbose = True, 
                    element_set = 'High Pass (UPS)', motorcontrol = mc)
    
    
    region = {'centerEnergy': 16.2000,
              'dwellTime': 118,   #ms
              'energyStep': 0.020,
              'fixed': False,
              'highEnergy': 16.9778,
              'lowEnergy': 15.4222,
              'lens_mode' : 'DA30L_08',
              'pass_energy' : 20.,
              'sweeps' : 1}
    
##    data, slice_scale, channel_scale = sm.MeasureAnalyzerRegion(region, data = None, updatefreq = 'slice', 
##                              path = None)
    motor_paths = {'P' : np.linspace(-15, 12, 91)}

    data, slice_scale, channel_scale = sm.MeasureWithMotors(region, motor_paths)
    
    sm.Finalize()

    with h5py.File('D:/programs/SESWrapperPython/SESWrapper-master/FS.h5','w') as hf:
        hf.create_dataset('P', data = np.array(motor_paths['P']))
        hf.create_dataset('slice_scale', data = np.array(slice_scale))
        hf.create_dataset('channel_scale', data = np.array(channel_scale))
        hf.create_dataset('data', data = np.array(data))


    
    
