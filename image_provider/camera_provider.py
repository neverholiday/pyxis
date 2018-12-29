#!/usr/bin/env python
#
# Copyright (C) 2018  FIBO/KMUTT
#			Written by Nasrun Hayeeyama
#

########################################################
#
#	STANDARD IMPORTS
#

import sys
import os

########################################################
#
#	LOCAL IMPORTS
#

import cv2
import numpy as np

########################################################
#
#	GLOBALS
#

#   FOR TESTING
CAMERA_DEVICE_WEBCAM = '/dev/video0'
CAMERA_DEVICE_EXTERNAL = '/dev/video1'

########################################################
#
#	EXCEPTION DEFINITIONS
#

########################################################
#
#	HELPER FUNCTIONS
#

########################################################
#
#	CLASS DEFINITIONS
#

class Camera( object ):

    def __init__( self, cameraDevice ):

        #   get camera ID
        cameraID = self.changeCameraDeviceToCameraID( cameraDevice )

        #   initial camera capture
        self.cameraCapture = cv2.VideoCapture( cameraID )
        self.cameraCapture.set( cv2.CAP_PROP_FRAME_WIDTH, 640 )
        self.cameraCapture.set( cv2.CAP_PROP_FRAME_HEIGHT, 480 )

        #   initial frame and camera retrive
        self.frame = None
        self.retrive = None

    def changeCameraDeviceToCameraID( self, cameraDevice ):
        """
            Checking camera device
        """

        if cameraDevice == '/dev/video0':
            return 0

        elif cameraDevice == '/dev/video1':
            return 1
        
        else:
            raise TypeError( "{} is not valid".format( cameraDevice ) )
        

    def read( self ):

        #   READ!!!!        
        self.retrive, self.frame = self.cameraCapture.read()

        #   convert to RGB
        self.frame = cv2.cvtColor( self.frame, cv2.COLOR_BGR2RGB )
    
    def end( self ):

        #   release
        self.cameraCapture.release()

if __name__ == "__main__":
    
    #   initial camera capture
    camera = Camera( CAMERA_DEVICE_WEBCAM )

    while True:

        camera.read()

        cv2.imshow( "frame", camera.frame )

        k = cv2.waitKey( 1 )
        if k == ord( 'q' ):
            break

    camera.end()
    cv2.destroyAllWindows()