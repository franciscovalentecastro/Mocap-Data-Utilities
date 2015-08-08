# -*- coding: utf-8 -*-

""" This file contains functions for visualization of the motion capture data. """

import numpy as np
import mayavi.mlab as mlab

from traits.api import HasTraits, Instance, Range, on_trait_change
from traitsui.api import View, Item, HGroup
from mayavi.core.ui.api import SceneEditor, MlabSceneModel

class Model_Visualization(HasTraits):
    "The class that contains the dialog"
    frame = Range(0, 300, 0)
    scene = Instance(MlabSceneModel, ())
    plotEdges = []

    def __init__(self , model ):
        HasTraits.__init__(self)

        ## Save model to object
        self.model = model

        ## Set value range
        ## self.frame = Range(0, self.model.numberOfFrames - 1 , 0)

        ## Set to initial frame
        self.model.setFrame( 0 )

        ## Get every joint coordinates in the frame
        x = np.array( [ self.model.model_position[ key ][ 0 , 0 ] for key in self.model.model_position ] ) 
        y = np.array( [ self.model.model_position[ key ][ 1 , 0 ] for key in self.model.model_position ] )
        z = np.array( [ self.model.model_position[ key ][ 2 , 0 ] for key in self.model.model_position ] )

        ## Plot Edges
        ##for edge in self.model.model_edges:
        ##    self.plotEdges.append( self.scene.mlab.plot3d( edge[ : , 0 ] , edge[ : , 2 ] , edge[ : , 1 ]  , color=(0 , 0 ,0) ) )

        ## Plot floor
        s = np.array( 100 * [ 100 * [0] ] )
        self.scene.mlab.surf( s , representation = 'wireframe' )        

        # Populating our plot
        self.plotJoints = self.scene.mlab.points3d(x, z, y, color=(0 , 0 ,0), scale_factor=.75 )

    @on_trait_change('frame')
    def update_plot( self ):


        ## Set to initial frame
        self.model.setFrame( self.frame )

        ## Get every joint coordinates in the frame
        x = np.array( [ self.model.model_position[ key ][ 0 , 0 ] for key in self.model.model_position ] ) 
        y = np.array( [ self.model.model_position[ key ][ 1 , 0 ] for key in self.model.model_position ] )
        z = np.array( [ self.model.model_position[ key ][ 2 , 0 ] for key in self.model.model_position ] )
        
        ## Set surce to new joint positions
        self.plotJoints.mlab_source.set( x=x, y=z, z=y )

        ## Set source to new edge posistion
        ##for index , edge in enumerate( self.model.model_edges ):
        ##    self.plotEdges[ index ].mlab_source.set( x = edge[ : , 0 ] , y = edge[ : , 2 ] , z = edge[ : , 1 ] )

    # Describe the dialog
    view = View( Item('scene', height=300, show_label=False,
                   editor=SceneEditor() ), HGroup('frame'), resizable=True )

def plotModel( model ):
    """ Animates the model """
    Model_Visualization( model ).configure_traits()

def plotFrame( model , frameNumber ):
    """ Plots a frame of the model """

    ## Set frame
    model.setFrame( frameNumber )

    ## Get every joint coordinates in the frame
    x = np.array( [ model.model_position[ key ][ 0 , 0 ] for key in model.model_position ] ) 
    y = np.array( [ model.model_position[ key ][ 1 , 0 ] for key in model.model_position ] )
    z = np.array( [ model.model_position[ key ][ 2 , 0 ] for key in model.model_position ] )

    mlab.points3d( x , y , z , color=(0 , 0 ,0), scale_factor=.5 )

    


 