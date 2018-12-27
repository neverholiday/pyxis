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

from PyQt4 import QtGui
from PyQt4 import QtCore

from image_provider.frame_provider import ImageSequence
from image_provider.roi_provider import ROIProvider
from image_widget import ImageWidget
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

########################################################
#
#	CLASS DEFINITIONS
#

class StepButton( QtGui.QWidget ):

	def __init__( self, imageSequenceProvider ):

		#   call super class of widget
		super( StepButton, self ).__init__()

		#   create instance of image provider
		self.imageSequenceProvider = imageSequenceProvider

		#	create instance of roi provider
		self.roiProvider = ROIProvider()

		#	create instance of image widget
		self.imageWidget = ImageWidget( self.imageSequenceProvider )

		#   create two button
		self.nextButton = QtGui.QPushButton( "Next (D)" )
		self.previousButton = QtGui.QPushButton( "Previous (A)" )
		self.submitPositiveROIButton = QtGui.QPushButton( "Submit Positive ROI (S)" )
		self.submitNegativeROIButton = QtGui.QPushButton( "Submit Negative ROI (W)" )
		self.exportImageButton = QtGui.QPushButton( "Export Image (X)" )

		#	set shortcut
		self.nextButton.setShortcut( QtGui.QKeySequence( QtCore.Qt.Key_D ) )
		self.previousButton.setShortcut( QtGui.QKeySequence( QtCore.Qt.Key_A ) )
		self.submitPositiveROIButton.setShortcut( QtGui.QKeySequence( QtCore.Qt.Key_S ) )
		self.submitNegativeROIButton.setShortcut( QtGui.QKeySequence( QtCore.Qt.Key_W ) )
		self.exportImageButton.setShortcut( QtGui.QKeySequence( QtCore.Qt.Key_X ) )

		#   connect callback function
		self.nextButton.clicked.connect( self.nextButtonCallback )
		self.previousButton.clicked.connect( self.previousButtonCallback )
		self.submitPositiveROIButton.clicked.connect( self.submitPositiveROIButtonCallback )
		self.submitNegativeROIButton.clicked.connect( self.submitNegativeROIButtonCallback )
		self.exportImageButton.clicked.connect( self.exportImageButtonCallback )

		#   create hbox layout
		self.horizontalBoxLayout = QtGui.QHBoxLayout()

		#   add two button to this layout
		self.horizontalBoxLayout.addWidget( self.previousButton )
		self.horizontalBoxLayout.addWidget( self.nextButton )

		#	create vertical box layout for submit
		self.verticalBoxSubmit = QtGui.QVBoxLayout()
		self.verticalBoxSubmit.addLayout( self.horizontalBoxLayout )
		self.verticalBoxSubmit.addWidget( self.submitPositiveROIButton )
		self.verticalBoxSubmit.addWidget( self.submitNegativeROIButton )
		self.verticalBoxSubmit.addWidget( self.exportImageButton )

		#	create vbox layout
		self.verticalBoxLayout = QtGui.QVBoxLayout()
		
		#	add image widget
		self.verticalBoxLayout.addWidget( self.imageWidget )

		#	add hbox layout
		self.verticalBoxLayout.addLayout( self.verticalBoxSubmit )

		#   set vertical box to main layout
		self.setLayout( self.verticalBoxLayout )
	
	def nextButtonCallback( self ):
		print "Call next!"
		self.imageSequenceProvider.nextFrame()
		print "Index frame : {} / {}".format( self.imageSequenceProvider.indexPointer, len( self.imageSequenceProvider.framePathList ) - 1 )

		print "Path image : {}".format( self.imageSequenceProvider.currentFramePath )

		#	change image
		self.imageWidget.imageLabel.setImageLabel( self.imageSequenceProvider.currentFrameImage )

		#	set none to upper left and bottom right
		self.imageWidget.imageLabel.bottomRightPosition = None
		self.imageWidget.imageLabel.topLeftPosition = None

		#	update
		self.imageWidget.imageLabel.update()

	def previousButtonCallback( self ):
		print "Call previous!" 
		self.imageSequenceProvider.previousFrame()
		print "Index frame : {} / {}".format( self.imageSequenceProvider.indexPointer, len( self.imageSequenceProvider.framePathList ) - 1 )

		print "Path image : {}".format( self.imageSequenceProvider.currentFramePath )
		
		#	change image
		self.imageWidget.imageLabel.setImageLabel( self.imageSequenceProvider.currentFrameImage )

		#	set none to upper left and bottom right
		self.imageWidget.imageLabel.bottomRightPosition = None
		self.imageWidget.imageLabel.topLeftPosition = None

		#	update
		self.imageWidget.imageLabel.update()

	def submitPositiveROIButtonCallback( self ):

		#	get ROI from image label
		#	NOTE:
		#		Swap x and y because image from opencv store as matrix form.

		try:	
			topLeft = ( self.imageWidget.imageLabel.topLeftPosition.y(),
						self.imageWidget.imageLabel.topLeftPosition.x() )

			bottomRight = ( self.imageWidget.imageLabel.bottomRightPosition.y(),
							self.imageWidget.imageLabel.bottomRightPosition.x() )

			#	set path of an image and roi location ( top left, bottom right )
			self.roiProvider.setPositiveData( self.imageSequenceProvider.currentFramePath, topLeft, bottomRight )
	
		except AttributeError:
			print "[ERROR] Bounding box has not ready."

		#	call some function for save ROI
		#	NOW I JUST PRINT IT
		print "Detail of {}".format( self.imageSequenceProvider.currentFramePath )
		print "Top left : {}, Bottom right : {} ".format( topLeft, bottomRight )
	
	def submitNegativeROIButtonCallback( self ):

		#	get ROI from image label
		#	NOTE:
		#		Swap x and y because image from opencv store as matrix form.

		try:	
			topLeft = ( self.imageWidget.imageLabel.topLeftPosition.y(),
						self.imageWidget.imageLabel.topLeftPosition.x() )

			bottomRight = ( self.imageWidget.imageLabel.bottomRightPosition.y(),
							self.imageWidget.imageLabel.bottomRightPosition.x() )

			#	set path of an image and roi location ( top left, bottom right )
			self.roiProvider.setNegativeData( self.imageSequenceProvider.currentFramePath, topLeft, bottomRight )
	
		except AttributeError:
			print "[ERROR] Bounding box has not ready."

		#	call some function for save ROI
		#	NOW I JUST PRINT IT
		print "Detail of {}".format( self.imageSequenceProvider.currentFramePath )
		print "Top left : {}, Bottom right : {} ".format( topLeft, bottomRight )

	def exportImageButtonCallback( self ):
		
		print "Generate ROI image from data"
		#	generate roi list first
		self.roiProvider.generateROIImage()
		print "Done!"

		print "Write image"
		#	export image to specify path
		self.roiProvider.writeImage()
		print "Done!"

if __name__ == "__main__":

	#	initial app
	app = QtGui.QApplication( sys.argv )
	
	#   create frame provider to test
	frameProvider = ImageSequence( TEST_FRAME_PATH )

	#	call widget
	widget = StepButton( frameProvider )

	#	show
	widget.show()

	#	execute app
	sys.exit( app.exec_() )

