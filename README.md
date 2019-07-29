# SESWrapper
Python wrapper for SES software

## Use
This is a python wrapper for use with Scienta's software for interfacing their hemispherical electron analyzers. This python code provides an interface for the functions exported in SESWrapper.dll. This software has been tested with SESWrapper version 2.7.4, and SES version 1.4.0.

## Warning
This software is able to set voltages to the analyzer without any restrictions or hardware protection mechanisms, and neither does the Scienta software do so internally. It is easy to damage expensive hardware this way, and use of this code is therefore only recommended to very experienced people.

Furthermore, the SESdll is able to read and write to configuration .ini files in the SES software, if errors are handled improperly or closing functions are not called, these may get corrupted. It is therefore recommended to keep backups of these files.



## Overview of files
* **ses_dll.py**: Low level definition of functions as exported in SESWrapper.dll
* **ses_error.py**: Mapping of integer errors as defined in SESWrapper to Python style errors
* **ses_functions.py**: High level definition of functions: this provides another layer that handles all the ctypes conversions
* **ses_measure.py**: A class that implements the functions of a typical photoemission experiment
* **structs.py**: Definition of ctypes classes used by SESWrapper
* **test_ses_wrapper.py**: An example script to run an acquisition

These files are set up such that ses_error.py, structs.py and ses_dll.py do not need to be directly interfaced. The main user API is what is defined in ses_functions.py, and handles all ctypes conversions. At a more high level, ses_measure.py and test_ses_wrapper.py provide higher level code but will probably need to be modified to a user's specific wishes and experimental setup.


## Team Members
* Berend Zwartsenberg, University of British Columbia

