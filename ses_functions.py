#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 10:42:20 2019

@author: berend
"""

## sesfunctions: wraps the dll in pure python

from ses_dll import SESdll
from ses_error import SESError
import ctypes
from structs import AnalyzerRegion, DetectorRegion, DetectorInfo
import numpy as np



class SESFunctions:
    
    
    
    def __init__(self, dllpath, verbose = False):
        
        
        self.sesdll = SESdll(dllpath) ## note: close this dll
        self.verbose = verbose
        self.e = SESError(verbose = self.verbose)
        self.acq_funcs = {
                'acq_channels' : (self.sesdll.GetAcquiredDataInteger,ctypes.c_int),
                'acq_slices' : (self.sesdll.GetAcquiredDataInteger,ctypes.c_int),
                'acq_iterations' : (self.sesdll.GetAcquiredDataInteger,ctypes.c_int),
                'acq_intensity_unit':(self.sesdll.GetAcquiredDataString,ctypes.c_char_p),
                'acq_channel_unit':(self.sesdll.GetAcquiredDataString,ctypes.c_char_p),
                'acq_slice_unit':(self.sesdll.GetAcquiredDataString,ctypes.c_char_p),
                'acq_spectrum' : (self.sesdll.GetAcquiredDataVectorDouble, ctypes.c_double),
                'acq_slice' : (self.sesdll.GetAcquiredDataVectorDouble, ctypes.c_double),
                'acq_image' : (self.sesdll.GetAcquiredDataVectorDouble, ctypes.c_double),
                'acq_channel_scale':(self.sesdll.GetAcquiredDataVectorDouble, ctypes.c_double),
                'acq_slice_scale':(self.sesdll.GetAcquiredDataVectorDouble, ctypes.c_double),
                'acq_raw_image':(self.sesdll.GetAcquiredDataVectorInt32, ctypes.c_int),
                'acq_current_step':(self.sesdll.GetAcquiredDataInteger,ctypes.c_int),
                'acq_elapsed_time':(self.sesdll.GetAcquiredDataDouble, ctypes.c_double),
                'acq_current_point':(self.sesdll.GetAcquiredDataInteger,ctypes.c_int),
                'acq_point_intensity':(self.sesdll.GetAcquiredDataDouble, ctypes.c_double),
                'acq_channel_intensity':(self.sesdll.GetAcquiredDataVectorDouble, ctypes.c_double),
                }
        
        self.property_funcs = {
                'lib_description' :(self.sesdll.GetPropertyString,ctypes.c_char_p),
                'lib_version' : (self.sesdll.GetPropertyString,ctypes.c_char_p),
                'lib_error' : (self.sesdll.GetPropertyString,ctypes.c_char_p),
                'lib_working_dir':(self.sesdll.GetPropertyString,ctypes.c_char_p),
                'instrument_library':(self.sesdll.GetPropertyString,ctypes.c_char_p),
                'instrument_status':(self.sesdll.GetPropertyInteger,ctypes.c_int),
                
                'always_delay_region' : (self.sesdll.GetPropertyBool, ctypes.c_bool),
                'allow_io_with_detector' : (self.sesdll.GetPropertyBool, ctypes.c_bool),
                
                'instrument_model' : (self.sesdll.GetPropertyString, ctypes.c_char_p),
                'instrument_serial_no':(self.sesdll.GetPropertyString, ctypes.c_char_p),
                
#                'detector_info':(self.sesdll.GetPropertyDouble, ctypes.c_double), ## Not mapped, use GetDetectorInfo
#                'detector_region':(self.sesdll.GetPropertyDouble, ctypes.c_double), ##Not mapped, use GetDetectorRegion
                
                'element_set_count':(self.sesdll.GetPropertyInteger,ctypes.c_int),
                'element_set':(self.sesdll.GetPropertyString,ctypes.c_char_p),
                
                'element_name_count':(self.sesdll.GetPropertyInteger,ctypes.c_int),
                'element_name':(self.sesdll.GetPropertyString,ctypes.c_char_p),
                
                'lens_mode_count':(self.sesdll.GetPropertyInteger,ctypes.c_int),
                'lens_mode':(self.sesdll.GetPropertyString,ctypes.c_char_p),
                
                'pass_energy_count':(self.sesdll.GetPropertyInteger,ctypes.c_int),
                'pass_energy':(self.sesdll.GetPropertyDouble,ctypes.c_double),
                

#                'analyzer_region':(self.sesdll.GetPropertyDouble,ctypes.c_double), ###Not mapped: use GetAnalyzerRegion
                
                'use_external_io' : (self.sesdll.GetPropertyBool, ctypes.c_bool),
                'use_detector' : (self.sesdll.GetPropertyBool, ctypes.c_bool),
                'use_spin' : (self.sesdll.GetPropertyBool, ctypes.c_bool),
                'region_name' : (self.sesdll.GetPropertyString, ctypes.c_char_p),
                'temp_file_name' : (self.sesdll.GetPropertyString, ctypes.c_char_p),
                'reset_data_between_iterations' : (self.sesdll.GetPropertyBool, ctypes.c_bool),
                'use_binding_energy' : (self.sesdll.GetPropertyBool, ctypes.c_bool),

                }        
        
        
        
        
    def Initialize(self):
        """Initialize the SES software
        Args:
            None
        Returns:
            None
            """
        
        self.e.error(self.sesdll.Initialize(0)) ##0 is a standard parameter
        
                
    def GetProperty(self, name):
        """Get property data
        Args:
            name: parameter name
        Returns:
            value of paramter
            """
        if self.verbose:
            print('Getting property')
            
        func, returntype = self.property_funcs[name]
        
        if returntype == ctypes.c_char_p:
            if self.verbose:
                print('Getting property ',name, ' of string type')
            returnarray = ctypes.create_string_buffer(2000)
            returnsize = ctypes.c_int(2000)
            nameb = name.encode('ASCII')
            self.e.error(func(nameb, 0, returnarray, ctypes.byref(returnsize)))
            return returnarray.value.decode('ASCII')    
        else:
            if self.verbose:
                print('Getting property ', name, ' of type ', returntype)
            returnvar = returntype(0)
            returnsize = ctypes.c_int(0)
            nameb = name.encode('ASCII')
            self.e.error(func(nameb, 0, ctypes.byref(returnvar), ctypes.byref(returnsize)))
            
            return returnvar.value    
        
        
    def SetProperty(self, pname, value):
        """Set a property
        Args:
            pname: property name
            pvalue: value
        Returns:
            None
            """


            
        if type(value) == int:
            if self.verbose:
                print('Setting int property')    
            value = ctypes.c_int(value)
            pname = pname.encode('ASCII')            
            self.e.error(self.sesdll.SetPropertyInteger(pname, -1, ctypes.byref(value))) ##middle argument is size
        if type(value) == float:
            if self.verbose:
                print('Setting double/float property')    
            value = ctypes.c_double(value)
            pname = pname.encode('ASCII')            
            self.e.error(self.sesdll.SetPropertyDouble(pname, -1, ctypes.byref(value))) ##middle argument is size
        if type(value) == str:
            if self.verbose:
                print('Setting string property')    
            value = value.encode('ASCII')
            pname = pname.encode('ASCII')            
            self.e.error(self.sesdll.SetPropertyString(pname, 0, value)) ##middle argument is size
            
                    
        
    def LoadInstrument(self, instrumentpath):
        """Load the instrument dat file
        Args:
            path to the instrument
        Returns:
            None"""
            
        if self.verbose:
            print('Laoding Instrument')    
            
        instrumentpath = instrumentpath.encode('ASCII')
        self.e.error(self.sesdll.LoadInstrument(instrumentpath))
        
        
    def GetDetectorInfo(self):
        """Get the detector info
        Args:
            None
        Returns:
            dictionary with detector properties"""
            
        if self.verbose:
            print('Getting Detector info')            
            
        info = DetectorInfo()
        self.e.error(self.sesdll.GetDetectorInfo(info))
        
        return dict(info)
    
    def SetAnalyzerRegion(self, analyzer_dict):
        """Take a dictionary of parameters and set the region
        Args:
            analyzer: dictionary of parameters"""
            
        if self.verbose:
            print('Setting Analyzer region')
            
        analyzer = AnalyzerRegion(paramdict = analyzer_dict)
        
        self.e.error(self.sesdll.SetAnalyzerRegion(analyzer))
        

    def GetAnalyzerRegion(self):
        """Get the current analyzer region
        Args:
            None
        Returns:
            Analyzer dictionary paramter"""             
            
        if self.verbose:
            print('Getting Analyzer region')            
            
        analyzer = AnalyzerRegion()
        self.e.error(self.sesdll.GetAnalyzerRegion(analyzer))        
        
        return dict(analyzer)

    def InitAcquisition(self, blockpointready, blockregionready):
        """Initialize the acquisition.
        Args:
            blockpointready:	If true, this parameter tells the acquisition thread 
                            to wait for confirmation between each step taken in 
                            a swept mode acquisition.
            blockregionready: If true, this parameter tells the acquisition thread 
                                to wait for confirmation once the acquisition is finished.        
        Returns:
            None
            """
        if self.verbose:
            print('Initializing acquisition')
        self.e.error(self.sesdll.InitAcquisition(blockpointready, blockregionready))
        
    def StartAcquisition(self):
        """Start the acquisition.
        Args:
            None
        Returns:
            None
            """
        if self.verbose:
            print('Starting acquisition')
            
        self.e.error(self.sesdll.StartAcquisition())
        
    def WaitForRegionReady(self, timeout_time):
        """Start the acquisition.
        Args:
            timeout_time: -1 is infinite
        Returns:
            None
            """
        if self.verbose:
            print('Waiting for region')
        
        timeout_time = ctypes.c_int(timeout_time)
        self.e.error(self.sesdll.WaitForRegionReady(timeout_time))

    def ContinueAcquisition(self):
        """Start the acquisition.
        Args:
            None
        Returns:
            None
            """
        if self.verbose:
            print('Continuing acquisition')
            
        self.e.error(self.sesdll.ContinueAcquisition())
        
    def StopAcquisition(self):
        """Stop the acquisition.
        Args:
            None
        Returns:
            None
            """
        if self.verbose:
            print('Stopping acquisition')
            
        self.e.error(self.sesdll.StopAcquisition())
                  
        
    def GetAcquiredData(self, name):
        """Get acquired data
        Args:
            name: parameter name
        Returns:
            value of paramter
            """
        if self.verbose:
            print('Getting data')
            
        func, returntype = self.acq_funcs[name]
        
        if returntype == ctypes.c_char_p:
            if self.verbose:
                print('Getting data ',name, ' of string type')
            returnarray = ctypes.create_string_buffer(2000)
            returnsize = ctypes.c_int(2000)
            nameb = name.encode('ASCII')
            self.e.error(func(nameb, 0, returnarray, ctypes.byref(returnsize)))
            return returnarray.value.decode('ASCII')    
        else:
            if self.verbose:
                print('Getting data ', name, ' of type ', returntype)
            returnvar = returntype(0)
            returnsize = ctypes.c_int(0)
            nameb = name.encode('ASCII')
            self.e.error(func(nameb, 0, ctypes.byref(returnvar), ctypes.byref(returnsize)))
            
            return returnvar.value            
                    

    def GetAcquiredDataArray(self, name, size, data = None, index = 0):
        """Get acquired data
        Args:
            name: parameter name
            size: size for the data
            data: optional pointer to data holding object (numpy array)
            index: for parameters that require an index
            """            
        if self.verbose:
            print('Getting data array')
            
        func, returntype = self.acq_funcs[name]
            
        returnarray = (returntype * size)()
        returnsize = ctypes.c_int(size)
        nameb = name.encode('ASCII')
        self.e.error(func(nameb, index, returnarray, ctypes.byref(returnsize)))
        
        if data is None:
            data = np.array(returnarray)
        else:
            np.copyto(np.array(returnarray),data)
        
        return data
    
   
    
    
    def Finalize(self):
        """Finalize the instrument
        Args: None
        Returns: None"""
        
        if self.verbose:
            print('Finalizing')
        
        
        self.e.error(self.sesdll.Finalize())
        
        
        
        
        
                
        
        
        
        
    def setVerbosity(self, verbose = False):
        self.verbose = verbose
        
        self.e.verbose = verbose
        
        
    def closedll(self):
        """Close the dll"""
        pass
        
