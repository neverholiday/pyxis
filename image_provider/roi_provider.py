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
class ROIProvider( object ):
    """
    ROI provider
    """
    
    def __init__( self ):

        #   initial dictionary for store data
        #   NOTE:
        #       key is path.
        #       value is list of tuple top left and bottom right.
        
        #   initial positive dict
        self.positiveRoiDict = dict()

        #   initial negative dict
        self.negativeRoiDict = dict()

        #   initial ROI list
        self.positiveImageList = list()
        self.negativeImageList = list()

    def setPositiveData( self, imagePathStr, topLeftTuple, bottomRightTuple ):
        
        #   set key and data to dictionary
        self.positiveRoiDict[ imagePathStr ] = [ topLeftTuple, bottomRightTuple ]

    def setNegativeData( self, imagePathStr, topLeftTuple, bottomRightTuple ):

        #   set key and data to dictionary
        self.negativeRoiDict[ imagePathStr ] = [ topLeftTuple, bottomRightTuple ]

    def generateROIImage( self, imgWidth = 40, imgHeight = 40 ):
        
        #
        #   loop over data in dictionary generate positive image
        #
        
        for imagePath, roiList in self.positiveRoiDict.iteritems():
            
            #   read image
            img = cv2.imread( imagePath )

            #   get roi information
            #   top left = ( row1, col1 )
            row1 = roiList[ 0 ][ 0 ]
            col1 = roiList[ 0 ][ 1 ]

            #   bottom right = ( row2, col2 )
            row2 = roiList[ 1 ][ 0 ]
            col2 = roiList[ 1 ][ 1 ]

            #   crop by using roi list
            cropImage = img[ row1 : row2, col1 : col2 ]

            #   resize image to desire size
            cropImageResized = cv2.resize( cropImage, ( imgWidth, imgHeight ) )
 
            #   append to roi list
            self.positiveImageList.append( cropImageResized )
        
        
        #
        #   loop over data in dictionary generate negative image
        #

        for imagePath, roiList in self.negativeRoiDict.iteritems():
            
            #   read image
            img = cv2.imread( imagePath )

            #   get roi information
            #   top left = ( row1, col1 )
            row1 = roiList[ 0 ][ 0 ]
            col1 = roiList[ 0 ][ 1 ]

            #   bottom right = ( row2, col2 )
            row2 = roiList[ 1 ][ 0 ]
            col2 = roiList[ 1 ][ 1 ]

            #   crop by using roi list
            cropImage = img[ row1 : row2, col1 : col2 ]

            #   resize image to desire size
            cropImageResized = cv2.resize( cropImage, ( imgWidth, imgHeight ) )
 
            #   append to roi list
            self.negativeImageList.append( cropImageResized )       

    def writeImage( self, savePathStr = '/tmpfs' ):

        #   good path and bad path
        positiveImagePathStr = os.path.abspath( savePathStr ) + '/' + 'positive'
        negativeImagePathStr = os.path.abspath( savePathStr ) + '/' + 'negative'
    
        #   mkdir good and bad under save path
        os.mkdir( positiveImagePathStr )
        os.mkdir( negativeImagePathStr )

        #
        #   write positive image
        #

        for idx, roiImage in enumerate( self.positiveImageList ):
            
            #   get index name
            idxNameStr = str( idx )
            if len( idxNameStr ) == 1:
                idxNameStr = '000' + idxNameStr
            elif len( idxNameStr ) == 2:
                idxNameStr = '00' + idxNameStr
            elif len( idxNameStr ) == 3:
                idxNameStr = '0' + idxNameStr

            #   get file name
            frameNameStr = 'frame' + idxNameStr + '.jpg'

            #   combine with save path for save correctly
            if positiveImagePathStr[ -1 ] != '/':
                savePath_oneImage = positiveImagePathStr + '/' + frameNameStr
            else:
                savePath_oneImage = positiveImagePathStr + frameNameStr

            #   write file by imwrite
            doWrite = cv2.imwrite( savePath_oneImage, roiImage )

            #   check write
            if not doWrite:
                raise TypeError( "Cannot write image at {}".format( savePath_oneImage ) )

        #
        #   write negative image
        #

        for idx, roiImage in enumerate( self.negativeImageList ):
            
            #   get index name
            idxNameStr = str( idx )
            if len( idxNameStr ) == 1:
                idxNameStr = '000' + idxNameStr
            elif len( idxNameStr ) == 2:
                idxNameStr = '00' + idxNameStr
            elif len( idxNameStr ) == 3:
                idxNameStr = '0' + idxNameStr

            #   get file name
            frameNameStr = 'frame' + idxNameStr + '.jpg'

            #   combine with save path for save correctly
            if negativeImagePathStr[ -1 ] != '/':
                savePath_oneImage = negativeImagePathStr + '/' + frameNameStr
            else:
                savePath_oneImage = negativeImagePathStr + frameNameStr

            #   write file by imwrite
            doWrite = cv2.imwrite( savePath_oneImage, roiImage )

            #   check write
            if not doWrite:
                raise TypeError( "Cannot write image at {}".format( savePath_oneImage ) )

if __name__ == "__main__":
    
    #   test imag path
    testImagePath = '/home/neverholiday/work/ball_detector/raw_data/data1/frame0000.jpg'

    testImagePath2 = '/home/neverholiday/work/ball_detector/raw_data/data1/frame0001.jpg'
    
    #   roi point for testing
    topLeft = ( 243, 201 )
    botttomRight = ( 304, 268 )

    topLeft2 = ( 238, 219 )
    bottomRight2 = ( 296, 285 ) 

    #   initial instance of roi provider
    tool = ROIProvider()

    #   set data
    tool.setData( testImagePath, topLeft, botttomRight )
    tool.setData( testImagePath2, topLeft2, bottomRight2 )
    
    #   generate roi image
    tool.generateROIImage()

    #   save
    tool.writeImage( '/tmpfs' )