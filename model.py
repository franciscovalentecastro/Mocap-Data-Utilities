""" Este modulo consistira de funciones referentes 
    al manejo de datos de movimiento """
    
""" El tipo de archivos que manejará será .bvh"""

import bvh 
import geometry
import numpy as np

class Model( bvh.BVHReader ):
    """ A hierachical structure of nodes that contains the information
        of a 3D model and frames of its movement obtained from a bvh file
    """
    """ Attributes:
            numberOfFrames : The number of frames in the animation from the file
            frames : A list of the frames. Each frames has a list of values that takes each channel.
            frameTime : Indicates the sampling rate of the data.
            model_position : A dictionary that saves the global position of a joint with its name as the key

        Inherited Attributes:
            filename : Path to the file
            _root : A pointer to the root node of the Model
            _numchannels: The number of channels in the model
    """
    def __init__( self , filename ):
        """ Initializes the values of the attributes """
        bvh.BVHReader.__init__( self , filename )

        self.numberOfFrames = 0
        self.frames = []
        self.frameTime = 0 
    
        self.model_position = {}

    def onMotion( self , frames , dt ):
        """ Called when the 'MOTION' part of the .bvh is read.
            Set the frame values. """
        self.numberOfFrames = frames
        self.frameTime = dt

    def onFrame( self , values ):
        """ Called on every frame of the 'MOTION' section of the .bvh file.
            Add frame to frame list."""
        self.frames.append( values )     

    def setFrame( self , frame_index ):

        """ Calculate the positions of every joint in the 3D model in frame with number index. """
        
        self.channel_position = 0       ## Set index for traversing channels in frame
        self.getNodePosition( np.matrix(np.identity(4), copy=False ), self._root , self.frames[ frame_index ] )

    def getNodePosition( self , parent_transformation , current_node , frameChannels ):
        """ Recursive calculation of node position with transformation matrices """
        
        ## Initialize channel variables
        x_position , y_position , z_position = 0 , 0 , 0
        x_rotation , y_rotation , z_rotation = 0 , 0 , 0

        ## Obtain values for the channel variables
        for channel in current_node.channels:
            if( channel == "Xposition" ):
                x_position = frameChannels[ self.channel_position ]  
            elif( channel == "Yposition" ):
                y_position = frameChannels[ self.channel_position ]  
            elif( channel == "Zposition" ):
                z_position = frameChannels[ self.channel_position ]  
            elif( channel == "Xrotation" ):
                x_rotation = frameChannels[ self.channel_position ]  
            elif( channel == "Yrotation" ):
                y_rotation = frameChannels[ self.channel_position ]  
            elif( channel == "Zrotation" ):
                z_rotation = frameChannels[ self.channel_position ]  

            self.channel_position += 1
        
        ### Create transformation matrix
        transformation =  geometry.translationMatrix( x_position , y_position , z_position )
        transformation *= geometry.rotationMatrix( x_rotation , y_rotation , z_rotation )
        transformation *= geometry.translationMatrix( *current_node.offset )

        ### Save position to the dictionary
        self.model_position[ current_node.name ] = parent_transformation*transformation*np.matrix([[0],[0],[0],[1]])

        ### Recursively call the method with the children of the current node
        for child in current_node.children:
            self.getNodePosition( parent_transformation*transformation , 
                                                                 child , 
                                                         frameChannels )
