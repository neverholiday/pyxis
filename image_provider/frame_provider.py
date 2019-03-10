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

TEST_FRAME_PATH = "/home/neverholiday/work/ball_detector/raw_data/data1"

########################################################
#
#	EXCEPTION DEFINITIONS
#

########################################################
#
#	HELPER FUNCTIONS
#

def filterGetOnlyFrameName( dataList, indicateFrameStr = 'frame' ):
	"""
	filter function for get only frame number name
	argument :
		dataList : list of data which have 
		indicateFrameStr : str to indicate frame name
	return :
		dataFilterList : filtered data from data list
	"""

	#	use filter function for filtering
	dataFilterList = filter( lambda bufferStr : indicateFrameStr in bufferStr, dataList )
	
	return dataFilterList

def convertBGR2RGB( frameDataList ):
	
	#	create empty list
	frameRGBList = list()
	
	for image in frameDataList:
	
		#	convert color format to RGB format
		imageRGB = cv2.cvtColor( image.copy(), cv2.COLOR_BGR2RGB )
		
		#	append to list
		frameRGBList.append( imageRGB )

	return frameRGBList
########################################################
#
#	CLASS DEFINITIONS
#

class ImageSequence( object ):
	
	def __init__( self, framePathStr ):
		
		#	get frame path string
		self.framePathStr = framePathStr

		#	initial video capture object to none
		self.capture = None

		#	index pointer to image sequence
		self.indexPointer = 0

		#	get list of path image sequence (absolute path)
		self.framePathList = self.getImageSequenceFromPath()

		#	add number of frame attribute
		self.numFrame = len( self.framePathList )

		#	get list of image sequence
		self.frameList = self.getFrameData()

		#	initial current frame
		self.currentFrameImage = self.frameList[ self.indexPointer ]

		#	initial current frame path
		self.currentFramePath = self.framePathList[ self.indexPointer ]

	def nextFrame( self ):
		
		#	terminate when get over lenght of list
		if self.indexPointer >= len( self.frameList ) - 1:
			self.indexPointer = len( self.frameList ) - 1
			return False

		#	increment index of index pointer
		self.indexPointer += 1

		#	set current frame
		self.currentFrameImage = self.frameList[ self.indexPointer ]

		#	set current frame path
		self.currentFramePath = self.framePathList[ self.indexPointer ]

		return True
		
	def previousFrame( self ):
		
		#	terminate when get lower lenght of list
		if self.indexPointer <= 0:
			self.indexPointer = 0
			return False

		#	decrease index of index pointer
		self.indexPointer -= 1

		#	set current frame
		self.currentFrameImage = self.frameList[ self.indexPointer ]

		#	set current frame path
		self.currentFramePath = self.framePathList[ self.indexPointer ]

		return True

	def setIndexFrame( self, frameIndex ):

		#	terminate when index out of lenght
		if frameIndex > len( self.frameList ) - 1 or frameIndex < 0:
			return

		#	set frame index
		self.indexPointer = frameIndex

		#	set current frame
		self.currentFrameImage = self.frameList[ self.indexPointer ]

		#	set current frame path
		self.currentFramePath = self.framePathList[ self.indexPointer ]

	def getImageWithMask( self, lowerBound, upperBound ):

		#	change to hsv image
		hsvImage = cv2.cvtColor( self.currentFrameImage, cv2.COLOR_RGB2HSV )

		#	limit with range of hsv value, get mask
		mask = cv2.inRange( hsvImage, lowerBound, upperBound )

		#	bitwise-and with mask for get res and return it
		res = cv2.bitwise_and( self.currentFrameImage, self.currentFrameImage, mask = mask )

		return res

	def getImageSequenceFromPath( self, indicateFrameStr = 'frame' ):
		
		#	get abs path
		absPath = os.path.abspath( self.framePathStr )

		#	get list of image
		framePathList = os.listdir( absPath )

		#	filter and get only frame name from indicate frame string
		framePathList = filter( lambda bufferStr : indicateFrameStr in bufferStr, framePathList )

		#	sort frame number
		framePathList.sort()

		#	add abspath to frame name
		framePathList = map( lambda frameNameStr : self.framePathStr + '/' + frameNameStr, framePathList )

		#	return it!!!
		return framePathList

	def getFrameData( self, enableBlur = True ):

		#	get frame data
		frameData = map( cv2.imread, self.framePathList )
	
		#	change bgr to rgb
		frameData = convertBGR2RGB( frameData )
		
		return frameData

if __name__ == "__main__":
	
	#	define frame path str
	FRAME_PATH_STR = "/home/neverholiday/work/ball_detector/raw_data/data1"

	#	Create instance of provider
	frameProvider = ImageSequence( FRAME_PATH_STR )

	while True:

		cv2.imshow( "frame", frameProvider.currentFrameImage )

		k = cv2.waitKey( 1 )
		if k == ord( 'a' ):
			
			frameProvider.previousFrame()
			print frameProvider.indexPointer

		if k == ord( 'd' ):

			frameProvider.nextFrame()
			print frameProvider.indexPointer
		if k == ord( 'q' ):
			break
	cv2.destroyAllWindows()
