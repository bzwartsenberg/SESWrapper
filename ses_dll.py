#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:37:38 2019

@author: berend
"""

import ctypes
from structs import AnalyzerRegion, DetectorRegion, DetectorInfo

class SESdll:
    
    def __init__(self, sesdllpath):
        
        self.sesdll = ctypes.WinDLL(sesdllpath)
        
        
        #initialize:
        sesinitProto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_void_p
                                         
                                         
                                         )
        ##note: first value is 1 for input, 2 for output, second is name of the parameter (optional: third is default)
        sesinitParams = ((1, 'p1'),)
        
        self.Initialize = sesinitProto(('WRP_Initialize',self.sesdll),sesinitParams)

        
        ######Finalize:
        
        sesFinalizeProto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         )
        
        sesFinalizeParams = ()
        
        self.Finalize = sesFinalizeProto(('WRP_Finalize',self.sesdll),sesFinalizeParams)
        


        ### GetProperty is not wrapped: use GetPropertyString, etc.
        
        
        ### GetPropertyBool:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #param name
                                         ctypes.c_int, #index
                                         ctypes.POINTER(ctypes.c_bool), #property pointer
                                         ctypes.POINTER(ctypes.c_int), #size
                                         )        
        
        funcparams = ((1,'param_name'),(1,'index'),(1,'property_pointer'),(1,'data_size'))
        self.GetPropertyBool = funcproto(('WRP_GetPropertyBool',self.sesdll),funcparams)
                        
        ### GetPropertyDouble:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #param name
                                         ctypes.c_int, #index
                                         ctypes.POINTER(ctypes.c_double), #property pointer
                                         ctypes.POINTER(ctypes.c_int), #size
                                         )        
        
        funcparams = ((1,'param_name'),(1,'index'),(1,'property_pointer'),(1,'data_size'))
        self.GetPropertyDouble = funcproto(('WRP_GetPropertyDouble',self.sesdll),funcparams)
                        
        ### GetPropertyInteger:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #param name
                                         ctypes.c_int, #index
                                         ctypes.POINTER(ctypes.c_int), #property pointer
                                         ctypes.POINTER(ctypes.c_int), #size
                                         )        
        
        funcparams = ((1,'param_name'),(1,'index'),(1,'property_pointer'),(1,'data_size'))
        self.GetPropertyInteger = funcproto(('WRP_GetPropertyInteger',self.sesdll),funcparams)
                        
                
        ### GetPropertyString:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #param name
                                         ctypes.c_int, #index
                                         ctypes.c_char_p, #data pointer
                                         ctypes.POINTER(ctypes.c_int), #size
                                         )        
        
        funcparams = ((1,'param_name'),(1,'index'),(1,'data_pointer'),(1,'data_size'))
        self.GetPropertyString = funcproto(('WRP_GetPropertyString',self.sesdll),funcparams)
        
        
        ####### getDetectorRegion:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         DetectorRegion,
                                         )        
        
        funcparams = ((1,'detector_region'),)
        self.GetDetectorRegion = funcproto(('WRP_GetDetectorRegion',self.sesdll),funcparams)
                
        ####### getDetectorInfo:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         DetectorInfo,
                                         )        
        
        funcparams = ((1,'detector_info'),)
        self.GetDetectorInfo = funcproto(('WRP_GetDetectorInfo',self.sesdll),funcparams)
                        

        ####### getAnalyzer:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         AnalyzerRegion,
                                         )        
        
        funcparams = ((1,'analyzer_region'),)
        self.GetAnalyzerRegion = funcproto(('WRP_GetAnalyzerRegion',self.sesdll),funcparams)
        
        #### SetProperty: not wrapped, use SetPropertyInteger etc.
        

        ### SetPropertyBool:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #param name
                                         ctypes.c_int, #index
                                         ctypes.POINTER(ctypes.c_bool), #pointer to property value to set
                                         )        
        
        funcparams = ((1,'param_name'),(1,'index'),(1,'property_pointer'))
        self.SetPropertyBool = funcproto(('WRP_SetPropertyBool',self.sesdll),funcparams)
                  


        #####Set property Integer:
        
        
        sesSetPropertyIntegerProto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #param name
                                         ctypes.c_int, #
                                         ctypes.POINTER(ctypes.c_int) #param value 
                                         )
        
        sesSetPropertyIntegerParams = ((1,'param_name'),(1,'unk'),(1,'param_value'))
        
        self.SetPropertyInteger = sesSetPropertyIntegerProto(('WRP_SetPropertyInteger',self.sesdll),sesSetPropertyIntegerParams)
        
        ######Set property Double:
        
        sesSetPropertyDoubleProto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #param name
                                         ctypes.c_int, #
                                         ctypes.POINTER(ctypes.c_double) #param value (actually needs to be an int_p)
                                         )
        
        sesSetPropertyDoubleParams = ((1,'param_name'),(1,'unk'),(1,'param_value'))
        
        self.SetPropertyDouble = sesSetPropertyDoubleProto(('WRP_SetPropertyDouble',self.sesdll),sesSetPropertyDoubleParams)
                
        
        #####Set property String
        sesSetPropertyStringProto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #param name
                                         ctypes.c_int, #
                                         ctypes.c_char_p #
                                         )
        
        sesSetPropertyStringParams = ((1,'param_name'),(1,'unk'),(1,'param_value'))
        
        self.SetPropertyString = sesSetPropertyStringProto(('WRP_SetPropertyString',self.sesdll),sesSetPropertyStringParams)

        ####### setAnalyzer:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         AnalyzerRegion,
                                         )        
        
        funcparams = ((1,'analyzer_region'),)
        self.SetAnalyzerRegion = funcproto(('WRP_SetAnalyzerRegion',self.sesdll),funcparams)
        


        ####### setDetectorRegion:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         DetectorRegion,
                                         )        
        
        funcparams = ((1,'detector_region'),)
        self.SetDetectorRegion = funcproto(('WRP_SetDetectorRegion',self.sesdll),funcparams)
                


                
        ### Validate:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #elementSet
                                         ctypes.c_char_p, #lens_mode
                                         ctypes.c_double, #passEnergy
                                         ctypes.c_double, #kineticEnergy
                                         )        
        
        funcparams = ((1,'element_set'),(1,'lens_mode'),(1,'pass_energy'),(1,'kinetic_energy'))
        self.Validate = funcproto(('WRP_Validate',self.sesdll),funcparams)
        

        ####### resetHW:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         )        
        
        funcparams = ()
        self.ResetHW = funcproto(('WRP_ResetHW',self.sesdll),funcparams)
                
        ####### testHW:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         )        
        
        funcparams = ()
        self.TestHW = funcproto(('WRP_TestHW',self.sesdll),funcparams)
                

        
        ######Load instrument
        
        sesLoadInstrumentProto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #file name
                                         )
        
        sesLoadInstrumentParams = ((1,'file_name'),)
        
        self.LoadInstrument = sesLoadInstrumentProto(('WRP_LoadInstrument',self.sesdll),sesLoadInstrumentParams)
        

        ####### zeroSupplies:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         )        
        
        funcparams = ()
        self.ZeroSupplies = funcproto(('WRP_ZeroSupplies',self.sesdll),funcparams)
                

        ####### Getbinding Energy:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.POINTER(ctypes.c_double), #bindingEnergy
                                         )        
                
        funcparams = ((1,'binding_energy'))
        self.GetBindingEnergy = funcproto(('WRP_GetBindingEnergy',self.sesdll),funcparams)
          
        ####### Setbinding Energy:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_double, #bindingEnergy
                                         )        
                
        funcparams = ((1,'binding_energy'))
        self.SetBindingEnergy = funcproto(('WRP_SetBindingEnergy',self.sesdll),funcparams)
 
        ####### GetKineticEnergy:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.POINTER(ctypes.c_double), #kineticEnergy
                                         )        
                
        funcparams = ((1,'kinetic_energy'))
        self.GetKineticEnergy = funcproto(('WRP_GetKineticEnergy',self.sesdll),funcparams)
          
        ####### SetKineticEnergy:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_double, #KineticEnergy
                                         )        
                
        funcparams = ((1,'kinetic_energy'))
        self.SetKineticEnergy = funcproto(('WRP_SetKineticEnergy',self.sesdll),funcparams)
          
        ####### GetExcitationEnergy:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.POINTER(ctypes.c_double), #excitation_energy
                                         )        
                
        funcparams = ((1,'excitation_energy'))
        self.GetExcitationEnergy = funcproto(('WRP_GetExcitationEnergy',self.sesdll),funcparams)
          
        ####### SetExcitationEnergy:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_double, #excitation_energy
                                         )        
                
        funcparams = ((1,'excitation_energy'))
        self.SetExcitationEnergy = funcproto(('WRP_SetExcitationEnergy',self.sesdll),funcparams)
                  
        ####### GetElementVoltage:
        
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #element name                                         
                                         ctypes.POINTER(ctypes.c_double), #element_voltage
                                         )        
                
        funcparams = ((1,'element_name'),(1,'element_voltage'))
        self.GetElementVoltage = funcproto(('WRP_GetElementVoltage',self.sesdll),funcparams)
          
        ####### SetElementEnergy:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #element name                                                                                  
                                         ctypes.c_double, #element_voltage
                                         )        
                
        funcparams = ((1,'element_name'),(1,'element_voltage'))
        self.SetElementVoltage = funcproto(('WRP_ElementVoltage',self.sesdll),funcparams)
                  

        ####### CheckAnalyzerRegion:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         AnalyzerRegion,
                                         ctypes.POINTER(ctypes.c_int), #steps
                                         ctypes.POINTER(ctypes.c_double), #time_ms
                                         ctypes.POINTER(ctypes.c_double), #energyStep
                                         
                                         )        
        
        funcparams = ((1,'analyzer_region'),(1,'steps'),(1,'time_ms'),(1,'energyStep'),)
        self.CheckAnalyzerRegion = funcproto(('WRP_CheckAnalyzerRegion',self.sesdll),funcparams)
        


                                
        ####### initAcquisition:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_bool, 
                                         ctypes.c_bool,
                                         )        
        
        funcparams = ((1,'blockPointReady'),(1,'blockRegionReady'))
        self.InitAcquisition = funcproto(('WRP_InitAcquisition',self.sesdll),funcparams)
                
                                
        ####### startAcquisition:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         )        
        
        funcparams = ()
        self.StartAcquisition = funcproto(('WRP_StartAcquisition',self.sesdll),funcparams)
                

                
        ####### stopAcquisition:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         )        
        
        funcparams = ()
        self.StopAcquisition = funcproto(('WRP_StopAcquisition',self.sesdll),funcparams)
        

        ####### GetAcquiredDataDouble:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #param name
                                         ctypes.c_int, #index
                                         ctypes.POINTER(ctypes.c_double), #data pointer
                                         ctypes.POINTER(ctypes.c_int), #size
                                         )        
        
        funcparams = ((1,'param_name'),(1,'index'),(1,'data_pointer'),(1,'data_size'))
        self.GetAcquiredDataDouble = funcproto(('WRP_GetAcquiredDataDouble',self.sesdll),funcparams)
                
        ####### GetAcquiredDataInteger:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #param name
                                         ctypes.c_int, #index
                                         ctypes.POINTER(ctypes.c_int), #data pointer
                                         ctypes.POINTER(ctypes.c_int), #size
                                         )        
        
        funcparams = ((1,'param_name'),(1,'index'),(1,'data_pointer'),(1,'data_size'))
        self.GetAcquiredDataInteger = funcproto(('WRP_GetAcquiredDataInteger',self.sesdll),funcparams)
                
        ####### GetAcquiredDataString:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #param name
                                         ctypes.c_int, #index
                                         ctypes.c_char_p, #data pointer
                                         ctypes.POINTER(ctypes.c_int), #size
                                         )        
        
        funcparams = ((1,'param_name'),(1,'index'),(1,'data_pointer'),(1,'data_size'))
        self.GetAcquiredDataString = funcproto(('WRP_GetAcquiredDataString',self.sesdll),funcparams)
                
        ####### GetAcquiredDataVectorDouble:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #param name
                                         ctypes.c_int, #index
                                         ctypes.POINTER(ctypes.c_double), #data pointer
                                         ctypes.POINTER(ctypes.c_int), #size
                                         )        
        
        funcparams = ((1,'param_name'),(1,'index'),(1,'data_pointer'),(1,'data_size'))
        self.GetAcquiredDataVectorDouble = funcproto(('WRP_GetAcquiredDataVectorDouble',self.sesdll),funcparams)
                
        ####### GetAcquiredDataVectorInteger:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #param name
                                         ctypes.c_int, #index
                                         ctypes.POINTER(ctypes.c_int), #data pointer
                                         ctypes.POINTER(ctypes.c_int), #size
                                         )        
        
        funcparams = ((1,'param_name'),(1,'index'),(1,'data_pointer'),(1,'data_size'))
        self.GetAcquiredDataVectorInt32 = funcproto(('WRP_GetAcquiredDataVectorInt32',self.sesdll),funcparams)
                                                                                      
                


                                
        ####### waitForPointReady:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_int, 
                                         )        
        
        funcparams = ((1,'timeout_ms'),)
        self.WaitForPointReady = funcproto(('WRP_WaitForPointReady',self.sesdll),funcparams)
                
        ####### waitForRegionReady:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_int, 
                                         )        
        
        funcparams = ((1,'timeout_ms'),)
        self.WaitForRegionReady = funcproto(('WRP_WaitForRegionReady',self.sesdll),funcparams)
                



                                
        ####### continueAcquisition:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         )        
        
        funcparams = ()
        self.ContinueAcquisition = funcproto(('WRP_ContinueAcquisition',self.sesdll),funcparams)



