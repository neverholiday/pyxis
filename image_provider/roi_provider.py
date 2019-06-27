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

import random

########################################################
#
#	LOCAL IMPORTS
#

import cv2
import numpy as np

import yaml

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

		#   initial positive and negative dictionary
		self.allPosAndNegDict = { "Positive" : self.positiveRoiDict, "Negative" : self.negativeRoiDict }

		#   initial ROI list
		self.positiveImageList = list()
		self.negativeImageList = list()

	def setPositiveData( self, imagePathStr, topLeftTuple, bottomRightTuple ):
		
		#   check key
		if imagePathStr not in self.positiveRoiDict.keys():
			
			#   create empty list
			self.positiveRoiDict[ imagePathStr ] = list()

			#   append to empty list
			self.positiveRoiDict[ imagePathStr ].append( ( topLeftTuple, bottomRightTuple ) )

		else:
			
			#   just append
			self.positiveRoiDict[ imagePathStr ].append( ( topLeftTuple, bottomRightTuple ) )

	def setNegativeData( self, imagePathStr, topLeftTuple, bottomRightTuple ):

		#   check key
		if imagePathStr not in self.negativeRoiDict.keys():
			
			#   create empty list
			self.negativeRoiDict[ imagePathStr ] = list()

			#   append to empty list
			self.negativeRoiDict[ imagePathStr ].append( ( topLeftTuple, bottomRightTuple ) )

		else:
			
			#   just append
			self.negativeRoiDict[ imagePathStr ].append( ( topLeftTuple, bottomRightTuple ) )
	
	def randomPositionNegative( self, imagePathStr, limitWidth, limitHeight ):
		
		
		pass
		
		
#		#	set flag for loop set random position
#		flagLoopRandom = True
#		
#		while flagLoopRandom:
#
#			#	random row position
#			yTopLeft = random.randint( 0, limitHeight )
#
#			#	random column position
#			xTopLeft = random.randint( 0, limitWidth )
#			
#			#	generate bottom left 
#			yBottomRight = yTopLeft + 100
#			xBottomRight = xTopLeft + 100
#			
#			#	loop every positive bounding box
#			for positivePos in self.positiveROIDict[ imagePathStr ]:
#				
#				#	check top left
#				checkInside = ( positivePos[ 0 ][ 0 ] < xTopLeft < positivePos[ 1 ][ 0 ] && positivePos[ 0 ][ 1 ] < yTopLeft < positivePos[ 1 ][ 1 ] ):
					 
				 
		

	def saveDataDict( self, savePath  ):

		with open( savePath, 'w' ) as streamFile:
			
			yaml.dump( self.allPosAndNegDict, stream = streamFile )

		print "Save yaml file at {}".format( savePath )

	def loadDataDict( self, yamlPath ):

		with open( yamlPath, 'r' ) as streamFile:

			self.allPosAndNegDict = yaml.load( streamFile )
			self.positiveRoiDict = self.allPosAndNegDict[ "Positive" ]
			self.negativeRoiDict = self.allPosAndNegDict[ "Negative" ]


	def generateROIImage( self, imgWidth = 40, imgHeight = 40 ):
		
		#
		#   loop over data in dictionary generate positive image
		#
		
		print "[INFO] Generate positive roi image "
		for imagePath, roiList in self.positiveRoiDict.iteritems():
			
			#   read image
			img = cv2.imread( imagePath )

			for roiTuple in roiList:

				#   get roi information
				#   top left = ( row1, col1 )
				row1 = roiTuple[ 0 ][ 0 ]
				col1 = roiTuple[ 0 ][ 1 ]

				#   bottom right = ( row2, col2 )
				row2 = roiTuple[ 1 ][ 0 ]
				col2 = roiTuple[ 1 ][ 1 ]

				print roiTuple

				row1, row2 = ( row1, row2 )if row2 > row1 else ( row2, row1 )
				col1, col2 = ( col1, col2 ) if col2 > col1 else (col2, col1)

				#   crop by using roi list
				cropImage = img[ row1 : row2, col1 : col2 ]

				#   resize image to desire size
				cropImageResized = cv2.resize( cropImage, ( imgWidth, imgHeight ) )
	
				#   append to roi list
				self.positiveImageList.append( cropImageResized )
		
		print "[INFO] Finish generate positive roi image "
		
		
		#
		#   loop over data in dictionary generate negative image
		#

		print "[INFO] Generate negative roi image "
		for imagePath, roiList in self.negativeRoiDict.iteritems():
			
			#   read image
			img = cv2.imread( imagePath )

			for roiTuple in roiList:
			
				#   get roi information
				#   top left = ( row1, col1 )
				row1 = roiTuple[ 0 ][ 0 ]
				col1 = roiTuple[ 0 ][ 1 ]

				#   bottom right = ( row2, col2 )
				row2 = roiTuple[ 1 ][ 0 ]
				col2 = roiTuple[ 1 ][ 1 ]

				row1, row2 = (row1, row2) if row2 > row1 else (row2, row1)
				col1, col2 = (col1, col2) if col2 > col1 else (col2, col1)

				#   crop by using roi list
				cropImage = img[ row1 : row2, col1 : col2 ]

				#   resize image to desire size
				cropImageResized = cv2.resize( cropImage, ( imgWidth, imgHeight ) )
	
				#   append to roi list
				self.negativeImageList.append( cropImageResized )


		print "[INFO] Finish generate negative roi image "       

	def writeImage( self, savePathStr = '/tmpfs', zeroPad = 4 ):

		#   good path and bad path
		positiveImagePathStr = os.path.abspath( savePathStr ) + '/' + 'positive'
		negativeImagePathStr = os.path.abspath( savePathStr ) + '/' + 'negative'
	
		#   mkdir good and bad under save path
		os.mkdir( positiveImagePathStr )
		os.mkdir( negativeImagePathStr )

		#
		#   write positive image
		#

		print "[INFO] Save positive roi image"
		
		for idx, roiImage in enumerate( self.positiveImageList ):
			
			# #   get index name
			# idxNameStr = str( idx )
			# if len( idxNameStr ) == 1:
			# 	idxNameStr = '0000' + idxNameStr
			# elif len( idxNameStr ) == 2:
			# 	idxNameStr = '000' + idxNameStr
			# elif len( idxNameStr ) == 3:
			# 	idxNameStr = '00' + idxNameStr
			# elif len( idxNameStr ) == 4:
			# 	idxNameStr = '0' + idxNameStr

			idxStr = str( idx ).zfill( zeroPad )

			#   get file name
			frameNameStr = 'frame.{}.jpg'.format( idxStr )

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

		print "[INFO] Finish save positive roi image"

		#
		#   write negative image
		#

		print "[INFO] Save negative roi image"

		for idx, roiImage in enumerate( self.negativeImageList ):
			
			# #   get index name
			# idxNameStr = str( idx )
			# if len( idxNameStr ) == 1:
			# 	idxNameStr = '0000' + idxNameStr
			# elif len( idxNameStr ) == 2:
			# 	idxNameStr = '000' + idxNameStr
			# elif len( idxNameStr ) == 3:
			# 	idxNameStr = '00' + idxNameStr
			# elif len( idxNameStr ) == 4:
			# 	idxNameStr = '0' + idxNameStr

			idxStr = str( idx ).zfill( zeroPad )

			#   get file name
			frameNameStr = 'frame.{}.jpg'.format( idxStr )

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

		print "[INFO] Finish save negative roi image"

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
