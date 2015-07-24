""" This file contains functions for analysing and studying the data
    obtained from the MOCAP information obtained from the model"""\

import numpy as np
import scipy.signal as sig

def getPeriod( signal , frameTime ):
    """ Returns the period in seconds of the given signal using the highest
        peak obtained from the autocorrelation of the signal. """

    ## Use correlation function from numpy library
    autoCorrelation = np.correlate( signal , signal , 'full' )

    ## Get only positive values
    autoCorrelation = autoCorrelation[ autoCorrelation.size // 2 : ]

    ## Find maxima in array
    maximaIndex = sig.argrelmax( autoCorrelation )[ 0 ]

    ## Find the highest peak
    maxima = [ autoCorrelation[ maximaIndex[ index ] ] for index in range( maximaIndex.size ) ]

    ## Get the frame number of the maximum
    frame = maximaIndex[ np.argmax( maxima ) ]

    return frame * frameTime



