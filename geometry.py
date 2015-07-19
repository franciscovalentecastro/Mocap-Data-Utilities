""" This file contains functions for 3D geometry """

import numpy as np
import math as m

def rotationMatrix( angle_x , angle_y , angle_z ):
	""" Creates a 4x4 rotation matrix that rotates a vector 
		about the axes x , y , z with the angles provided """

	## Angle from degrees to radiasn
	angle_x = m.radians( angle_x )  
	angle_y = m.radians( angle_y ) 
	angle_z = m.radians( angle_z ) 

	rotationAxis_x = np.matrix( [ [ 1 , 0                , 0                 , 0 ], 
								  [ 0 , m.cos( angle_x ) , -m.sin( angle_x ) , 0 ],
								  [ 0 , m.sin( angle_x ) ,  m.cos( angle_x ) , 0 ],
								  [ 0 ,                0 ,                 0 , 1 ] ] , np.dtype(float)  ) 

	rotationAxis_y = np.matrix( [ [  m.cos( angle_y ) , 0 , m.sin( angle_y ) , 0 ], 
								  [                 0 , 1 ,                0 , 0 ],
								  [ -m.sin( angle_y ) , 0 , m.cos( angle_y ) , 0 ],
								  [                 0 , 0 ,                0 , 1 ] ] , np.dtype(float) )

	rotationAxis_z = np.matrix( [ [ m.cos( angle_z ) , -m.sin( angle_z ) , 0 , 0 ], 
								  [ m.sin( angle_z ) ,  m.cos( angle_z ) , 0 , 0 ],
								  [                0 ,                 0 , 1 , 0 ],
								  [                0 ,                 0 , 0 , 1 ] ] , np.dtype(float) )

	rotation = rotationAxis_x * rotationAxis_y * rotationAxis_z

	return rotation

def translationMatrix( trans_x , trans_y , trans_z ):
	""" Creates a 4x4 translation matrix that translates a vector
		using the coefficients given """

	translation = np.matrix( [ [ 1 , 0 , 0 , trans_x ],
							   [ 0 , 1 , 0 , trans_y ],
							   [ 0 , 0 , 1 , trans_z ],
							   [ 0 , 0 , 0 ,       1 ] ] , np.dtype(float) )

	return translation
