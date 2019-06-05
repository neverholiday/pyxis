#!/usr/bin/env python
#
# Copyright (C) 2019  FIBO/KMUTT
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


class ImageSeqProvider( object ):

    def __init__( self, imagePathStr ):

        self.cap = cv2.VideoCapture( imagePathStr )

        self.imagePathStr = imagePathStr

        self.idxFrame = 0
        
        self.totalFrameNum = self.cap.get( cv2.CAP_PROP_FRAME_COUNT )

    def nextFrame( self ):
        
        if self.idxFrame < self.totalFrameNum:
            self.idxFrame += 1
    
    def previousFrame( self ):

        if self.idxFrame > 0:
            self.idxFrame -= 1

    def setFrame( self, idxFrame ):
        
        self.idxFrame = idxFrame

    def getFrame( self ):

        self.cap.set( cv2.CAP_PROP_POS_FRAMES, self.idxFrame )

        print self.idxFrame

        ret, frame = self.cap.read()
        
        frameRGB = cv2.cvtColor( frame, cv2.COLOR_BGR2RGB )

        return ret, frameRGB
    
    def release( self ):
        
        self.cap.release()


if __name__ == "__main__":

    frameSeqPath = '/home/neverholiday/work/ball_detector/raw_data/video_raw/capture.avi'
    #frameSeqPath = '/home/neverholiday/jpg_orig/dataTest/iStock-514710226.%04d.jpg'

    imageProvider = ImageSeqProvider( frameSeqPath )

    cv2.namedWindow( 'show', cv2.WINDOW_NORMAL )

    while True:

        ret, image = imageProvider.getFrame()

        imageEIEI = cv2.cvtColor( image, cv2.COLOR_RGB2BGR )

        cv2.imshow( 'show', imageEIEI )

        k = cv2.waitKey( 1 )

        if k == ord( 'q' ):
            break

        elif k == ord( 'd' ):

            imageProvider.nextFrame()

        elif k == ord( 'a' ):

            imageProvider.previousFrame()

    imageProvider.release()
    cv2.destroyAllWindows()