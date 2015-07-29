""" Este modulo consistira de funciones referentes al movimiento 
    de un modelo jerarquico en 3D ( marioneta ) y su estudio """

import model
import math
import matplotlib.pyplot as plt
import itertools
import numpy as np

### 3D plot 
from mpl_toolkits.mplot3d import Axes3D

def getJointPosition( model , joint_name ):
    """ Calculates the position of the given joint in every frame."""
    jointPosition = []

    ### Calculate every frame
    for frame_index in range( model.numberOfFrames ):
        model.setFrame( frame_index )
        jointPosition.append( model.model_position[ joint_name ] )

    return jointPosition

def getJointAngle( model , joint_name ):
    """ Returns a list with the rotation in euler angles of the given joint. """
    jointAngle = []

    ### Calculate every frame
    for frame_index in range( model.numberOfFrames ):
        model.setFrame( frame_index )
        jointAngle.append( model.model_eulerAngles[ joint_name ] )

    return jointAngle
def getJointSpeed( model , joint_name ):
        """ Calculates the average speed of the joint between each succesive frames. """
        jointSpeed = []

        ### Initialize model to the position in the first frame
        model.setFrame( 0 )  
        current_position = model.model_position[ joint_name ]  

        ### Calculate average speed of succesive joint positions
        for frame_index in range( 1 , model.numberOfFrames ):
            model.setFrame( frame_index )
            previous_position = current_position
            current_position = model.model_position[ joint_name ]
            
            jointSpeed.append( np.linalg.norm( current_position - previous_position ) / model.frameTime )

        return jointSpeed

def getJointAcceleration( model , joint_name ):
    """ Calculates the acceleration of the joint between each succesive frames. """
    jointAcceleration = []

    jointSpeed = getJointSpeed( model , joint_name )

    ### Calculate average accelearation from succesive joint speed
    for index in range( 1 , len( jointSpeed ) ):

        jointAcceleration.append( ( jointSpeed[ index ] - jointSpeed[ index - 1 ] ) / model.frameTime  )

    return jointAcceleration

def plotJointPositionCoordinate( model , joint_name , coordinate ):
    
    """ Plot the given coordinate of the joint as a function of the frames"""

    ### Check if argument joint_name is a string , convert to string
    if( type(joint_name) is str ):
        joint_name = [ joint_name ]

    ### Set color cycle for the plots
    colors = itertools.cycle(['r', 'g', 'b', 'y'])

    for joint in joint_name:

        ### Get corrdinates of a joint
        jointPositionList = getJointPosition( model , joint )

        ### Generate coordinate value array
        plotCoordinate = [ position[ coordinate,0 ] for position in jointPositionList ]
        axis = [ x for x in range( 0 , model.numberOfFrames ) ]

        ### Plot the given coordinate
        plt.plot( axis , plotCoordinate , 'ro' , color = next(colors) )
    
    ### Show plot
    plt.show()

def plotJointAngleCoordinate( model , joint_name , coordinate ):
    
    """ Plot the given coordinate of the joint as a function of the frames"""

    ### Check if argument joint_name is a string , convert to string
    if( type(joint_name) is str ):
        joint_name = [ joint_name ]

    ### Set color cycle for the plots
    colors = itertools.cycle(['r', 'g', 'b', 'y'])

    for joint in joint_name:

        ### Get corrdinates of a joint
        jointAngleList = getJointAngle( model , joint )

        ### Generate coordinate value array
        plotCoordinate = [ angle[ coordinate ] for angle in jointAngleList ]
        axis = [ x for x in range( 0 , model.numberOfFrames ) ]

        ### Plot the given coordinate
        plt.plot( axis , plotCoordinate , 'ro' , color = next(colors) )
    
    ### Show plot
    plt.show()

def jointLowestFrames( model , joint_name , error ):
    """ Find the frames where the given joint is in its lowest position. Given that the Y axis 
        is the vertical axis """
    joint_position = getJointPosition( model , joint_name )

    joint_height = [ coordinate[ 1,0 ] for coordinate in joint_position ]

    min_height = min( joint_height )

    frames = []

    for index in range( 0 , len( joint_height ) ):

        if( abs( joint_height[ index ] - min_height ) < error ):

            frames.append( index )

    return frames

def getJointLocalWorkspace( model , joint_name ):
    """ Returns the observed positions of the joint in the local workspace. """
    
    ### Get joint node
    joint = model.getJointByName( joint_name )

    ### Local workspace positions
    jointLocalWorkspace = []

    ### Calculate every frame
    for frame_index in range( model.numberOfFrames ):
        model.setFrame( frame_index )
        
        local_position = np.matrix( joint.transformation ) * np.matrix( [ [0] ,[0] ,[0] ,[1] ] )

        jointLocalWorkspace.append( [ local_position[0,0] , local_position[1,0] , local_position[2,0] ] )

    return jointLocalWorkspace


def plotJointLocalWorkspace( model , joint_name ):
    """ 3D plot of the angles of a joint in the unit sphere """

    jointLocalWorkspace = getJointLocalWorkspace( model , joint_name )
    
    x = [ element[ 0 ] for element in jointLocalWorkspace ]
    y = [ element[ 1 ] for element in jointLocalWorkspace ]
    z = [ element[ 2 ] for element in jointLocalWorkspace ]

    ### 3D plot the positions
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(x, y, z, c='r', marker='o')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()

def plotFrame( model , frameNumber ):
    """ Plots a frame of the model """

    ## Set frame
    model.setFrame( frameNumber )

    ## Get every joint coordinates in the frame
    x = [ model.model_position[ key ][ 0 , 0 ] for key in model.model_position ] 
    y = [ model.model_position[ key ][ 1 , 0 ] for key in model.model_position ]
    z = [ model.model_position[ key ][ 2 , 0 ] for key in model.model_position ]

    ## 

    ## Plot model
    fig = plt.figure( figsize=plt.figaspect( 1 ) )
    ax = fig.add_subplot( 111 , projection='3d' )
    ax.set_aspect('equal')

    ax.scatter( x , y , z )

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    ## Set bounding box for the plot
    max_range = max( [ max( x ) - min( x ), max( y ) - min( y ) , max( z ) - min( z ) ] ) / 2.0

    mean_x = np.mean( x )
    mean_y = np.mean( y )
    mean_z = np.mean( z )
    
    ax.set_xlim( mean_x - max_range, mean_x + max_range )
    ax.set_ylim( mean_y - max_range, mean_y + max_range )
    ax.set_zlim( mean_z - max_range, mean_z + max_range )
    
    plt.show()
