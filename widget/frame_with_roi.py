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
		self.exportButton = QtGui.QPushButton( "Export Image" )

		#	connect with callback function
		self.submitPositiveButton.clicked.connect( self.submitPositiveButtonFunctionCallback )
		self.submitNegativeButton.clicked.connect( self.submitNegativeButtonFunctionCallback )
		self.exportButton.clicked.connect( self.exportButtonFunctionCallback )

		#	add to main layout
		self.mainLayout.addWidget( self.submitPositiveButton )
		self.mainLayout.addWidget( self.submitNegativeButton )
		self.mainLayout.addWidget( self.exportButton )
		
	def nextButtonFunctionCallback( self ):
		print "call nexButtonFunctionCallback using child"

		#   call next frame
		self.imageSequenceProvider.nextFrame()

		#	load saved roi
		positiveROIList, negativeROIList = self.loadCurrentROITuple()

		#	set saved positive roi list
		self.setListROI( positiveROIList, negativeROIList )

		#	display!
		self.displayImageWithMask()

		#	erase current rect
		self.imageLabel.topLeftPosition = None
		self.imageLabel.bottomRightPosition = None

	def previousButtonFunctionCallback( self ):
		print "call previousButtonFunctionCallback using child "

		#   call previous frame
		self.imageSequenceProvider.previousFrame()

		#	load saved roi
		positiveROIList, negativeROIList = self.loadCurrentROITuple()

		#	set saved positive roi list
		self.setListROI( positiveROIList, negativeROIList )

		#	display!
		self.displayImageWithMask()

		#	erase current rect
		self.imageLabel.topLeftPosition = None
		self.imageLabel.bottomRightPosition = None

	def playPauseButtonFunctionCallback( self ):
		print "call playPauseButtonFunctionCallback"

		#	toggle state
		self.playPauseFlag = ( self.playPauseFlag + 1 ) % 2

		#	erase rect
		self.imageLabel.topLeftPosition = None
		self.imageLabel.bottomRightPosition = None

	def submitPositiveButtonFunctionCallback( self ):
		
		print "Call positive submit"

		#	get frame name
		frameName = self.imageSequenceProvider.currentFramePath

		#	get topleft and bottom right of roi
		topLeftROIPosition = ( self.imageLabel.topLeftPosition.y(), self.imageLabel.topLeftPosition.x() )
		bottomRightROIPosition = ( self.imageLabel.bottomRightPosition.y(), self.imageLabel.bottomRightPosition.x() )

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


