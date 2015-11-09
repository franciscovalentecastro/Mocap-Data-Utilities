## Fast Fourier Transform Test ##

import model as m
modelo =  m.Model( "../sample-mocap-data//49//49_01_ignoreFirstFrame.bvh" )
modelo.read()

import movement as mov
data = mov.getJointPosition( modelo , "LeftFoot" ) 
signal = [ position[ 1 , 0 ] for position in data ]

## Test Fast Fourier ##

import data as dt
f = dt.cubicInterpolation( signal )

axis = range( 0 , len( signal ) )

x = np.linspace( 0 , len( signal ) - 1 , 10000 )
y = f( x )

plt.plot( axis, signal, 'ro', x , y , 'g-' )
plt.show()

import numpy as np
import matplotlib.pyplot as plt

sp = np.fft.fft( signal )
freq = np.fft.fftfreq(len( signal) , .001  )
plt.plot(freq, np.absolute( sp ) )

plt.show()