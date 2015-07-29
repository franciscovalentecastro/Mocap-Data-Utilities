""" This file contains functions for analysing and studying the data
    obtained from the MOCAP information obtained from the model"""\

import numpy as np
import scipy.signal
import scipy.linalg
import scipy.interpolate

## Plot 3D
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def getPeriod( signal , frameTime ):
    """ Returns the period in seconds of the given signal using the highest
        peak obtained from the autocorrelation of the signal. """

    ## Use correlation function from numpy library
    autoCorrelation = np.correlate( signal , signal , 'full' )

    ## Get only positive values
    autoCorrelation = autoCorrelation[ autoCorrelation.size // 2 : ]

    ## Find maxima in array
    maximaIndex = scipy.signal.argrelmax( autoCorrelation )[ 0 ]

    ## Find the highest peak
    maxima = [ autoCorrelation[ maximaIndex[ index ] ] for index in range( maximaIndex.size ) ]

    ## Get the frame number of the maximum
    frame = maximaIndex[ np.argmax( maxima ) ]

    return frame * frameTime

def quadraticSurfaceFit( data ):
    """ This function plots a quadratic surface that fits the given data using least squares method."""

    ### Get maxima and minima from the x and y coordinates of the data
    minX = data[ : , 0 ].min()
    minY = data[ : , 1 ].min()

    maxX = data[ : , 0 ].max()
    maxY = data[ : , 1 ].max()

    # regular grid covering the domain of the data
    X,Y = np.meshgrid( np.arange( minX , maxX , 0.1 ), np.arange( minY , maxY , 0.1 ) )
    XX = X.flatten()
    YY = Y.flatten()

    order = 2    # 1: linear, 2: quadratic
    
    if order == 1:
    
        # best-fit linear plane
        A = np.c_[data[:,0], data[:,1], np.ones(data.shape[0])]
        C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])    # coefficients

        # evaluate it on grid
        Z = C[0]*X + C[1]*Y + C[2]

        # or expressed using matrix/vector product
        #Z = np.dot(np.c_[XX, YY, np.ones(XX.shape)], C).reshape(X.shape)

    elif order == 2:

        # best-fit quadratic curve
        A = np.c_[np.ones(data.shape[0]), data[:,:2], np.prod(data[:,:2], axis=1), data[:,:2]**2]
        C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])

        # evaluate it on a grid
        Z = np.dot(np.c_[np.ones(XX.shape), XX, YY, XX*YY, XX**2, YY**2], C).reshape(X.shape)

    # plot points and fitted surface
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, alpha=0.2)
    ax.scatter(data[:,0], data[:,1], data[:,2], c='r', s=50)
    plt.xlabel('X')
    plt.ylabel('Y')
    ax.set_zlabel('Z')
    ax.axis('equal')
    ax.axis('tight')
    plt.show()

def cubicInterpolation( signal ):
    """ Returns a cubic spline interpolation of the data recieved. """

    ### Get frame axis  
    axis = range( len( signal ) )

    ### Get cubic interpolation function
    f = scipy.interpolate.interp1d( axis, signal, kind='cubic')

    return f
