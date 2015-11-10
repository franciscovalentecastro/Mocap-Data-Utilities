## Fast Fourier Transform Test ##
import numpy as np
import model as m
import movement as mov
import data as dt
import matplotlib.pyplot as plt
import os

directory = "/home/francisco/Documents/Programming/Mocap-Data-Utilities/sample-mocap-data/Walking/"
listOfFilenames = next( os.walk( directory + "BVH/" ) )[ 2 ]  

listOfFrequenciesX = []
listOfFrequenciesY = []

for filename in listOfFilenames :

	print( filename )

	modelo =  m.Model( directory + "BVH/" + filename )
	modelo.read()

	data = mov.getJointPosition( modelo , "LeftFoot" ) 
	signal = [ position[ 1 , 0 ] for position in data ]
	axis = range( 0 , len( signal ) )

	f = dt.cubicInterpolation( signal )
	x = np.linspace( 0 , len( signal ) - 1 , 10000 )
	y = f( x )

	plt.plot( axis, signal, 'ro', x , y , 'g-' )
	plt.savefig( directory + "Images/" + filename + "_LeftFoot_Z_Coordinate.png" )
	plt.clf()

	maxFrequencies = dt.signalImportantFrequencies( signal , modelo.frameTime , filename ) [ 0 : 2 ]
	
	""" listOfFrequenciesX.append( maxFrequencies[ 0 ] )
	listOfFrequenciesY.append( maxFrequencies[ 1 ] ) """

""" plt.axis( [ 0 , 3 , 0 , 3 ] )
plt.scatter( listOfFrequenciesX , listOfFrequenciesY , color = 'red' )
plt.show()

print( [ ( listOfFrequenciesX[ i ] , listOfFrequenciesY[ i ] ) for i in range( len( listOfFrequenciesX ) ) ] ) """

