#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 23 14:00:29 2019

@author: berend
"""

### test API:

from structs import AnalyzerRegion, DetectorRegion, DetectorInfo
from sesFunctions import SESWrapper
import ctypes
import numpy as np


if __name__ == '__main__':
    
    
    dllpath = 'C:\seswrapper_2.7.4_Win64\SESWrapper.dll'
    ses_dir = 'C:/SES_1.4.0-r30_Win64'
    ses_instrument = ses_dir + '/dll/SESInstrument.dll'
    inst_path =  ses_dir + '/data/9ES219L_Instrument.dat'

    
    ses = SESWrapper(dllpath)
    
    #following:
    #/Users/berend/Documents/temp/seswrapper/seswrapper/ftp.scienta.se/SES/SESWrapper/seswrapper_2.7.4_Win64/doc/html/examples_page.html

    print(ses.SetPropertyString('lib_working_dir'.encode('ASCII'),0,ses_dir.encode('ASCII')))
    print(ses.SetPropertyString('instrument_library'.encode('ASCII'),0,ses_instrument.encode('ASCII')))
    
    
    ##note: to get this to run, go to ses/ini/detectorgraph.ini
    # and set direct_viewer to false
    #if you do that, the ses software will not load the viewer on startup, 
    #but this will run successfuly     
    print(ses.Initialize(0))
    
    
    print(ses.LoadInstrument(inst_path.encode('ASCII')))
    
    
    print(ses.setPropertyString('element_set'.encode('ASCII'), -1, 'Low Pass (Laser)'.encode('ASCII')))
    print(ses.setPropertyString('lens_mode'.encode('ASCII'), -1, 'Transmission'.encode('ASCII')))
    
    Epass = 10.
    print(ses.setPropertyDouble('pass_energy'.encode('ASCII'), -1, Epass))
    
    
    ##set detector and analyzer
    
    info = DetectorInfo()
    print(ses.GetDetectorInfo(info))
    print('Number of x channels: ',info.xChannels_)

    detector = DetectorRegion()
    detector.firstXChannel_ = 0
    detector.lastXChannel_ = 500
    detector.firstYChannel_ = 0
    detector.lastYChannel_ = 500
    detector.slices_ = 1
    detector.adcMode_ = True
    
    print(ses.SetDetectorRegion(detector))
    
    
    analyzer = AnalyzerRegion()
    analyzer.fixed_ = False
    analyzer.highEnergy_ = 90
    analyzer.lowEnergy_ = 82
#    analyzer.centerEnergy_ = 86
    analyzer.energyStep_ = 0.2
    analyzer.dwellTime_ = 500

    print(ses.SetAnalyzerRegion(analyzer))
    
    #test:
    analyzer2 = AnalyzerRegion()
    print(ses.GetAnalyzerRegion(analyzer2))
    
    print('Returned analyzer has lowenergy', analyzer2.lowenergy_)
    
    
    
    ses.InitAcquisition(False, True)
    channels = ctypes.c_int(0)
    print(ses.GetAcquiredData('acq_channels'.encode('ASCII'), 0, channels, ctypes.sizeof(channels)))

    spectrum = (ctypes.c_double * channels.value)()
    
    print('Generated spectrum has size:', ctypes.sizeof(spectrum))
    
    for i in range(10):
        print(ses.startAcquisition())
        print(ses.WaitForRegionReady(-1))
        print(ses.ContinueAcquisition())
    
    print(ses.getAcquiredData('acq_spectrum'.encode('ASCII'), 0, spectrum, ctypes.sizeof(spectrum)))
          
    
    
    spectrum_np = np.array(spectrum)
    
    np.savetxt('test.txt',spectrum_np)
    
    print(ses.Finalize())
    






