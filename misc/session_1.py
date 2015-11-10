### Sesión

########### Cubic spline interpolation

import model as m
modelo =  m.Model( "../sample-mocap-data//05//05_01_ignoreFirstFrame.bvh" )
modelo.read()

import movement as mov
data = mov.getJointPosition( modelo , "LeftFoot" ) 
signal = [ position[ 1 , 0 ] for position in data ]

import data as dt
f = dt.cubicInterpolation( signal )

import numpy as np
import matplotlib.pyplot as plt

axis = range( 0 , len( signal ) )

x = np.linspace( 0 , len( signal ) - 1 , 10000 )
y = f( x )

plt.plot( axis, signal, 'ro', x , y , 'g-' )
plt.show()

########### Plot speed and acceleration

import model as m
modelo =  m.Model( "sample-mocap-data//05//05_01_ignoreFirstFrame.bvh" )
modelo.read()

import movement as mov

speed = mov.getJointSpeed( modelo , "LeftFoot" )
acceleration = mov.getJointAcceleration( modelo , "LeftFoot" )

import matplotlib.pyplot as plt
axSpeed = range( len( speed ) )
axAcceleration = range( len( acceleration ) )

plt.plot( axSpeed , speed , 'g-')
plt.show()
plt.plot( axAcceleration, acceleration , "r-" )
plt.show()

########### Get stride length 

import model as m
modelo =  m.Model( "sample-mocap-data//05//05_01_ignoreFirstFrame.bvh" )
modelo.read()

import bipedal as bip
bip.strideLength( modelo , "LeftFoot" ,  "LeftToeBase" , "LeftToeBase_EndSite" )

import movement as mov
mov.jointLowestFrames( modelo , "LeftFoot" , 1.1 )

mov.plotJointPositionCoordinate( modelo , [ "LeftFoot" , "LeftToeBase" , "LeftToeBase_EndSite" ] , 1 ) 


########### Get period of discrete data

import model as m
modelo =  m.Model( "sample-mocap-data//05//05_01_ignoreFirstFrame.bvh" )
modelo.read()

import movement as mov
data = mov.getJointPosition( modelo , "LeftFoot" ) 
signal = [ position[ 1 , 0 ] for position in data ]


import data as dt
dt.getPeriod( signal , modelo.frameTime )

########### Plot Local workspace and fit a surface

import model as m
modelo =  m.Model( "sample-mocap-data//05//05_01_ignoreFirstFrame.bvh" )
modelo.read()

import movement as mov
import numpy as np
import pdb
import data as dt

data = mov.getJointLocalWorkspace( modelo , "LeftFoot" )
data = np.array( data )

dt.quadraticSurfaceFit( data )

## Forearm

data = mov.getJointLocalWorkspace( modelo , "LeftForeArm" )
data = np.array( data )

dt.quadraticSurfaceFit( data )

#########################
from mayavi import mlab
import numpy as np
import model as m

modelo =  m.Model( "../sample-mocap-data//05//05_01.bvh" )
modelo.read()

## Set frame
modelo.setFrame( 0 )

## Get every joint coordinates in the frame
x = np.array( [ modelo.model_position[ key ][ 0 , 0 ] for key in modelo.model_position ] ) 
y = np.array( [ modelo.model_position[ key ][ 1 , 0 ] for key in modelo.model_position ] )
z = np.array( [ modelo.model_position[ key ][ 2 , 0 ] for key in modelo.model_position ] )

s = mlab.points3d( x , y , z , color=(0 , 0 ,0), scale_factor=.5 )

###############################
import visualization as vis
import numpy as np
import model as m

modelo =  m.Model( "../sample-mocap-data//02//02_01.bvh" )
modelo.read()

vis.plotModel( modelo )


###############################
import numpy as np
import mayavi.mlab as mlab

y = np.array( 100*[ 100 * [0] ] )
x , z = np.mgrid[ -50 : 50 , -50 : 50 ]

mlab.points3d( x.flatten() , y.flatten() , z.flatten() )


### Measure set frame
import model as m
modelo =  m.Model( "../sample-mocap-data//02//02_01.bvh" )
modelo.read()

import timeit 
timeit.timeit( "modelo.setFrame( 1 )" ,  setup = " import model as m modelo =  m.Model( "../sample-mocap-data//02//02_01.bvh" ) modelo.read() " )