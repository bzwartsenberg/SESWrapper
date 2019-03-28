#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 13:37:38 2019

@author: berend
"""

import ctypes
from structs import AnalyzerRegion, DetectorRegion, DetectorInfo

class SESWrapper:
    
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

        #####Set property Integer:
        
        
        sesSetPropertyIntegerProto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #param name
                                         ctypes.c_int, #
                                         ctypes.POINTER(ctypes.c_int) #param value (actually needs to be an int_p)
                                         )
        
        sesSetPropertyIntegerParams = ((1,'param_name'),(1,'unk'),(1,'param_value'))
        
        self.SetPropertyInteger = sesSetPropertyIntegerProto(('WRP_SetPropertyInteger',self.sesdll),sesSetPropertyIntegerParams)
        
        
        #####Set property String: ##note: can make a function that automatically encodes strings as well
        sesSetPropertyStringProto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #param name
                                         ctypes.c_int, #
                                         ctypes.c_char_p #
                                         )
        
        sesSetPropertyStringParams = ((1,'param_name'),(1,'unk'),(1,'param_value'))
        
        self.SetPropertyString = sesSetPropertyStringProto(('WRP_SetPropertyString',self.sesdll),sesSetPropertyStringParams)

        ######Set property Double:
        
        sesSetPropertyDoubleProto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #param name
                                         ctypes.c_int, #
                                         ctypes.POINTER(ctypes.c_double) #param value (actually needs to be an int_p)
                                         )
        
        sesSetPropertyDoubleParams = ((1,'param_name'),(1,'unk'),(1,'param_value'))
        
        self.SetPropertyDouble = sesSetPropertyDoubleProto(('WRP_SetPropertyDouble',self.sesdll),sesSetPropertyDoubleParams)
        
        
        ######Load instrument
        
        sesLoadInstrumentProto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         ctypes.c_char_p, #file name
                                         )
        
        sesLoadInstrumentParams = ((1,'file_name'),)
        
        self.LoadInstrument = sesLoadInstrumentProto(('WRP_LoadInstrument',self.sesdll),sesLoadInstrumentParams)
        
        ####### setAnalyzer:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         AnalyzerRegion,
                                         )        
        
        funcparams = ((1,'analyzer_region'),)
        self.SetAnalyzerRegion = funcproto(('WRP_SetAnalyzerRegion',self.sesdll),funcparams)
        

        ####### getAnalyzer:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         AnalyzerRegion,
                                         )        
        
        funcparams = ((1,'analyzer_region'),)
        self.GetAnalyzerRegion = funcproto(('WRP_GetAnalyzerRegion',self.sesdll),funcparams)
        
        ####### setDetector:
        
        funcproto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         DetectorRegion,
                                         )        
        
        funcparams = ((1,'detector_region'),)
        self.SetDetectorRegion = funcproto(('WRP_SetDetectorRegion',self.sesdll),funcparams)
                
        ####### getDetector:
        
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
                                                                                      
                
        
        ######Finalize:
        
        sesFinalizeProto = ctypes.WINFUNCTYPE(
                                         ctypes.c_int,
                                         )
        
        sesFinalizeParams = ()
        
        self.Finalize = sesFinalizeProto(('WRP_Finalize',self.sesdll),sesFinalizeParams)
        




