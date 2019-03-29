#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 08:46:41 2019

@author: berend
"""



##error wrapper:


class SESError:
    
    def __init__(self,verbose = False):
        """
        ta
        """
        self.verbose = False
        self.errors = { -1 : RuntimeError('ERR_UNKNOWN'),
                        -2 : RuntimeError('ERR_FAIL'),
                        -3 : RuntimeError('ERR_NOT_INITIALIZED'),
                        -4 : RuntimeError('ERR_NOT_APPLICABLE'),
                        -5 : RuntimeError('ERR_PARAMETER_NOT_FOUND'),
                        -6 : RuntimeError('ERR_INDEX'),
                        -7 : RuntimeError('ERR_INCORRECT_ELEMENT_SET'),
                        -8 : RuntimeError('ERR_INCORRECT_LENS_MODE'),
                        -9 : RuntimeError('ERR_INCORRECT_PASS_ENERGY'),
                        -10 : RuntimeError('ERR_INCORRECT_ANALYZER_REGION'),
                        -11 : RuntimeError('ERR_INCORRECT_DETECTOR_REGION'),
                        -12 : RuntimeError('ERR_READONLY'),
                        -13 : RuntimeError('ERR_NO_INSTRUMENT'),
                        -14 : RuntimeError('ERR_ACQUIRING'),
                        -15 : RuntimeError('ERR_INITIALIZE_FAIL'),
                        -16 : RuntimeError('ERR_LOAD_LIBRARY'),
                        -17 : RuntimeError('ERR_OPEN_INSTRUMENT'),
                        -18 : RuntimeError('ERR_QT_RUNNING'),
                        -19 : RuntimeError('ERR_INVALID_DIR'),
                        8 : RuntimeError('ERR_TIMEOUT'),
                        9 : RuntimeError('ERR_NOT_IMPLEMENTED'),
                       }
      
        self.warnings = {313 : 'Failed to zero supplies',
                         }
    
    def error(self, intcode):
        
        ## do handling for SES errors with a dictionary
        ## if verbose, print "Ran OK"
        if type(intcode) != int:
            raise RuntimeError('Return code is not integer')
        
        
        if intcode in self.errors:
            raise self.errors[intcode]
        elif intcode < 0:
            raise RuntimeError('Unkown error occured with code {}'.format(intcode))
                
        elif intcode > 0:
            
            if intcode in self.warnings:
                print(self.warnings[intcode])
            else:
                print('An unkown warning occured with code {}'.format(intcode))
                
        else:
            if self.verbose:
                print('Return code OK')
                
                


            