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

import random

########################################################
#
#	LOCAL IMPORTS
#

from PyQt4 import QtCore
from PyQt4 import QtGui

from frame_with_next_previous_button import ImageWithNextPreviousButton
from image_widget import ImageWithBoundingBox

from image_provider.roi_provider import ROIProvider

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

class FrameWithROI( ImageWithNextPreviousButton ):

	def __init__( self, framePathStr, saveYAMLPath ):

		#   super and override image label to have image roi callback
		super( FrameWithROI, self ).__init__( framePathStr, ImageWithBoundingBox )

		#	initial instance of roi provider
		self.roiProvider = ROIProvider()

		#	load yaml if it had
		if saveYAMLPath is not None:
			self.roiProvider.loadDataDict( saveYAMLPath )

			#	load saved roi
			positiveROIList, negativeROIList = self.loadCurrentROITuple()

			#	set saved positive roi list
			self.setListROI( positiveROIList, negativeROIList )

		#	add submit button
		self.submitPositiveButton = QtGui.QPushButton( "Submit Positive ROI" )
		self.submitNegativeButton = QtGui.QPushButton( "Submit Negative ROI" )
		self.randomButton = QtGui.QPushButton( "Random ROI" )
		self.setAreaRandomButton = QtGui.QPushButton( "Set random area" )
		self.exportButton = QtGui.QPushButton( "Export Image" )
		
		#	set shotcut
		self.submitPositiveButton.setShortcut( QtGui.QKeySequence( QtCore.Qt.Key_S ) )
		self.submitNegativeButton.setShortcut( QtGui.QKeySequence( QtCore.Qt.Key_X ) )
		self.randomButton.setShortcut( QtGui.QKeySequence( QtCore.Qt.Key_C ) )
		
		#	connect with callback function
		self.submitPositiveButton.clicked.connect( self.submitPositiveButtonFunctionCallback )
		self.submitNegativeButton.clicked.connect( self.submitNegativeButtonFunctionCallback )
		self.exportButton.clicked.connect( self.exportButtonFunctionCallback )
		self.randomButton.clicked.connect( self.randomButtonFunctionCallback )
		self.setAreaRandomButton.clicked.connect( self.setAreaRandomButtonFunctionCallback )
		
		#	create layout for negative
		self.negativeButtonGroupLayout = QtGui.QHBoxLayout()
		
		#	add button to negative layout
		self.negativeButtonGroupLayout.addWidget( self.submitNegativeButton )
		self.negativeButtonGroupLayout.addWidget( self.randomButton )
		self.negativeButtonGroupLayout.addWidget( self.setAreaRandomButton )

		#	add to main layout
		self.mainLayout.addWidget( self.submitPositiveButton )
		self.mainLayout.addLayout( self.negativeButtonGroupLayout )
		self.mainLayout.addWidget( self.exportButton )
		
		#
		#	parameter for random
		#
		
		#	get shape
		width = self.imageSequenceProvider.currentFrameImage.shape[ 1 ]
		height = self.imageSequenceProvider.currentFrameImage.shape[ 0 ]
		
		self.minX = 0
		self.maxX = width
		
		self.minY = 0
		self.maxY = height
		
	def nextButtonFunctionCallback( self ):
		print "call nexButtonFunctionCallback using child"

		#   call next frame
		self.imageSequenceProvider.nextFrame()
		
		print " {} / {} ".format( self.imageSequenceProvider.indexPointer + 1, self.imageSequenceProvider.numFrame )

		#	load saved roi
		positiveROIList, negativeROIList = self.loadCurrentROITuple()

		#	set saved positive roi list
		self.setListROI( positiveROIList, negativeROIList )

		#	display!
		self.displayImageWithMask()

		#	erase current rect
		self.imageLabel.topLeftPosition = QtCore.QPoint()
		self.imageLabel.bottomRightPosition = QtCore.QPoint()

	def previousButtonFunctionCallback( self ):
		print "call previousButtonFunctionCallback using child "

		#   call previous frame
		self.imageSequenceProvider.previousFrame()
		
		print " {} / {} ".format( self.imageSequenceProvider.indexPointer + 1, self.imageSequenceProvider.numFrame )

		#	load saved roi
		positiveROIList, negativeROIList = self.loadCurrentROITuple()

		#	set saved positive roi list
		self.setListROI( positiveROIList, negativeROIList )

		#	display!
		self.displayImageWithMask()

		#	erase current rect
		self.imageLabel.topLeftPosition = QtCore.QPoint()
		self.imageLabel.bottomRightPosition = QtCore.QPoint()

	def playPauseButtonFunctionCallback( self ):
		print "call playPauseButtonFunctionCallback"

		#	toggle state
		self.playPauseFlag = ( self.playPauseFlag + 1 ) % 2

		#	erase rect
		self.imageLabel.topLeftPosition = QtCore.QPoint()
		self.imageLabel.bottomRightPosition = QtCore.QPoint()
		
	def randomButtonFunctionCallback( self ):
		
		print "random"
		
		#	get shape
		width = self.imageSequenceProvider.currentFrameImage.shape[ 1 ]
		height = self.imageSequenceProvider.currentFrameImage.shape[ 0 ]
		
		#	random top left position
		#	TODO :
		#		User should available to limit random area 
		randomX = random.randint( self.minX, self.maxX )
		randomY = random.randint( self.minY, self.maxY )
		
		topLeftPosition = QtCore.QPoint( randomX, randomY )
		
		#	set bottom left position
		#	NOTE : set static width and height to 100, 100
		bottomRightPosition = QtCore.QPoint( randomX + 40, randomY + 40 )
		
		
		#	try to set rect at the image from random position
		self.imageLabel.topLeftPosition = topLeftPosition
		self.imageLabel.bottomRightPosition = bottomRightPosition
	
	def setAreaRandomButtonFunctionCallback( self ):
		
		#	get topleft and bottom right of roi
		topLeftRandomAreaPosition = ( self.imageLabel.topLeftPosition.y(), self.imageLabel.topLeftPosition.x() )
		bottomRightRandomAreaPosition = ( self.imageLabel.bottomRightPosition.y(), self.imageLabel.bottomRightPosition.x() )
		
		if not ( topLeftRandomAreaPosition == ( 0, 0 ) and bottomRightRandomAreaPosition == ( 0, 0 ) ):
			
			#	set to random attribute of this class
			self.minX = topLeftRandomAreaPosition[ 1 ]
			self.minY = topLeftRandomAreaPosition[ 0 ]

			self.maxX = bottomRightRandomAreaPosition[ 1 ]
			self.maxY = bottomRightRandomAreaPosition[ 0 ]
		
		print "Set area of random between ( {}, {} ) to ( {}, {} )".format( self.minX, self.minY, self.maxX, self.maxY )
				
	def submitPositiveButtonFunctionCallback( self ):
		
		print "Call positive submit"

		#	get frame name
		frameName = self.imageSequenceProvider.currentFramePath

		#	get topleft and bottom right of roi
		topLeftROIPosition = ( self.imageLabel.topLeftPosition.y(), self.imageLabel.topLeftPosition.x() )
		bottomRightROIPosition = ( self.imageLabel.bottomRightPosition.y(), self.imageLabel.bottomRightPosition.x() )
		
		if not ( topLeftROIPosition == ( 0, 0 ) and bottomRightROIPosition == ( 0, 0 ) ):

			#	save current roi position
			self.roiProvider.setPositiveData( frameName, topLeftROIPosition, bottomRightROIPosition )

			#	load saved roi
			positiveROIList, negativeROIList = self.loadCurrentROITuple()

			#	set saved positive roi list
			self.setListROI( positiveROIList, negativeROIList )		
	
	def submitNegativeButtonFunctionCallback( self ):
		
		print "Call negative submit"

		#	get frame name
		frameName = self.imageSequenceProvider.currentFramePath

		#	get topleft and bottom right of roi
		topLeftROIPosition = ( self.imageLabel.topLeftPosition.y(), self.imageLabel.topLeftPosition.x() )
		bottomRightROIPosition = ( self.imageLabel.bottomRightPosition.y(), self.imageLabel.bottomRightPosition.x() )
		
		if not ( topLeftROIPosition == ( 0, 0 ) and bottomRightROIPosition == ( 0, 0 ) ):
	
			#	save current roi position
			self.roiProvider.setNegativeData( frameName, topLeftROIPosition, bottomRightROIPosition )		

			#	load saved roi
			positiveROIList, negativeROIList = self.loadCurrentROITuple()

			#	set saved positive roi list
			self.setListROI( positiveROIList, negativeROIList )

	def exportButtonFunctionCallback( self ):

		#	generate roi image from position
		self.roiProvider.generateROIImage()
		
		#	popup and get path of saved directory
		saveDirectoryStr = str( QtGui.QFileDialog.getExistingDirectory( self, "Save directory", os.path.expanduser( "~" ) ) )

		print "Save as {}".format( saveDirectoryStr )

		#	export to tmpfs
		self.roiProvider.writeImage( savePathStr = saveDirectoryStr )
		
	def timerToPlayFrameFunctionCallback( self ):
		
		if self.playPauseFlag == 1:
			
			#	continueous to call next frame
			retrieve = self.imageSequenceProvider.nextFrame()
			
			#	display!
			self.displayImageWithMask()

			#	check if is final frame
			if not retrieve:

				self.imageSequenceProvider.setIndexFrame( 0 )
				
				#	display!
				self.displayImageWithMask()
			#	load saved roi
			positiveROIList, negativeROIList = self.loadCurrentROITuple()

			#	set saved positive roi list
			self.setListROI( positiveROIList, negativeROIList )
			
			#	set empty position to draw
			self.imageLabel.topLeftPosition = QtCore.QPoint()
			self.imageLabel.bottomRightPosition = QtCore.QPoint()
			
			print " {} / {} ".format( self.imageSequenceProvider.indexPointer + 1, self.imageSequenceProvider.numFrame )

	def loadCurrentROITuple( self ):

		#	get path name from frame provider
		frameName = self.imageSequenceProvider.currentFramePath

		#	load positive roi
		try:
			positiveROIList = self.roiProvider.positiveRoiDict[ frameName ]
		except KeyError:
			positiveROIList = list()
		
		#	load negative roi
		try:
			negativeROIList = self.roiProvider.negativeRoiDict[ frameName ]
		except KeyError:
			negativeROIList = list()
			
		print "At frame : {}".format( frameName )
		print "Saved Positive : {}".format( positiveROIList )
		print "Saved Negative : {}".format( negativeROIList )

		return positiveROIList, negativeROIList
	
	def setListROI( self, positiveROIList, negativeROIList ):

		self.imageLabel.submitPositivePosition = positiveROIList
		self.imageLabel.submitNegativePosition = negativeROIList

		#	update
		self.imageLabel.update()

		
if __name__ == "__main__":

	#	initial app
	app = QtGui.QApplication( sys.argv )
	
	#	call widget
	widget = FrameWithROI( "/home/neverholiday/work/ball_detector/raw_data/data1", saveYAMLPath = None )

	#	show
	widget.show()

	#	execute app
	sys.exit( app.exec_() )


