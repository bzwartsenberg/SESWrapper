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
            #Note: not sure about the -1 for size, using what is in the tutorial for SESwrapper
            self.e.error(self.sesdll.SetPropertyInteger(pname, -1, ctypes.byref(value))) ##middle argument is size, 
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
            
                
    def Validate(self, element_set, lens_mode, pass_energy, kinetic_energy):
        """Validate the selected parameters, raise error if wrong
        Args:
            element_set: element set (string)
            lens_mode: lens mode (string)
            pass_energy: pass energy (float)
            kinetic_energy: kinetic energy (float)
        Returns:
            None
            """
        if self.verbose: print(self.verbose('Validating'))

        element_set = element_set.encode('ASCII')            
        lens_mode = lens_mode.encode('ASCII')            


        self.e.error(self.sesdll.Validate(element_set, lens_mode, pass_energy, kinetic_energy)) 

        if self.verbose: print(self.verbose('Validation OK'))

    def ResetHW(self):
        """Reset the hardware.
        Args:
            None
        Returns:
            None
            """
        if self.verbose:
            print('Resetting hardware')
            
        self.e.error(self.sesdll.ResetHW())
        
    def TestHW(self):
        """Test the hardware.
        Args:
            None
        Returns:
            None
            """
        if self.verbose:
            print('Testing hardware')
            
        self.e.error(self.sesdll.TestHW())   
        
        
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
        
        
    def ZeroSupplies(self):
        """Zero supplies.
        Args:
            None
        Returns:
            None
            """
        if self.verbose:
            print('Zeroing supplies')
            
        self.e.error(self.sesdll.ZeroSupplies())    
        
        
    def GetBindingEnergy(self):
        """Get the binding energy.
        Returns:
            binding energy
            """        
        if self.verbose: print(self.verbose('Getting binding energy'))
            
        returnvar = ctypes.c_double(0)
        self.e.error(self.sesdll.GetBindingEnergy(ctypes.byref(returnvar)))
        
        return returnvar.value
    
    def SetBindingEnergy(self, binding_energy):
        """Get the binding energy.
        Args:
            binding_energy: float with binding energy
            """        
        if self.verbose: print(self.verbose('Setting binding energy'))
            
        self.e.error(self.sesdll.SetBindingEnergy(binding_energy))
        
    def GetKineticEnergy(self):
        """Get the kinetic energy.
        Returns:
            kinetic energy
            """        
        if self.verbose: print(self.verbose('Getting kinetic energy'))
            
        returnvar = ctypes.c_double(0)
        self.e.error(self.sesdll.GetKineticEnergy(ctypes.byref(returnvar)))
        
        return returnvar.value
    
    def SetKineticEnergy(self, kinetic_energy):
        """Get the kinetic energy.
        Args:
            kinetic_energy: float with kinetic energy
            """        
        if self.verbose: print(self.verbose('Setting kinetic energy'))
            
        self.e.error(self.sesdll.SetKineticEnergy(kinetic_energy))
        
    def GetExcitationEnergy(self):
        """Get the excitation energy.
        Returns:
            excitation energy
            """        
        if self.verbose: print(self.verbose('Getting excitation energy'))
            
        returnvar = ctypes.c_double(0)
        self.e.error(self.sesdll.GetExcitationEnergy(ctypes.byref(returnvar)))
        
        return returnvar.value
    
    def SetExcitationEnergy(self, excitation_energy):
        """Get the excitation energy.
        Args:
            excitation_energy: float with excitation energy
            """        
        if self.verbose: print(self.verbose('Setting excitation energy'))
            
        self.e.error(self.sesdll.SetExcitationEnergy(excitation_energy))


    def GetElementVoltage(self, element_name):
        """Get the element voltage.
        Args:
            element_name: name of the element
        Returns:
             element voltage
            """        
        if self.verbose: print(self.verbose('Getting element voltage ', element_name))
        
        element_name = element_name.encode('ASCII')                    
        
        returnvar = ctypes.c_double(0)
        self.e.error(self.sesdll.GetElementVoltage(element_name, ctypes.byref(returnvar)))
        
        return returnvar.value
    
    
    def SetElementVoltage(self,element_name, element_voltage):
        """Get the element voltage.
        Args:
            element_voltage: float with excitation energy
            element_name: name of the element
            """        
        if self.verbose: print(self.verbose('Setting element voltage of ', element_name))
        element_name = element_name.encode('ASCII')                    
            
        self.e.error(self.sesdll.SetElementVoltage(element_name,element_voltage))


        
        
        
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
    
    def SetDetectorRegion(self, detector_dict):
        """Take a dictionary of parameters and set the region
        Args:
            detector_dict: dictionary of parameters describing detector region"""
            
        if self.verbose:
            print('Setting Detector region')
            
        detector = DetectorRegion(paramdict = detector_dict)
        
        self.e.error(self.sesdll.SetDetectorRegion(detector))
        

    def GetDetectorRegion(self):
        """Get the current detector region
        Args:
            None
        Returns:
            Detector dictionary paramter"""             
            
        if self.verbose:
            print('Getting Detector region')            
            
        detector = DetectorRegion()
        self.e.error(self.sesdll.SetDetectorRegion(detector))        
        
        return dict(detector)    
    

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
        
