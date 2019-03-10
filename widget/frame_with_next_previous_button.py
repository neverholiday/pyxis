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
from image_renderer import ImageLabel

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

class ImageWithNextPreviousButton( QtGui.QWidget ):

	def __init__( self, framePathStr, imageLabelClass, colorButtonInstance = None ):

		#   SUPAAA
		super( ImageWithNextPreviousButton, self ).__init__()

		#   generate image seqeunce from path given
		self.imageSequenceProvider = ImageSequence( framePathStr )

		#   initial flag play/pause
		self.playPauseFlag = 0

		#	add color button instance to attribute to this class
		self.colorButtonInstance = colorButtonInstance

		#   create instance of image label as image renderer
		self.imageLabel = imageLabelClass( self.imageSequenceProvider.currentFrameImage )
		self.displayImageWithMask()

		#   create next and previous button
		self.nextButton = QtGui.QPushButton( "Next" )
		self.playPauseButton = QtGui.QPushButton( "Play/Pause" )
		self.previousButton = QtGui.QPushButton( "Previous" )

		#	create shortcut for button
		self.nextButton.setShortcut( QtGui.QKeySequence( QtCore.Qt.Key_D ) )
		self.previousButton.setShortcut( QtGui.QKeySequence( QtCore.Qt.Key_A ) )
		self.playPauseButton.setShortcut( QtGui.QKeySequence( QtCore.Qt.Key_P ) )

		#   connect with function callback
		self.nextButton.clicked.connect( self.nextButtonFunctionCallback )
		self.previousButton.clicked.connect( self.previousButtonFunctionCallback )
		self.playPauseButton.clicked.connect( self.playPauseButtonFunctionCallback )

		#   start timer interupt
		#   connect with function callback 
		self.timerPlayPause = QtCore.QTimer()
		self.timerPlayPause.timeout.connect( self.timerToPlayFrameFunctionCallback )
		self.timerPlayPause.start( 20 )

		self.timerUpdateFrame = QtCore.QTimer()
		self.timerUpdateFrame.timeout.connect( self.timerUpdateFrameFunctionCallback )
		self.timerUpdateFrame.start( 1 )

		#   create layout
		self.buttonLayout = QtGui.QHBoxLayout()

		#   add widget
		self.buttonLayout.addWidget( self.previousButton )
		self.buttonLayout.addWidget( self.playPauseButton )
		self.buttonLayout.addWidget( self.nextButton )

		#   create vertical layout
		self.mainLayout = QtGui.QVBoxLayout()

		#   add all layout and widget to main layout
		self.mainLayout.addWidget( self.imageLabel )
		self.mainLayout.addLayout( self.buttonLayout )

		#   set main layout
		self.setLayout( self.mainLayout )

	def nextButtonFunctionCallback( self ):
		print "call nexButtonFunctionCallback"
		
		#   call provider
		self.imageSequenceProvider.nextFrame()
		
		print " {} / {} ".format( self.imageSequenceProvider.indexPointer + 1, self.imageSequenceProvider.numFrame )

		#	display!
		self.displayImageWithMask()

	def previousButtonFunctionCallback( self ):
		print "call previousButtonFunctionCallback"

		#   call provider
		self.imageSequenceProvider.previousFrame()
		
		print " {} / {} ".format( self.imageSequenceProvider.indexPointer + 1, self.imageSequenceProvider.numFrame )

		#	display!
		self.displayImageWithMask()
		
	def playPauseButtonFunctionCallback( self ):
		print "call playPauseButtonFunctionCallback"

		#	toggle state
		self.playPauseFlag = ( self.playPauseFlag + 1 ) % 2

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
			
			print " {} / {} ".format( self.imageSequenceProvider.indexPointer + 1, self.imageSequenceProvider.numFrame )

	def timerUpdateFrameFunctionCallback( self ):
		
		#	update current hsv value
		self.displayImageWithMask()


	def displayImageWithMask( self ):
		
		if self.colorButtonInstance == None:

			self.imageLabel.setImageLabel( self.imageSequenceProvider.currentFrameImage )
			return

		#	get value from slider
		upperValueArray, lowerValueArray = self.colorButtonInstance.getColorRangeValueList()

		#	get image with mask
		res = self.imageSequenceProvider.getImageWithMask( lowerValueArray, upperValueArray )

		#   set new image
		self.imageLabel.setImageLabel( res )


if __name__ == "__main__":

	from image_widget import ImageWithBoundingBox

	#	initial app
	app = QtGui.QApplication( sys.argv )
	
	#	call widget
	widget = ImageWithNextPreviousButton( "/home/neverholiday/work/ball_detector/raw_data/camera_onbot", ImageLabel )

	#	show
	widget.show()

	#	execute app
	sys.exit( app.exec_() )



		
