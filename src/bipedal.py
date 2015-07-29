# -*- coding: utf-8 -*-

""" Este modulo consistira de funciones referentes al estudio del movimiento 
    de un modelo jerarquico en 3D ( marioneta ). Específicamente al movimiento
    de bipedos ó bipedestración y sus movimientos de locomoción. """

import model
import movement
import numpy as np


def footOnFloorFrames( model , heel_joint ,  toeBase_joint , end_joint ):
    """ This function returns a list of the frames where the foot is on the ground."""
    """ Parameters : 
            model : An instance of the class model.Model .
            heel_joint : A string with the name of the joint that resembles the 'Heel' of a chosen foot .
            oeBase_joint : A string with the name of the joint that resembles the 'Toe Base' of a chosen foot .
            end_joint : A string with the name of the joint that resembles the 'End' of a chosen foot .
    """


    frames = movement.jointLowestFrames( model , heel_joint , 1.1 )

    return frames

def strideLength( model , heel_joint ,  toeBase_joint , end_joint ):
    """ This function returns the average stride length of the walk animation of the model"""
    """ Parameters : 
            model : An instance of the class model.Model .
            heel_joint : A string with the name of the joint that resembles the 'Heel' of a chosen foot .
            oeBase_joint : A string with the name of the joint that resembles the 'Toe Base' of a chosen foot .
            end_joint : A string with the name of the joint that resembles the 'End' of a chosen foot .
    """

    frames = footOnFloorFrames( model , heel_joint ,  toeBase_joint , end_joint )

    ### Check if frames size is larger than 1
    if( len( frames ) <= 1  ):
        return False

    ### Find the frames in the middle of a step ( foot on the floor )
    
    stepFrames = []

    startStep = frames[ 0 ]

    for index in range( 1 , len( frames ) ):

        if( abs( frames[ index ] - frames[ index - 1 ] ) > 1 ):
            
            endStep = frames[ index - 1 ]

            stepFrames.append( int( ( endStep + startStep ) / 2 ) )

            startStep = frames[ index ]


    ### Calculate the distance between the consecutive steps
    strideLengthSum = 0 

    heel_position = movement.getJointPosition( model , heel_joint )

    lastStepPosition = None

    for frameIndex in stepFrames:

        currentStepPosition = heel_position[ frameIndex ]

        if( lastStepPosition is None ):

            lastStepPosition = currentStepPosition 

        else:

            strideLengthSum += np.linalg.norm( currentStepPosition - lastStepPosition )

    averageStrideLength = strideLengthSum / ( len( stepFrames ) - 1 )

    return averageStrideLength












