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

from PyQt4 import QtCore, QtGui

from image_renderer import ImageLabel
from image_provider.camera_provider import Camera

########################################################
#
#	GLOBALS
#

CAMERA_DEVICE_LIST = [ '/dev/video0', '/dev/video1' ]

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

class FrameWidget( QtGui.QWidget ):

	def __init__( self, cameraDevice, colorButtonInstance ):

		#   check camera device
		assert cameraDevice in CAMERA_DEVICE_LIST, "{} is not compatible with this software".format( cameraDevice )

		#   SUPAAAAA
		super( FrameWidget, self ).__init__()

		#   create instace of camera
		self.camera = Camera( cameraDevice )
		self.camera.read()  #   for getting first frame

		#   create instance of label
		self.imageLabel = ImageLabel( self.camera.frame )

		#	get instance of colorButton to get value
		self.colorButtonInstance = colorButtonInstance

		#   start timer interupt
		#   connect with function callback 
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect( self.updataFrameCallback )
		self.timer.start( 1 )

		#   create box layout
		self.verticalLayout = QtGui.QVBoxLayout()
		
		#   add image label to layout
		self.verticalLayout.addWidget( self.imageLabel )

		#   set layout 
		self.setLayout( self.verticalLayout )
	

	def updataFrameCallback( self ):
		
		#   read from camera
		self.camera.read()

		#	get upper and value array
		upperValueArray, lowerValueArray = self.colorButtonInstance.getColorRangeValueList()

		#	get image that and with mask
		resImage =	self.camera.getImageWithMask( upperValueArray, lowerValueArray )

		#   set new image to label
		self.imageLabel.setImageLabel( resImage )


if __name__ == "__main__":

	from widget.color_calibrate_button_widget import ColorButton
	
		#	initial app
	app = QtGui.QApplication( sys.argv )

	#	call instance of color button
	colorButton = ColorButton( 255, 255, 255, 0, 0, 0 )

	#	call widget
	widget = FrameWidget( '/dev/video1', colorButton )

	#	show
	widget.show()

	#	execute app
	sys.exit( app.exec_() )