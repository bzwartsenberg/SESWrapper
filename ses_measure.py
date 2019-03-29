#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 08:45:42 2019

@author: berend
"""

import numpy as np
from ses_functions import SESFunctions
from configparser import ConfigParser

class SESMeasure:
    
    
    def __init__(self, dllpath, ses_dir, ses_instrument = '', inst_path = '' , 
                 verbose = False, element_set = 'High Pass (UPS)', motorcontrol = None):
        """
        
        
        """
        
        self.ses = SESFunctions(dllpath, verbose = verbose)
            
        
        self.ses.SetProperty('lib_working_dir', ses_dir)
        self.ses.SetProperty('instrument_library', ses_instrument)
        
        ## Note: change ini file here
        self.ini_path = ses_dir + '/ini/DetectorGraph.ini'
        config = ConfigParser()
        config.read(self.ini_path)
        self.save_direct_viewer = config['global']['direct_viewer']
        self.save_network_viewer = config['global']['network_viewer']
        config['global']['direct_viewer'] = 'false'
        config['global']['network_viewer'] = 'true'
        with open(self.ini_path, 'w') as configfile:
            config.write(configfile)        
        
        
        self.ses.Initialize()
        
        self.ses.LoadInstrument(inst_path)
        
        self.ses.SetProperty('element_set', element_set)
        
        self.motorcontrol = motorcontrol
        
        
            
    def __enter__(self, test): ##for syntax like "with SES() as ses:"
        pass
    
    
    
    
    def __exit__(self, test):
        pass
    
    
    
    
    def MeasureAnalyzerRegion(self, region, data = None, updatefreq = 'slice', 
                              path = None):
        """
        Measure a region with SES.
        Args:
            region: is a dictionary of parameters
            data:  np array that gets written to (not implemented yet)
            updatefreq: is the update frequency with which data gets updated
                        (not implemented yet)
            path: filename that data is written to, only written if not None"""
        
        sweeps = region.pop('sweeps')
                
        self.ses.SetProperty('pass_energy', float(region.pop('pass_energy')))
        self.ses.SetProperty('lens_mode', region.pop('lens_mode'))

        self.ses.SetAnalyzerRegion(region)
        
        self.ses.InitAcquisition(False, True)

        channels = self.ses.GetAcquiredData('acq_channels')
        slices = self.ses.GetAcquiredData('acq_slices')
        
        data_size = channels*slices
                

        for i in range(sweeps):
            self.ses.StartAcquisition()
            self.ses.WaitForRegionReady(-1)
            self.ses.ContinueAcquisition()

        data = self.ses.GetAcquiredDataArray('acq_image', data_size, data = None)
        slice_scale = self.ses.GetAcquiredDataArray('acq_slice_scale', slices, data = None)
        channel_scale = self.ses.GetAcquiredDataArray('acq_channel_scale', channels, data = None)
        
        
        data = data.reshape((slices, channels))
        
        if path is not None:
            np.savetxt(path, data)
            
        return data, slice_scale, channel_scale
        
    
    
    
    def MeasureWithMotors(self, region, motor_paths):
        """
        region: see above
        motor_paths: dictionary of axis name and array of values: 'P' : np.array([0, 0.5,1.0])
               Assumed to all be the same length
        """
        if self.motorcontrol is None:
            print('Please give motorcontrol object')
            
        n_steps = next(iter(motor_paths.values()))
        
        for i in range(n_steps):
            print('Taking step ', i)
            ## move motors:
            for ax, v_arr in motor_paths.items():                
                print('Moving motor {} to {:d}'.format(ax, v_arr[i]))
                r = self.motorcontrol.move_axis(self, ax, v_arr[i], s = 0.1)
                print('Response was:')
                self.motorcontrol.printresponse(r)
            print('Taking image:')
            
            data_step, slice_scale, channel_scale = self.MeasureAnalyzerRegion(region.copy(), data = None, 
                                                   updatefreq = 'slice', 
                                                    path = None)
            if i == 0:
                data = np.zeros((data_step.shape[0],n_steps))
            data[:,i] = data_step
            
            
        return data, slice_scale, channel_scale
    
    
    def Finalize(self):
        
        ## Note: change ini file here
        
        self.ses.Finalize()
        
        config = ConfigParser()
        config.read(self.ini_path)
        config['global']['direct_viewer'] = self.save_direct_viewer
        config['global']['network_viewer'] = self.save_network_viewer
        with open(self.ini_path, 'w') as configfile:
            config.write(configfile)           
    
    
    
    
    
    
    