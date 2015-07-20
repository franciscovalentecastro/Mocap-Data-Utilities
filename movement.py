""" Este modulo consistira de funciones referentes al movimiento 
    de un modelo jerarquico en 3D ( marioneta ) y su estudio """

import model as m
import matplotlib.pyplot as plt
import itertools

def getJointPosition( model , joint_name ):
    """ Calculates the position of the given joint in every frame."""
    jointPosition = []

    ### Calculate every frame
    for frame_index in range( model.numberOfFrames ):
        model.setFrame( frame_index )
        jointPosition.append( model.model_position[ joint_name ] )

    return jointPosition

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
            
            jointSpeed.append( np.linalg.norm( current_position - previous_position ) / self.frameTime )

        return jointSpeed

def plotJointCoordinate( model , joint_name , coordinate ):
    
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
